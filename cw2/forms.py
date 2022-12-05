import wtforms
from wtforms.validators import length, EqualTo, email, data_required, regexp
from models import EmailCaptchaModel, Baker


class SignInForm(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=3, max=20)])
    password = wtforms.StringField(validators=[length(min=6, max=20)])


class RegisterForm(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=3, max=20)])
    email = wtforms.StringField(validators=[email()])
    captcha = wtforms.StringField(validators=[length(min=4, max=4)])
    password = wtforms.StringField(validators=[length(min=6, max=20)])
    password_confirm = wtforms.StringField(validators=[EqualTo("password")])

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_q = EmailCaptchaModel.query.filter_by(email=email).first()
        if not captcha_q or captcha_q.captcha.lower() != captcha.lower():
            raise wtforms.ValidationError("The captcha code is wrong")

    def validate_email(self, field):
        email = field.data
        baker = Baker.query.filter_by(email=email).first()
        if baker:
            raise wtforms.ValidationError("The email address has been registered.")


# Form validation to see if the input is formatted, otherwise the add page will be cleared
class AddForm(wtforms.Form):
    bread_name = wtforms.SearchField(validators=[length(min=1, max=30)])
    finish = wtforms.SearchField(validators=[data_required(), regexp('True|true|TRUE|False|false|FALSE', 0,
                                                                     'Invalid status')])
    # You must write the right module name, otherwise it will clear the add page, and you need to rewrite it.
    client_id = wtforms.SearchField(validators=[data_required()])


# Form validation to see if the input is formatted, otherwise the add page will be cleared
class AddBreadForm(wtforms.Form):
    bread_name = wtforms.SearchField(validators=[length(min=1, max=30)])
    m_date = wtforms.SearchField(validators=[data_required()])
    # You must write the right module name, otherwise it will clear the add page, and you need to rewrite it.
    e_date = wtforms.SearchField(validators=[data_required()])
    type_name = wtforms.SearchField(validators=[data_required()])


# Form validation to see if the input is formatted, otherwise the add page will be cleared
class AddTypeForm(wtforms.Form):
    type_name = wtforms.SearchField(validators=[length(min=1, max=30)])
