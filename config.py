# All the configuration items are in this file
# JSON_AS_ASCII = False

# Database Configuration
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'yummy_bakery'
USERNAME = 'root'
PASSWORD = '123456'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True

MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_DEBUG = True
MAIL_USERNAME = "2802996331@qq.com"
MAIL_PASSWORD = "izgfzxmikvcqdgei"
MAIL_DEFAULT_SENDER = "2802996331@qq.com"


