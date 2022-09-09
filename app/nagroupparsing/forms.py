from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL

from ..models import ParsingLog

class StartParseData(FlaskForm):
    """
    Form to start parse
    """
    parse_link = StringField('Link to master data', validators=[DataRequired(), URL()])
    submit = SubmitField('Загрузить')


