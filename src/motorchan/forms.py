# -*- coding: utf-8 -*-
from wtforms import fields, validators
from tornadotools import forms


required_validator = validators.required(u'Обязательное поле.')


class LoginForm(forms.Form):
    username = fields.StringField(u'Логин', [required_validator])
    password = fields.PasswordField(u'Пароль', [required_validator])


class BoardForm(forms.Form):
    slug = fields.StringField(u'Идентификатор', [required_validator])
    name = fields.StringField(u'Имя', [required_validator])


class PostForm(forms.Form):
    name = fields.StringField(u'Имя')
    email = fields.StringField(u'Email')
    body = fields.TextField(u'Тело', [required_validator])
    image = fields.FileField(u'Изображение')


class ThreadForm(PostForm):
    image = fields.FileField(u'Изображение', [required_validator])