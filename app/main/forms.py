
from flask import request
from flask_wtf import FlaskForm
from flask_babel import _, lazy_gettext as _l
from flask_wtf.form import _Auto
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError
from app import db
from app.models import User

import sqlalchemy as sa

class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('About me'), validators=[Length(min=0, max=256)])
    submit = SubmitField(_l('Submit'))

    # проверка имени пользователя в форме редактирования профиля. 
    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = db.session.scalar(sa.select(User).where(User.username == self.username.data))
            if user is not None:
                raise ValidationError(_('Please use a different username.'))
            
# пустая форма для подписки и отмены подписки
class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

# форма опубликования поста
class PostForm(FlaskForm):
    post = TextAreaField(_l('Ваше сообщение:'), validators=[DataRequired(), Length(min=10, max=150)])
    submit = SubmitField(_l('Submit'))

# форма поиска
class SearchForm(FlaskForm):
    q = StringField(_l('Search'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
            if 'meta' not in kwargs:
                kwargs['meta'] = {'csrf': False}
        super(SearchForm, self).__init__(*args, **kwargs)