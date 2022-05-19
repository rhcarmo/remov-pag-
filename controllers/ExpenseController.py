from flask import render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from database import db
from models.User import Users
from models.Expense import Expenses

class ExpenseController():
    def index():
        if 'user_id' not in session:
            flash('Faça o login novamente', 'error')
            return redirect('/login')

        today = datetime.now().date()
        user = Users.query.filter_by(id=session['user_id']).first()
        expenses = Expenses.query.filter_by(user_id=session['user_id']).order_by('due_date').all()
        return render_template('expenses/index.html', user=user, expenses=expenses, today=today)

    def create():
        if 'user_id' not in session:
            flash('Faça o login novamente', 'error')
            return redirect('/login')

        user = Users.query.filter_by(id=session['user_id']).first()
        return render_template('expenses/create.html', user=user)

    def edit(id):
        if 'user_id' not in session:
            flash('Faça o login novamente', 'error')
            return redirect('/login')

        user = Users.query.filter_by(id=session['user_id']).first()
        expense = Expenses.query.filter_by(id=id).first()

        if not expense or expense.user_id != session['user_id']:
            flash('Despesa não encontrada', 'error')
            return redirect('/dashboard')

        return render_template('expenses/edit.html', user=user, expense=expense)

    def store():
        if 'user_id' not in session:
            flash('Faça o login novamente', 'error')
            return redirect('/login')

        title = request.form.get('title')
        value = request.form.get('value')
        due_date = datetime.strptime(request.form.get('due_date'), '%Y-%m-%d').date()
    
        new_expense = Expenses(
            title=title,
            value=value,
            due_date=due_date,
            paid=False,
            user_id=session['user_id']
        )
        db.session.add(new_expense)
        db.session.commit()
    
        flash('Despesa criada com sucesso', 'success')
        return redirect('/dashboard')

    def update(id):
        if 'user_id' not in session:
            flash('Faça o login novamente', 'error')
            return redirect('/login')

        expense = Expenses.query.filter_by(id=id).first()

        if not expense or expense.user_id != session['user_id']:
            flash('Despesa não encontrada', 'error')
            return redirect('/dashboard')

        expense.title = request.form.get('title')
        expense.value = request.form.get('value')
        expense.due_date = datetime.strptime(request.form.get('due_date'), '%Y-%m-%d').date()
    
        flash('Despesa editada com sucesso', 'success')
        return redirect('/dashboard')

    def pay(id):
        if 'user_id' not in session:
            flash('Faça o login novamente', 'error')
            return redirect('/login')

        expense = Expenses.query.filter_by(id=id).first()

        if not expense or expense.user_id != session['user_id']:
            flash('Despesa não encontrada', 'error')
            return redirect('/dashboard')

        expense.paid=True
        db.session.commit()
    
        flash('Despesa paga com sucesso', 'success')
        return redirect('/dashboard')

    def unpay(id):
        if 'user_id' not in session:
            flash('Faça o login novamente', 'error')
            return redirect('/login')

        expense = Expenses.query.filter_by(id=id).first()

        if not expense or expense.user_id != session['user_id']:
            flash('Despesa não encontrada', 'error')
            return redirect('/dashboard')

        expense.paid=False
        db.session.commit()

        flash('Despesa não paga', 'success')
        return redirect('/dashboard')
