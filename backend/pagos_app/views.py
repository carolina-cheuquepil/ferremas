# ---------------- PASO 1 TBK-----------------
# pip install transbank-sdk

# ---------------- PASO 2 TBK-----------------
#Configuración en el archivo settings.py

# ---------------- PASO 3 TBK-----------------
#Importación de Módulos Necesarios:
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.integration_type import IntegrationType
from pedidos_app.models import Pedido
from .models import Pago

def construir_transaccion():
    return Transaction.build_for_integration(
        commerce_code=settings.TRANSBANK['COMMERCE_CODE'],
        api_key=settings.TRANSBANK['API_KEY']
    )

def iniciar_pago(request, pedido_id):
    transaction = construir_transaccion()

    pedido = get_object_or_404(Pedido, pk=pedido_id)

    buy_order = str(pedido.pedido_id)
    session_id = str(request.user.id)
    amount = pedido.total
    return_url = 'http://localhost:8000/pagos/retorno/'

    response = transaction.create(buy_order, session_id, amount, return_url)

    return redirect(f"{response['url']}?token_ws={response['token']}")

def retorno_pago(request):
    transaction = construir_transaccion()

    token = request.GET.get('token_ws')

    response = transaction.commit(token)

    if response['status'] == 'AUTHORIZED':
        pedido = Pedido.objects.get(pedido_id=response['buy_order'])
        Pago.objects.create(
            pedido=pedido,
            metodo_pago='WebPay Plus',
            monto=pedido.total
        )
        return render(request, 'pagos_app/exito.html', {'pedido': pedido})
    else:
        return render(request, 'pagos_app/error.html')




