from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# форма входа в аккаунт
class Form(FlaskForm):
    vuz = StringField('ВУЗ', validators=[DataRequired()])
    nup = StringField('Направление', validators=[DataRequired()])
    submit = SubmitField('Подготовить')