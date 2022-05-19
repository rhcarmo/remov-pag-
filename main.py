from flask import Flask
from database import db
from controllers.HomeController import HomeController
from controllers.ExpenseController import ExpenseController

###### CONFIGURACOES ######
app = Flask('app')
app.config['SECRET_KEY'] = 'qEChL7R3SpF72cEA'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db.init_app(app)

###### ROTAS ######
@app.route('/')
def index():
  return HomeController.index()

@app.route('/login')
def login():
  return HomeController.login()

@app.route('/register')
def register():
  return HomeController.register()

@app.route('/signup', methods=['POST'])
def signup():
  return HomeController.signup()

@app.route('/signin', methods=['POST'])
def signin():
  return HomeController.signin()

@app.route('/logout')
def logout():
  return HomeController.logout()

@app.route('/dashboard')
def dashboard():
  return ExpenseController.index()

@app.route('/expenses/create')
def expenses_create():
  return ExpenseController.create()

@app.route('/expenses/edit/<int:id>')
def expenses_edit(id):
  return ExpenseController.edit(id)

@app.route('/expenses/store', methods=['POST'])
def expenses_store():
  return ExpenseController.store()

@app.route('/expenses/update/<int:id>', methods=['POST'])
def expenses_update(id):
  return ExpenseController.update(id)

@app.route('/expenses/pay/<int:id>')
def expenses_pay(id):
  return ExpenseController.pay(id)

@app.route('/expenses/unpay/<int:id>')
def expenses_unpay(id):
  return ExpenseController.unpay(id)

###### INICIALIZACAO ######
with app.app_context():
  db.create_all()

if __name__ == '__main__':
  app.run(host='0.0.0.0')