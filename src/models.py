from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
class Pedido(db.Model):
    __tablename__ = 'pedidos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idpediddo = db.Column(db.String(20))
    nombre = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(100))
    fecha = db.Column(db.Date, default=datetime.utcnow)
    tamanio = db.Column(db.String(20))
    cantidad = db.Column(db.Integer)
    champi = db.Column(db.Boolean, default=False)
    jamon = db.Column(db.Boolean, default=False)
    pina = db.Column(db.Boolean, default=False)
    subtotal = db.Column(db.Float)
    
   