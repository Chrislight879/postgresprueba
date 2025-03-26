from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from forms import ProductoForm 
from models import db, Producto, Categoria

app = Flask(__name__)

# CONEXION A BASE DE DATOS

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:1234@localhost:5432/TiendonaDb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "clave_secreta"


db.init_app(app)

# Crear la base de datos si no existe
with app.app_context():
    db.create_all()

# ===========================
#   RUTA PRINCIPAL
# ===========================

@app.route('/')
def index():
    return render_template('base.html')

# ===========================
#   RUTAS PARA PRODUCTOS
# ===========================

@app.route('/productos')
def lista_productos():
    productos = Producto.query.all()
    return render_template('producto/index.html', productos=productos)

@app.route('/productos/agregar', methods=['GET', 'POST'])
def agregar_producto():
    form = ProductoForm() 
    form.categoria_id.choices = [(c.id, c.nombre) for c in Categoria.query.all()]

    if form.validate_on_submit():
        nuevo_producto = Producto(
            nombre=form.nombre.data,
            stock=form.stock.data,
            precio=form.precio.data,
            categoria_id=form.categoria_id.data,
            descripcion=form.descripcion.data,
            imagen=form.imagen.data
        )
        db.session.add(nuevo_producto)
        db.session.commit()
        return redirect(url_for('lista_productos'))
    
    return render_template('producto/add.html', form=form)

@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    producto = Producto.query.get_or_404(id)
    form = ProductoForm(obj=producto)
    form.categoria_id.choices = [(c.id, c.nombre) for c in Categoria.query.all()]

    if form.validate_on_submit():
        producto.nombre = form.nombre.data
        producto.stock = form.stock.data
        producto.precio = form.precio.data
        producto.categoria_id = form.categoria_id.data
        producto.descripcion = form.descripcion.data
        producto.imagen = form.imagen.data
        db.session.commit()
        return redirect(url_for('lista_productos'))
    
    return render_template('producto/edit.html', form=form, producto=producto)

@app.route('/productos/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)

    if request.method == 'POST':
        db.session.delete(producto)
        db.session.commit()
        return redirect(url_for('lista_productos'))

    return render_template('producto/delete.html', producto=producto)

# ===========================
#   RUTAS PARA CATEGORÍAS
# ===========================

@app.route('/categorias')
def lista_categorias():
    categorias = Categoria.query.all()
    return render_template('categoria/index.html', categorias=categorias)

@app.route('/categorias/agregar', methods=['GET', 'POST'])
def agregar_categoria():
    if request.method == 'POST':
        nombre = request.form['nombre']
        nueva_categoria = Categoria(nombre=nombre)
        db.session.add(nueva_categoria)
        db.session.commit()
        return redirect(url_for('lista_categorias'))
    
    return render_template('categoria/add.html')

@app.route('/categorias/editar/<int:id>', methods=['GET', 'POST'])
def editar_categoria(id):
    categoria = Categoria.query.get_or_404(id)

    if request.method == 'POST':
        categoria.nombre = request.form['nombre']
        db.session.commit()
        return redirect(url_for('lista_categorias'))

    return render_template('categoria/edit.html', categoria=categoria)

@app.route('/categorias/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminar_categoria(id):
    categoria = Categoria.query.get_or_404(id)

    if request.method == 'POST':
        db.session.delete(categoria)
        db.session.commit()
        return redirect(url_for('lista_categorias'))

    return render_template('categoria/delete.html', categoria=categoria)

# ===========================
#   EJECUTAR LA APLICACIÓN
# ===========================

if __name__ == "__main__":
    app.run(debug=True)
