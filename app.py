from flask import Flask, render_template, request
from babel.numbers import format_currency


app = Flask(__name__)

def calcular_valor_cuota(monto, tasa_interes, plazo):
    # se deriva la forma de calcular la cuota de la siguiente manera:
    # cuota = monto/ factor
    # el 'factor' corresponde a la suma de 1/(1+i)^1 + 1/(1+i)^2 + ... + 1/(1+i)^n
    # se debe crear link en documentación para la foto donde despejo la fórmula matemática
    factor = 0
    for j in range(plazo):
        factor += 1/((1+tasa_interes)**(j+1))
    valor_cuota = monto/factor
    return valor_cuota

def calcular_plan_pagos(monto, tasa_interes, plazo):
    # Lógica para calcular el plan de pagos aquí
    # Esto es solo un ejemplo, debes implementar los cálculos financieros adecuados
    pagos = []
    valor_cuota = calcular_valor_cuota(monto, tasa_interes, plazo)

    # se agrega el primer elemento del arreglo de pagos. Este corresponde a un pago 0
    # en el cual no hay cuota ni intereses, sólo el saldo inicial
    pagos.append({
        "numero_cuota": 0,
        "monto_cuota": 0,
        "interes_cuota": 0,
        "saldo_pendiente": monto
    })
    # se agrega el plan de pagos
    for i in range(plazo):
        pago_anterior = pagos[-1]
        saldo_anterior = pago_anterior['saldo_pendiente']
        intereses_cuota = saldo_anterior*tasa_interes
        capital_cuota = valor_cuota - intereses_cuota
        saldo_pendiente = saldo_anterior - capital_cuota
        pago = {
            "numero_cuota": i + 1,
            "monto_cuota": valor_cuota,
            "interes_cuota": intereses_cuota,
            "saldo_pendiente": saldo_pendiente
        }
        pagos.append(pago)
    return pagos

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        monto = float(request.form['monto'])
        tasa_interes = float(request.form['tasa_interes']) / 100
        plazo = int(request.form['plazo'])
        plan_pagos = calcular_plan_pagos(monto, tasa_interes, plazo)
        return render_template('index.html', plan_pagos=plan_pagos)
    return render_template('index.html')

@app.template_filter('currency')
def format_currency_filter(value):
    return format_currency(value, 'COP', locale='es_CO')


if __name__ == '__main__':
    app.run(debug=True)
