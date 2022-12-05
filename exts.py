# This file was written because without it, the application would jump again and again
# between form and models.py and app.py.
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

db = SQLAlchemy()

mail = Mail()
