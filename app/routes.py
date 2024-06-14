from flask import render_template, flash, redirect, url_for, request, current_app, session, jsonify
from app import db, login_manager
from app.forms import RegistrationForm, LoginForm, AppointmentForm
from app.models import User, Service, Appointment
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
from flask_login import UserMixin, login_user, logout_user, login_required, current_user

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def get_available_times(date):
    now = datetime.now()
    start_time = datetime.strptime("08:00", "%H:%M").time()
    end_time = datetime.strptime("18:00", "%H:%M").time()
    interval = timedelta(hours=1)

    times = []
    current_time = datetime.combine(date, start_time)

    while current_time.time() <= end_time:
        # Não adicionar horários no passado
        if datetime.combine(date, current_time.time()) > now:
            times.append(current_time.time())
        current_time += interval

    appointments = Appointment.query.filter_by(data=date).all()
    booked_times = [appointment.hora for appointment in appointments]

    available_times = [time for time in times if time not in booked_times]

    return available_times

@current_app.route('/get_available_times/<date>', methods=['GET'])
@login_required
def get_available_times_route(date):
    date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    available_times = get_available_times(date_obj)
    return jsonify({'times': [time.strftime("%H:%M") for time in available_times]})

@current_app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.senha.data)
        user = User(nome=form.nome.data, email=form.email.data, senha=hashed_password, telefone=form.telefone.data)
        db.session.add(user)
        db.session.commit()
        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Cadastro', form=form)

@current_app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.senha, form.senha.data):
            login_user(user, remember=form.remember_me.data)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login ou senha incorretos.', 'danger')
    # Limpar mensagens flash apenas se redirecionado do logout ou registro
    if 'next' in request.args and (request.args['next'] == url_for('logout') or request.args['next'] == url_for('register')):
        session.pop('_flashes', None)
    return render_template('login.html', title='Login', form=form)

@current_app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('login', next=url_for('logout')))

@current_app.route('/dashboard')
@login_required
def dashboard():
    today = date.today()
    requested_date = request.args.get('date')
    if current_user.is_admin:
        if requested_date:
            date_obj = datetime.strptime(requested_date, '%Y-%m-%d').date()
            if date_obj < today:
                appointments = []  # Se a data é anterior a hoje, não mostrar agendamentos
            else:
                appointments = Appointment.query.filter(Appointment.data == date_obj).order_by(Appointment.data.asc(), Appointment.hora.asc()).all()
        else:
            appointments = Appointment.query.filter(Appointment.data >= today).order_by(Appointment.data.asc(), Appointment.hora.asc()).all()
    else:
        user_id = current_user.id
        appointments = Appointment.query.filter_by(user_id=user_id).filter(Appointment.data >= today).order_by(Appointment.data.asc(), Appointment.hora.asc()).all()

    return render_template('admin_dashboard.html' if current_user.is_admin else 'user_dashboard.html', title='Dashboard', appointments=appointments)


@current_app.route('/confirm_cancel/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
def confirm_cancel(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if request.method == 'POST':
        if appointment:
            db.session.delete(appointment)
            db.session.commit()
            flash('Agendamento cancelado com sucesso!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('confirm_cancel.html', title='Confirmar Cancelamento', appointment=appointment)

@current_app.route('/agendar', methods=['GET', 'POST'])
@login_required
def agendar():
    form = AppointmentForm()
    if form.data.data:
        form.hora.choices = [(t.strftime("%H:%M"), t.strftime("%H:%M")) for t in get_available_times(form.data.data)]
    if form.validate_on_submit():
        appointment = Appointment(user_id=current_user.id, service_id=form.servico.data, data=form.data.data, hora=form.hora.data)
        db.session.add(appointment)
        db.session.commit()
        flash('Agendamento realizado com sucesso!', 'success')
        appointment_data = form.data.data.strftime('%d/%m/%Y')
        appointment_hora = datetime.strptime(form.hora.data, '%H:%M').strftime('%H:%M')
        return redirect(url_for('confirmacao', data=appointment_data, hora=appointment_hora))
    return render_template('agendar.html', title='Agendar Serviço', form=form)

@current_app.route('/confirmacao')
@login_required
def confirmacao():
    data = request.args.get('data')
    hora = request.args.get('hora')
    return render_template('confirmacao.html', title='Confirmação de Agendamento', data=data, hora=hora)

@current_app.route('/lgpd')
def lgpd():
    return render_template('lgpd.html', title='Termos e Serviços - LGPD')

@current_app.route('/cancelar_agendamento/<int:appointment_id>', methods=['POST'])
@login_required
def cancelar_agendamento(appointment_id):
    return redirect(url_for('confirm_cancel', appointment_id=appointment_id))
