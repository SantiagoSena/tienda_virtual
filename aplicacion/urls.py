from django.urls import path

from . import views

urlpatterns = [
    path('', views.lista_productos, name='lista_productos'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('agregar_carrito/<int:producto_id>/', views.agregar_carrito, name='agregar_carrito'),
    path('eliminar_del_carrito/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('realizar_pedido/', views.realizar_pedido, name='realizar_pedido'),
    path('carrito_compras/', views.carrito_compras, name='carrito_compras'),
    path('detalle_pedido/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
    path('listar_pedidos/', views.listar_pedidos, name='listar_pedidos'),
]