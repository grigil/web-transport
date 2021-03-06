from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, IntegerField, SubmitField, RadioField, FloatField, FieldList, FormField, DateTimeField, PasswordField, HiddenField
from wtforms.validators import Required, ValidationError, Email, EqualTo

from wtforms.fields.html5 import DateTimeLocalField

from datetime import datetime

from .models import User


def _required(form, field):
    #print(field, bool(not field.raw_data or not field.raw_data[0]))
    if not field.raw_data or not field.raw_data[0]:
        raise ValidationError('Field is required')


class MyForm(FlaskForm):
    class Meta:
        csrf = True
    submit = SubmitField('Ok')
    cancel = SubmitField('Cancel')
    form_name = 'form name'

class CSRF_Form(MyForm):
    pass

class MyFieldList(FieldList):
    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)
        self.clm_names = []
        self.table_name = ''
    


class LoginForm(FlaskForm):
    email = StringField('E-mail', validators = [Required(), Email()])
    password = PasswordField('passwprd', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)
    #submit = SubmitField('Log in')
    #form_name = "login"

    def validate(self):
        #initial_validation = super(LoginForm, self).validate()
        #if not initial_validation:
            #return False
        print('sup val')
        user = User.query.filter_by(email=self.email.data).first()
        if not user:
            #self.email.errors.append('Unknown email')
            return False
        print('log val', user.verify_password(self.password.data), self.password.data)
        if not user.verify_password(self.password.data):
            #self.password.errors.append('Invalid password')
            return False
        return True


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[Required()])
    email = StringField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required()])
    confirm = PasswordField('Verify password', validators=[Required(), EqualTo('password', message='Passwords must match')])
    remember_me = BooleanField('remember_me', default = False)
    submit = SubmitField('Log in')


    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append("Username already registered")
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True




class FClients_delivery(MyForm):
    form_name = "????????????????"

class FClients_finances(MyForm):
    form_name = "??????????????"

class FClients_rate_inner(FlaskForm):
    class Meta:
        csrf_token = True
    product_group = StringField('???????????? ??????????????')
    product_group_id = HiddenField('Id ???????????? ??????????????')
    rate = FloatField('????????????')
    currency = SelectField('????????????', coerce=int)


class FClients_product_inner(FlaskForm):
    class Meta:
        csrf_token = True
    checkbox = BooleanField('??????????????????')
    product_name = StringField('??????????')
    product_id = HiddenField('Id ????????????')
    quanity = IntegerField('??????-???? ???? ??????????????')


class FClients_rates_and_products(MyForm):
    date_start = DateTimeLocalField('???????? ????????????', default=datetime.today, format='%Y-%m-%dT%H:%M')
    client_id = HiddenField('Id ??????????????', default=0)
    rates = MyFieldList(FormField(FClients_rate_inner))
    products = MyFieldList(FormField(FClients_product_inner))
    comment = StringField('??????????????????????')
    form_name = "???????????? ?? ????????????"


class FClients(CSRF_Form):
    brand = StringField('????????????????????????', validators = [_required])
    Fname = StringField('??????????????', validators = [_required])
    Iname = StringField('??????', validators = [_required])
    Oname = StringField('????????????????', validators = [_required])
    phone = StringField('??????????????', validators = [_required])
    email = StringField('E-mail', validators = [_required])
    comment = StringField('??????????????????????', validators = [_required])
    rates = MyFieldList(FormField(FClients_rate_inner))
    products = MyFieldList(FormField(FClients_product_inner))
    form_name = "???????????????? ??????????????"

#grish dolbaeb
class FFinances(CSRF_Form):
    clients = StringField('????????????????????????', validators = [_required])
    Progress_sum = IntegerField('????????????????????????', validators = [_required])
    Now_sum = IntegerField('????????????????????????', validators = [_required])
    Paid = IntegerField('????????????????????????', validators = [_required])
    Overall = IntegerField('????????????????????????', validators = [_required])
    Days = IntegerField('????????????????????????', validators = [_required])


class FProducts(CSRF_Form):
    name = StringField('????????????????????????', validators = [_required])
    group = SelectField('???????????? ??????????????', validators = [_required], coerce=int)
    quanity = IntegerField('??????-???? ???? ??????????????', validators = [_required])
    form_name = "???????????????? ??????????"

class FProduct_groups(CSRF_Form):
    name = StringField('???????????? ??????????????', validators = [_required])
    form_name = "???????????????? ???????????? ??????????????"


class FCar_types(CSRF_Form):
    car_type = StringField('?????? ????????????', validators = [_required])
    form_name = "???????????????? ?????? ????????????"


class FCar_numbers(CSRF_Form):
    number = StringField('?????????? ????????????', validators = [_required])
    car_type = SelectField('?????? ????????????', validators = [_required], coerce=int)
    form_name = "???????????????? ????????????"

class FExchange_rates(CSRF_Form):
    date = DateTimeLocalField('????????', default=datetime.today, format='%Y-%m-%dT%H:%M')
    currency_dollar = FloatField('???????? ??????????????', validators = [_required])
    currency_euro = FloatField('???????? ????????', validators = [_required])
    comment = StringField('??????????????????????', validators = [_required])
    author = StringField('?????????? ??????????????????', validators = [_required])
    form_name = "???????????????? ???????? ??????????"

class FPrepared_cars(CSRF_Form):
    car_id = SelectField('?????????? ????????????', validators = [_required], coerce=int)
    date_in = DateTimeLocalField('???????? ??????????????????????', default=datetime.today, format='%Y-%m-%dT%H:%M')
    form_name = "???????????????? ????????????"


class FCar_client_products_inner(FlaskForm):
    class Meta:
        csrf_token = True
    product_name = StringField('??????????')
    product_id = HiddenField('Id ????????????')
    quanity_default = StringField('??????-???? ???? ??????????????')
    quanity = FloatField('??????-????')
    volume = StringField('??????????')
    price = FloatField('??????????')


class FCar_client_rates_inner(FlaskForm):
    class Meta:
        csrf_token = True
    product_group = StringField('???????????? ??????????????')
    product_group_id = HiddenField('Id ???????????? ??????????????')
    rate = StringField('????????????')
    quanity = FloatField('??????-????')
    result = SelectField('??????????')



class FPrepared_car_clients(CSRF_Form):
    client = SelectField('????????????', validators = [_required], coerce=int)
    #rates = MyFieldList(FormField(FCar_client_rates_inner))
    #products = MyFieldList(FormField(FCar_client_products_inner))
    form_name = "???????????????? ??????????????"

class FPrepared_car_clients_inner(CSRF_Form):
    rates = MyFieldList(FormField(FCar_client_rates_inner))
    products = MyFieldList(FormField(FCar_client_products_inner))
    form_name = "???????????? ?? ????????????"


