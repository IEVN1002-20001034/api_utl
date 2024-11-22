from flask import Flask, jsonify, request
from flask_cors import CORS
from config import DevelopmentConfig
from models import db, Pedido
from datetime import datetime

app = Flask(__name__)
CORS(app)
app.config.from_object(DevelopmentConfig)

#DECORADORES O RUTAS
@app.route('/api', methods=['GET'])
def get_data():
    data = {"message": "Bienvenido a PIZZERIA API!"}
    return data

@app.route('/api/addpedido', methods=['POST'])
def add_pedido():
    datos = request.get_json()
    
    print(datos)
    if not datos:
        return jsonify({"status": False, "error": "Se esperaba un array"}), 400

    pedidos_ids = []
    for pedido in datos['pedidos']:
        try:
            nombre = pedido.get('nombre')
            idpediddo = datos['id_compra']
            telefono = pedido.get('telefono')
            direccion = pedido.get('direccion')
            fecha = pedido.get('fecha')
            tamanio = pedido.get('tamanio')
            cantidad = int(pedido.get('cantidad', 0))
            champi = bool(pedido.get('champi'))
            jamon = bool(pedido.get('jamon'))
            pina = bool(pedido.get('pina'))
            subtotal = float(pedido.get('subtotal', 0.0))

            fecha = datetime.strptime(fecha, '%Y-%m-%d') if fecha else None

            newPedido = Pedido(
                nombre=nombre,
                idpediddo= idpediddo,
                telefono=telefono,
                direccion=direccion,
                fecha=fecha,
                tamanio=tamanio,
                cantidad=cantidad,
                champi=champi,
                jamon=jamon,
                pina=pina,
                subtotal=subtotal
            )
            db.session.add(newPedido)
            db.session.commit()
            pedidos_ids.append(newPedido.id)
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": False, "error": f"Error al procesar pedido: {str(e)}"}), 500

    return jsonify({"status": True,"message": f"Pedidos agregados exitosamente","pedidos_ids": pedidos_ids}), 200


@app.route('/api/getpedidos', methods=['GET'])
def get_pedido():
    pedidos = Pedido.query.all()
    
    if not pedidos: 
        return jsonify({"status": False, "message": "No se ha encontrado ningún pedido"}), 400
    pedidos_data = [
        {
            "nombre":pedido.nombre,
            "telefono":pedido.telefono,
            "idpediddo":pedido.idpediddo,
            "direccion":pedido.direccion,
            "fecha":pedido.fecha,
            "tamanio":pedido.tamanio,
            "cantidad":pedido.cantidad,
            "champi":pedido.champi,
            "jamon":pedido.jamon,
            "pina":pedido.pina,
            "subtotal":pedido.subtotal
        }
        for pedido in pedidos
    ]

    data = jsonify({"status": True, "pedidos": pedidos_data}), 201
            

    return data

if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)


