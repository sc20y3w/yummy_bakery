from flask import (Blueprint,
                   render_template,
                   request,
                   url_for,
                   redirect,
                   jsonify,
                   session,
                   flash)
from models import Baker, EmailCaptchaModel
from exts import mail, db
from flask_mail import Message
from datetime import datetime
from .forms import RegisterForm, SignInForm
import string
import random

bp = Blueprint("baker", __name__, url_prefix="/baker")


# Send captcha code
@bp.route('/captcha', methods=['POST'])
def get_captcha():
    # GET
    email = request.form.get("email")
    letters = string.ascii_letters+string.digits
    captcha = "".join(random.sample(letters, 4))
    if email:
        message = Message(
            subject= "validation",
            recipients=[email],
            body=f"code:{captcha}"
        )
        mail.send(message)
        captcha_q = EmailCaptchaModel.query.filter_by(email=email).first()
        if captcha_q:
            captcha_q.captcha = captcha
            captcha_q.create_time = datetime.now()
            db.session.commit()
        else:
            captcha_q = EmailCaptchaModel(email=email, captcha=captcha)
            db.session.add(captcha_q)
            db.session.commit()
        return jsonify({"code": 200})  # success
    else:
        return jsonify({"code": 400, "message": "Please enter the email address"})  # fail


@bp.route('/baker_register', methods=['GET', 'POST'])
def baker_register():
    if request.method == 'POST':
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data

            baker = Baker(email=email, username=username, password=password)
            db.session.add(baker)
            db.session.commit()
            return redirect(url_for("sign_in"))
        else:
            return redirect(url_for("sign_up"))
    else:
        return render_template("sign_up.html")


@bp.route('/baker_sign_in', methods=['GET', 'POST'])
def baker_sign_in():
    if request.method == 'POST':
        form = SignInForm(request.form)
        if form.validate():
            username = form.username.data
            password = form.password.data
            baker = Baker.query.filter_by(username=username).first()
            if baker and baker.password == password:
                session['baker_username'] = baker.username
                return redirect(url_for("home"))
            else:
                flash("The user name or password is incorrect.")
                return redirect(url_for("baker.baker_sign_in"))
        else:
            flash("The user name or password format is incorrect.")
            return redirect(url_for("baker.baker_sign_in"))
    else:
        return render_template("sign_in.html")


@bp.route('/sign_out', methods=['GET', 'POST'])
def sign_out():
    session.clear()  # Clear all data
    return redirect(url_for('baker.baker_sign_in'))


