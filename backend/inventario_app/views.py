# 4.- JPA Repository

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import Producto, Categoria, Marca
from utils.divisas import obtener_valor_dolar

# READ ALL
def productos_api(request):
    productos = Producto.objects.all().values(
        'producto_id',
        'nombre_producto',
        'modelo',
        'precio',
        'codigo_sku',
        'categoria__nombre_categoria',
        'marca__nombre_marca'
    )

    valor_dolar = obtener_valor_dolar()

    # Agregar el precio en dólares a cada producto
    productos_con_usd = []
    for p in productos:
        precio_usd = round(p['precio'] / valor_dolar, 2) if valor_dolar > 0 else None
        p['precio_usd'] = precio_usd
        productos_con_usd.append(p)

    return JsonResponse(productos_con_usd, safe=False)

# CREAR
@csrf_exempt  # Solo si no usas token CSRF (para pruebas)
def crear_producto(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            categoria = Categoria.objects.get(pk=data['categoria_id'])
            marca = Marca.objects.get(pk=data['marca_id'])

            producto = Producto.objects.create(
                nombre_producto=data['nombre_producto'],
                modelo=data.get('modelo'),
                precio=data['precio'],
                codigo_sku=data['codigo_sku'],
                categoria=categoria,
                marca=marca
            )

            return JsonResponse({'mensaje': 'Producto creado', 'id': producto.producto_id}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

#READ ONE
@csrf_exempt
def producto_por_id(request, id):
    if request.method == 'GET':
        try:
            producto = Producto.objects.select_related('categoria', 'marca').get(pk=id)
            data = {
                'producto_id': producto.producto_id,
                'nombre_producto': producto.nombre_producto,
                'modelo': producto.modelo,
                'precio': producto.precio,
                'codigo_sku': producto.codigo_sku,
                'categoria': producto.categoria.nombre_categoria,
                'marca': producto.marca.nombre_marca,
            }
            return JsonResponse(data, status=200)
        except Producto.DoesNotExist:
            return JsonResponse({'error': 'Producto no encontrado'}, status=404)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

#Update: PUT
@csrf_exempt
def actualizar_producto(request, id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)

            producto = Producto.objects.get(pk=id)

            producto.nombre_producto = data.get('nombre_producto', producto.nombre_producto)
            producto.modelo = data.get('modelo', producto.modelo)
            producto.precio = data.get('precio', producto.precio)
            producto.codigo_sku = data.get('codigo_sku', producto.codigo_sku)

            if 'categoria_id' in data:
                producto.categoria = Categoria.objects.get(pk=data['categoria_id'])

            if 'marca_id' in data:
                producto.marca = Marca.objects.get(pk=data['marca_id'])

            producto.save()

            return JsonResponse({'mensaje': 'Producto actualizado correctamente'}, status=200)

        except Producto.DoesNotExist:
            return JsonResponse({'error': 'Producto no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

#Delete
@csrf_exempt
def eliminar_producto(request, id):
    if request.method == 'DELETE':
        try:
            producto = Producto.objects.get(pk=id)
            producto.delete()
            return JsonResponse({'mensaje': 'Producto eliminado correctamente'}, status=200)
        except Producto.DoesNotExist:
            return JsonResponse({'error': 'Producto no encontrado'}, status=404)
    return JsonResponse({'error': 'Método no permitido'}, status=405)