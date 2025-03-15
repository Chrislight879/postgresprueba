from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    stock = IntegerField('Stock', validators=[DataRequired(), NumberRange(min=0)])
    precio = DecimalField('Precio', validators=[DataRequired(), NumberRange(min=0)])
    categoria_id = SelectField('Categoría', coerce=int, validators=[DataRequired()])
    imagen = StringField('URL de la Imagen', validators=[DataRequired()])
    submit = SubmitField('Guardar')
