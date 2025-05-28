import bcchapi
import datetime
from decimal import Decimal

def obtener_valor_dolar():
    try:
        siete = bcchapi.Siete(file="credenciales/credenciales.txt")
        hoy = datetime.date.today().isoformat()
        datos = siete.cuadro(
            series=["F073.TCO.PRE.Z.D"],
            nombres=["dolar"],
            desde=hoy,
            hasta=hoy
        )
        valor = datos.iloc[0]['dolar']
        print("Dólar obtenido:", valor)  # 👈 Agrega esta línea
        return Decimal(valor)
    except Exception as e:
        print("❌ Error al obtener el dólar:", e)
        return Decimal("0")

