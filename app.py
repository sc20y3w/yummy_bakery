import requests.cookies
from flask import Flask, render_template, Response, request, session, g, flash, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from cw2.forms import AddForm
from decorators import sign_in_required
from models import Baker, Bread, Type, Order, Client
from cw2 import baker_bp
from cw2 import order_bp

from exts import db, mail
import config
app = Flask(__name__)
app.config.from_object(config)
app.register_blueprint(baker_bp)
app.register_blueprint(order_bp)


# Secret key
app.config['SECRET_KEY'] = "123456"
# Bind the app to bd
db.init_app(app)
mail.init_app(app)


migrate = Migrate(app, db)


# Test whether the database is connected successfully
# with app.app_context():
#     with db.engine.connect() as conn:
#         rs = conn.execute("select 1")
#         print(rs.fetchone())


@app.route("/type/add")
def add_type():
    type = Type(type_name="pancake")
    db.session.add(type)
    # submit operation
    db.session.commit()
    return "Add successful"

# Test whether the database is connected successfully
@app.route("/baker/add")
def add_baker():
    # Add data
    baker = Baker(username="Carrie", password="123456", email="sc20y3w@leeds.ac.uk")
    db.session.add(baker)
    #
    bread = Bread(bread_name="pancake", m_date="2022-11-07", e_date="2022-11-08")
    # type = Type(type_name="pancake")
    bread1 = Bread(bread_name="pancake1", m_date="2022-11-07", e_date="2022-11-08")
    # type = Type(type_name="pancake")
    type = Type(type_name="pancake")
    bread.type = type
    bread1.type = type
    db.session.add(bread)
    db.session.add(bread1)
    #
    order = Order(finish="false")
    order1 = Order(finish="true")
    client = Client(client_name="ccc", phone="13842867505", address="T156020")
    order.bread = bread
    order.client = client
    order1.bread = bread1
    order1.client = client
    db.session.add(order)
    db.session.add(order1)
    # submit operation
    db.session.commit()
    return "Add successful"


@app.route("/baker/add1")
def add1_baker():
    order = Order(bread_name="pancake", client_id="ccc", finish="False", baker_name="111111")
    db.session.add(order)
    db.session.commit()
    return "Add successful"

@app.route('/')
def home():
    return render_template("home.html")
@app.route('/u11/<int:id>', methods=['POST', 'GET'])
def u11(id):
    order = Order.query.filter_by(id=id)[0]
    n = 0
    n1 = 0
    if request.method == 'POST':
        form = AddForm(request.form)
        bread = Bread.query.all()
        client = Client.query.all()
        if form.validate():
            order.bread_name = form.bread_name.data
            order.client_id = form.client_id.data
            order.finish = form.finish.data
            for i in bread:
                if i.bread_name == order.bread_name:
                    n = 1
            for i in client:
                # name>id
                if i.client_name == order.client_id:
                    n1 = 1
            if n == 0:
                flash("There is no such bread!Please add the bread first.")
                return redirect(url_for("u11", id=id))
            if n1 == 0:
                flash("There is no such client!Please add the client first.")
                return redirect(url_for("u11", id=id))
            db.session.commit()
            return redirect(url_for("order.delete_display"))
        else:
            flash("cc")
            return redirect(url_for("u11", order=order, id=id))
    else:
        return render_template('11.html', order=order, id=id)


@app.route('/base')
def base2():
    return render_template("base.html")
@app.route('/sign_in')
def sign_in():
    return render_template("sign_in.html")
@app.route('/sign_up')
def sign_up():
    return render_template("sign_up.html")
@app.route('/order_add')
@sign_in_required
def order_add():
    return render_template("order_add.html")
@app.route('/delete')
@sign_in_required
def delete():
    return render_template("order_delete.html")
@app.route('/set_cookie')
def set_cookie():
    response = Response("set cookie")
    response.set_cookie("baker_id","xxx")
    return response
@app.route('/get_cookie')
def get_cookie():
    baker_id = request.cookies.get("baker_id")
    print("baker_id:",baker_id)
    return "get"
@app.route('/set_session')
def set_session():
    session["username"] = "yummy"
    return "get"
@app.route('/get_session')
def get_session():
    username = session.get('username')
    print("baker_id:", username)
    return "get"


@app.before_request
def before_request():
    baker_username = session.get("baker_username")
    if baker_username:
        try:
            baker = Baker.query.get(baker_username)
            # g is the global variable to which baker is bound
            g.baker = baker
        except:
            g.baker = None

# When the request is successful -> before_request -> View function -> Return to template -> context_processor
@app.context_processor
def context_processor():
    if hasattr(g, "baker"):
        return {"baker": g.baker}
    else:
        return {}


with app.app_context():
    db.create_all()
if __name__ == '__main__':
    app.run()
