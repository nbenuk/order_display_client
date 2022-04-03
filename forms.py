from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class OrderForm(FlaskForm):
    order_ref = StringField('Order ID', validators=[DataRequired(), Length(max=10)])
    submit = SubmitField('Submit')