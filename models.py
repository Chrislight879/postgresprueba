from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Numeric(10,2), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id', ondelete="CASCADE"), nullable=False)
    imagen = db.Column(db.Text)
    descripcion = db.Column(db.Text)


    categoria = db.relationship('Categoria', backref=db.backref('productos', lazy=True))


