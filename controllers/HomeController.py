from flask import render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from models.User import Users

class HomeController():
    def index():
        return render_template('index.html')

    def login():
        return render_template('signin.html')

    def register():
        return render_template('signup.html')

    def signup():
        name_input = request.form.get('name')
        email_input = request.form.get('email')
        password_input = request.form.get('password')
    
        # Verificar se já existe o email no bd
        user = Users.query.filter_by(email=email_input).first()
        if user:
            flash('Este e-mail já existe', 'error')
            return redirect('/register')
    
        new_user = Users(
            name=name_input,
            email=email_input,
            password=generate_password_hash(password_input)
        )
        db.session.add(new_user)
        db.session.commit()
    
        flash('Usuário criado com sucesso', 'success')
        return redirect('/login')

    def signin():
        email_input = request.form.get('email')
        password_input = request.form.get('password')
    
        # Verificar se existe um usuário com o email
        user = Users.query.filter_by(email=email_input).first()
        if not user:
            flash('E-mail não encontrado', 'error')
            return redirect('/login')
    
        # Verificar se senha está correta
        if not check_password_hash(user.password, password_input):
            flash('Senha incorreta', 'error')
            return redirect('/login')
    
        # Guardar usuário na sessão
        session['user_id'] = user.id
    
        flash(f'Olá, {user.name}', 'info')
        return redirect('/dashboard')

    def logout():
        session.pop('user_id', None)
        return redirect('/login')
