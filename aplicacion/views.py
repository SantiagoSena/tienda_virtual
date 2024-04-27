from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction

from aplicacion.models import *

def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'lista_productos.html', {'productos': productos})

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, idproducto=producto_id)
    return render(request, 'detalle_producto.html', {'producto': producto})

def agregar_carrito(request, producto_id):
    producto = get_object_or_404(Producto, idproducto=producto_id)
    
    # Verificar si el producto está agotado
    if producto.cantidad == 0:
        messages.warning(request, f"¡Lo siento! {producto.nombreprod} está agotado.")
        return redirect('lista_productos')
    
    carrito = request.session.get('carrito', {})
    
    # Incrementar la cantidad si el producto ya está en el carrito
    if producto_id in carrito:
        carrito[producto_id]['cantidad'] += 1
    else:
        carrito[producto_id] = {
            'nombre': producto.nombreprod,
            'cantidad': 1,
            'valor_unitario': producto.valor
        }
    
    request.session['carrito'] = carrito
    messages.success(request, f"{producto.nombreprod} ha sido agregado al carrito.")
    return redirect('lista_productos')



def carrito_compras(request):
     if request.method == 'GET':
        carrito_ids = request.session.get('carrito', [])
        productos_en_carrito = Producto.objects.filter(idproducto__in=carrito_ids)
        total = sum(producto.valor for producto in productos_en_carrito)
        return render(request, 'carrito_compras.html', {'productos_en_carrito': productos_en_carrito, 'total': total})
     elif request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        if producto_id:
            carrito = request.session.get('carrito', [])
            carrito.append(int(producto_id))
            request.session['carrito'] = carrito
            messages.success(request, "Producto agregado al carrito.")
        return redirect('carrito_compras')

def eliminar_del_carrito(request, producto_id):
    producto = get_object_or_404(Producto, idproducto=producto_id)
    carrito = request.session.get('carrito', [])
    if producto_id in carrito:
        carrito.remove(producto_id)
        request.session['carrito'] = carrito
        messages.success(request, f"{producto.nombreprod} ha sido eliminado del carrito.")
    return redirect('ver_carrito')

@transaction.atomic
def realizar_pedido(request):
    carrito = request.session.get('carrito', {})
    pedido = Pedido.objects.create(estado='pendiente')
    for producto_id, detalle_carrito in carrito.items():
        producto = get_object_or_404(Producto, idproducto=producto_id)
        cantidad = detalle_carrito['cantidad']
        DetallePedido.objects.create(
            idpedido=pedido,
            idproducto=producto,
            cantidad=cantidad,
            valorproducto=producto.valor * cantidad
        )
        # Resta la cantidad comprada del inventario
        producto.cantidad -= cantidad
        producto.save()
    # Limpia el carrito después de realizar el pedido
    request.session.pop('carrito')
    messages.success(request, "Tu pedido ha sido realizado. ¡Gracias por tu compra!")
    return redirect('detalle_pedido', pedido_id=pedido.idpedido)

def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, idpedido=pedido_id)
    detalles = DetallePedido.objects.filter(idpedido=pedido)
    return render(request, 'detalle_pedido.html', {'pedido': pedido, 'detalles': detalles})



def listar_pedidos(request):
    pedidos = Pedido.objects.all()
    for pedido in pedidos:
        detalles = DetallePedido.objects.filter(idpedido=pedido)
        valor_total = sum(detalle.valorproducto for detalle in detalles)
        pedido.valor_total = valor_total
    return render(request, 'listar_pedidos.html', {'pedidos': pedidos})