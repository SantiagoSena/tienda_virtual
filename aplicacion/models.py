# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class DetallePedido(models.Model):
    iddetallep = models.AutoField(db_column='idDetalleP', primary_key=True)  # Field name made lowercase.
    idpedido = models.ForeignKey('Pedido', models.DO_NOTHING, db_column='idPedido', blank=True, null=True)  # Field name made lowercase.
    idproducto = models.ForeignKey('Producto', models.DO_NOTHING, db_column='idProducto', blank=True, null=True)  # Field name made lowercase.
    cantidad = models.IntegerField(blank=True, null=True)
    valorproducto = models.IntegerField(db_column='valorProducto', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'detalle_pedido'


class Pedido(models.Model):
    idpedido = models.AutoField(db_column='idPedido', primary_key=True)  # Field name made lowercase.
    estado = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pedido'


class Producto(models.Model):
    idproducto = models.AutoField(db_column='idProducto', primary_key=True)  # Field name made lowercase.
    nombreprod = models.CharField(db_column='nombreProd', max_length=50, blank=True, null=True)  # Field name made lowercase.
    cantidad = models.IntegerField(blank=True, null=True)
    valor = models.IntegerField(blank=True, null=True)
    imagen = models.ImageField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'producto'

    def __str__(self):
        return self.nombreprod

