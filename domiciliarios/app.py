from flask import Flask, url_for, redirect
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///domiciliarios.db'
app.config['SECRET_KEY'] = "123"
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

db = SQLAlchemy(app)

class domiciliario(db.Model):
    id = db.Column('user_id', db.Integer, primary_key=True)
    domiciliario_nombre = db.Column(db.String(100))
    domiciliario_empresa = db.Column(db.String(100))

    def __init__(self,datos):
        self.domiciliario_nombre = datos["nombre"]
        self.domiciliario_empresa = datos["empresa"]

@app.route('/')
@cross_origin()
def principal():
    data = domiciliario.query.all()
    diccionario_domiciliarios = {}
    for d in data:
        p = { 
            'id': d.id,
            'nombre': d.domiciliario_nombre,
            'empresa': d.domiciliario_empresa,
            }
        diccionario_domiciliarios[d.id] = p
    return diccionario_domiciliarios


@app.route('/agregar/<nombre>/<empresa>')
@cross_origin()
def agregar(nombre, empresa):
    datos = {
        "nombre": nombre,
        "empresa": empresa,
        }
    p = domiciliario(datos)
    db.session.add(p)
    db.session.commit()
    return redirect(url_for('principal'))

@app.route('/eliminar/<int:id>')
@cross_origin()
def eliminar(id):
    p = domiciliario.query.filter_by(id=id).first()
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('principal'))

@app.route('/actualizar/<int:id>/<nombre>/<empresa>')
@cross_origin()
def actualizar(id, nombre, empresa):
    p = domiciliario.query.filter_by(id=id).first()
    p.domiciliario_nombre = nombre
    p.domiciliario_empresa = empresa
    db.session.commit()
    return redirect(url_for('principal'))

@app.route('/buscar/<int:id>')
@cross_origin()
def buscar(id):
    d = domiciliario.query.filter_by(id=id).first()
    p = { 
        'id': d.id,
        'nombre': d.domiciliario_nombre,
        'empresa': d.domiciliario_empresa,
    }
    return p


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
