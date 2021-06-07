from flask import Flask, url_for, redirect
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SECRET_KEY'] = "123"
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

db = SQLAlchemy(app)

class usuario(db.Model):
    id = db.Column('user_id', db.Integer, primary_key=True)
    usuario_nombre = db.Column(db.String(100))
    usuario_direccion = db.Column(db.String(100))

    def __init__(self,datos):
        self.usuario_nombre = datos["nombre"]
        self.usuario_direccion = datos["direccion"]

@app.route('/')
@cross_origin()
def principal():
    data = usuario.query.all()
    diccionario_usuarios = {}
    for d in data:
        p = { 
            'id': d.id,
            'nombre': d.usuario_nombre,
            'direccion': d.usuario_direccion,
            }
        diccionario_usuarios[d.id] = p
    return diccionario_usuarios


@app.route('/agregar/<nombre>/<direccion>')
@cross_origin()
def agregar(nombre, direccion):
    datos = {
        "nombre": nombre,
        "direccion": direccion,
        }
    p = usuario(datos)
    db.session.add(p)
    db.session.commit()
    return redirect(url_for('principal'))

@app.route('/eliminar/<int:id>')
@cross_origin()
def eliminar(id):
    p = usuario.query.filter_by(id=id).first()
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('principal'))

@app.route('/actualizar/<int:id>/<nombre>/<direccion>')
@cross_origin()
def actualizar(id, nombre, direccion):
    p = usuario.query.filter_by(id=id).first()
    p.usuario_nombre = nombre
    p.usuario_direccion = direccion
    db.session.commit()
    return redirect(url_for('principal'))

@app.route('/buscar/<int:id>')
@cross_origin()
def buscar(id):
    d = usuario.query.filter_by(id=id).first()
    p = { 
        'id': d.id,
        'nombre': d.usuario_nombre,
        'direccion': d.usuario_direccion,
    }
    return p


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
