import pymysql
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

from flask_cors import CORS

# from app.config import config
from config import config

app=Flask(__name__)
CORS(app)

con=MySQL(app)

# db = pymysql.connect(
#     host=config['development'].MYSQL_HOST,
#     user=config['development'].MYSQL_USER,
#     password=config['development'].MYSQL_PASSWORD,
#     database=config['development'].MYSQL_DB,
#     ssl={'ssl': {}}  )


@app.route("/alumnos", methods=['GET'])
def lista_alumnos():
    try:
        cursor=con.connection.cursor()
        cursor = con.connection.cursor()
        cursor.execute("SELECT 1")
        sql='select * from alumnos'
        cursor.execute(sql)
        datos=cursor.fetchall()
        alumnos=[]
        for fila in datos:
            alumno={ 'matricula':fila[0], 'nombre':fila[1], 'apaterno':fila[2], 'amaterno':fila[3], 'email':fila[4]}
            
            alumnos.append(alumno)
            print(alumnos)
            
        return jsonify({'alumnos':alumnos, 'mensaje': 'Lista de alumnos', 'exito':True})
    except Exception as ex:
        return jsonify({"message": "Error al conectar con la base de datos {}".format(ex),'exito':False})

def leer_alumno_bd(matricula):
    try:
        cursor=con.connection.cursor()
        sql='select * from alumnos where matricula={0}'.format(matricula)
        cursor.execute(sql)
        datos=cursor.fetchome()
        if datos!=None:
            alumno={'matricula':datos[0], 'nombre':datos[1], 'apaterno':datos[2], 'amaterno':datos[3], 'correo':datos[4]}
            return alumno
        else:
            return None
        
    except Exception as ex:
        return jsonify({"message": "Error al conectar a la base de datos {}"})

# nueva ruta ENCONTRAR POR MATRICULA
@app.route('/alumnos/<mat>', methods=['GET'])
def leer_curso(mat):
    try:
        alumno = leer_alumno_bd(mat)
        if alumno != None:
            return jsonify({'alumno': alumno, 'mensaje': "Alumno encontrado.", 'exito': True})
        else:
            return jsonify({'mensaje': "Alumno no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})
    
    
#ENVIAR DATOS
@app.route('/alumnos/<mat>', methods=['PUT'])
def actualizar_curso(mat):
    #if (validar_matricula(mat) and validar_nombre(request.json['nombre']) and validar_apaterno(request.json['apaterno'])):
        try:
            alumno = leer_alumno_bd(mat)
            if alumno != None:
                cursor = con.connection.cursor()
                sql = """UPDATE alumnos SET nombre = '{0}', apaterno = '{1}', amaterno='{2}', correo='{3}'
                WHERE matricula = {4}""".format(request.json['nombre'], request.json['apaterno'], request.json['amaterno'],request.json['correo'], mat)
                cursor.execute(sql)
                con.connection.commit()  # Confirma la acción de actualización.
                return jsonify({'mensaje': "Alumno actualizado.", 'exito': True})
            else:
                return jsonify({'mensaje': "Alumno no encontrado.", 'exito': False})
        except Exception as ex:
            return jsonify({'mensaje': "Error {0} ".format(ex), 'exito': False})

 
@app.route('/alumnos/<mat>', methods=['DELETE'])
def eliminar_curso(mat):
    try:
        alumno = leer_alumno_bd(mat)
        if alumno != None:
            cursor = con.connection.cursor()
            sql = "DELETE FROM alumnos WHERE matricula = {0}".format(mat)
            cursor.execute(sql)
            con.connection.commit()  # Confirma la acción de eliminación.
            return jsonify({'mensaje': "Alumno eliminado.", 'exito': True})
        else:
            return jsonify({'mensaje': "Alumno no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})
    
    
def pagina_no_encontrada(error):
    return "<h1>La pagina que esta buscando no existe</h1>", 400

if __name__ == "__main__":
    app.config.from_object(config['development'])
    print("Configuration loaded:", app.config) 
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(host='0.0.0.0', port=5000)