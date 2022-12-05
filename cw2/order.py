from flask import (Blueprint,
                   render_template,
                   redirect,
                   url_for,
                   request,
                   flash,
                   session,
                   g)
from models import Order, Bread, Client, Type
from exts import db
from .forms import AddForm, AddBreadForm, AddTypeForm
from decorators import sign_in_required
from sqlalchemy import or_
import datetime
import time

# Here, for administrative purposes, I've placed all the back-end code for the display page under the display blueprint
bp = Blueprint("order", __name__, url_prefix="/order")


# The page which display all assessments.
@bp.route('/display')
@sign_in_required
def display():
    un = g.baker.username
    order = Order.query.order_by(Order.join_time).filter(Order.baker_name == un).all()
    n = 0
    for i in order:
        n = n+1
    return render_template("order_display.html", order=order, n=n)


@bp.route('/display_reverse')
def display_reverse():
    un = g.baker.username
    order = Order.query.order_by(Order.join_time.desc()).filter(Order.baker_name == un).all()
    n = 0
    for i in order:
        n = n+1
    return render_template("order_display.html", order=order, n=n)


@bp.route('/bread_display')
@sign_in_required
def bread_display():
    bread = Bread.query.order_by(Bread.e_date).all()
    n = 0
    for i in bread:
        n = n+1
    return render_template("bread_display.html", bread=bread, n=n)


@bp.route('/bread_display_reverse')
@sign_in_required
def bread_display_reverse():
    bread = Bread.query.order_by(Bread.e_date.desc()).all()
    n = 0
    for i in bread:
        n = n+1
    return render_template("bread_display.html", bread=bread, n=n)


@bp.route('/client_display')
@sign_in_required
def client_display():
    client = Client.query.all()
    return render_template("client_display.html", client=client)


@bp.route('/type_display')
@sign_in_required
def type_display():
    type1 = Type.query.all()
    n = 0
    for i in type1:
        n = n+1
    return render_template("type_display.html", type=type1, n=n)


@bp.route('/order_add_dis')
@sign_in_required
def order_add_dis():
    bread = Bread.query.all()
    return render_template("order_add.html", bread=bread)


@bp.route('/delete_display')
@sign_in_required
def delete_display():
    order = Order.query.all()
    n = 0
    for i in order:
        n = n+1
    return render_template("order_delete.html", order=order, n=n)


@bp.route('/bread_delete_display')
@sign_in_required
def bread_delete_display():
    bread = Bread.query.all()
    n = 0
    for i in bread:
        n = n+1
    return render_template("bread_delete.html", bread=bread, n=n)


# Execute the operation of deleting.
@bp.route('/delete/<int:id>')
def delete(id):
    order = Order.query.filter_by(id=id)[0]
    db.session.delete(order)
    db.session.commit()
    return redirect(url_for('order.delete_display'))


# Execute the operation of bread deleting.
@bp.route('/bread_delete/<string:bread_name>')
def bread_delete(bread_name):
    bread = Bread.query.filter_by(bread_name=bread_name)[0]
    db.session.delete(bread)
    db.session.commit()
    return redirect(url_for('order.bread_delete_display'))


# Add the order
@bp.route('/order_add', methods=['GET', 'POST'])
@sign_in_required
def order_add():
    # Check whether its method is "get" or "post"
    n = 0
    n1 = 0
    un = g.baker.username
    if request.method == 'POST':
        form = AddForm(request.form)
        # Check whether it pass the validator
        bread = Bread.query.all()
        client = Client.query.all()

        if form.validate():
            bread_name = form.bread_name.data
            finish = form.finish.data
            client_id = form.client_id.data
            for i in bread:
                if i.bread_name == bread_name:
                    n = 1
            for i in client:
                # name>id
                if i.client_name == client_id:
                    n1 = 1
            if n == 0:
                flash("There is no such bread!Please add the bread first.")
                return redirect(url_for("order.order_add"))
            if n1 == 0:
                flash("There is no such client!Please add the client first.")
                return redirect(url_for("order.order_add"))
            assessment = Order(bread_name=bread_name, finish=finish, client_id=client_id, baker_name=un)
            db.session.add(assessment)
            db.session.commit()
            return redirect(url_for("order.display"))
        else:
            return redirect(url_for("order.order_add"))
    else:
        return render_template("order_add.html")


# Add the bread
@bp.route('/bread_add', methods=['GET', 'POST'])
@sign_in_required
def bread_add():
    # Check whether its method is "get" or "post"
    n = 0
    if request.method == 'POST':
        form = AddBreadForm(request.form)
        # Check whether it pass the validator
        t = Type.query.all()

        if form.validate():
            bread_name = form.bread_name.data
            m_date = form.m_date.data
            e_date = form.e_date.data
            type_name = form.type_name.data
            for i in t:
                if i.type_name == type_name:
                    n = 1
            if n == 0:
                flash("There is no such type!Please add the type first.")
                return redirect(url_for("order.bread_add"))
            assessment = Bread(bread_name=bread_name, m_date=m_date, e_date=e_date, type_name=type_name)
            db.session.add(assessment)
            db.session.commit()
            return redirect(url_for("order.bread_display"))
        else:
            return redirect(url_for("order.bread_add"))
    else:
        return render_template("bread_add.html")


# Add the type
@bp.route('/type_add', methods=['GET', 'POST'])
@sign_in_required
def type_add():
    # Check whether its method is "get" or "post"
    # n = 0
    if request.method == 'POST':
        form = AddTypeForm(request.form)
        # Check whether it pass the validator
        # t = Type.query.all()

        if form.validate():
            type_name = form.type_name.data
            assessment = Type(type_name=type_name)
            db.session.add(assessment)
            db.session.commit()
            return redirect(url_for("order.type_display"))
        else:
            return redirect(url_for("order.type_add"))
    else:
        return render_template("type_add.html")


# Execute the operation of searching order.(which in the top right corner of the page)
@bp.route('/search_order')
def search_order():
    select_type = request.args.get("select_type")
    search = request.args.get("search")
    n = 0
    if select_type == "order":
        order = Order.query.filter(or_(Order.bread_name.contains(search),
                                       Order.client_id.contains(search),
                                       Order.finish.contains(search),
                                       Order.join_time.contains(search)))
        for i in order:
            n = n+1
        return render_template('order_display.html', order=order, n=n)
    else:
        if select_type == "bread":
            bread1 = Order.query.filter(or_(Bread.e_date.contains(search),
                                            Bread.bread_name.contains(search),
                                            Bread.m_date.contains(search),
                                            Bread.type_name.contains(search)))
            for i in bread1:
                n = n+1
            return render_template('bread_display.html', bread=bread1, n=n)
        else:
            if select_type == "client":
                client = Client.query.filter(or_(Client.client_name.contains(search),
                                                 Client.phone.contains(search),
                                                 Client.address.contains(search)))
                for i in client:
                    n = n+1
                return render_template('client_display.html', client=client, n=n)


@bp.route('/order_edit/<int:id>', methods=['POST', 'GET'])
def order_edit(id):
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
                return redirect(url_for("order.order_edit", id=id))
            if n1 == 0:
                flash("There is no such client!Please add the client first.")
                return redirect(url_for("order.order_edit", id=id))
            db.session.commit()
            return redirect(url_for("order.delete_display"))
        else:
            flash("cc")
            return redirect(url_for("order.order_edit", order=order, id=id))
    else:
        return render_template('order_edit.html', order=order, id=id)
