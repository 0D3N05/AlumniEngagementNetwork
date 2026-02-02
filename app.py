from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from sqlalchemy import or_ 
from datetime import datetime

app = Flask(__name__)

# --- CONFIGURATION ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alumni.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecretkey' 

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- DATABASE MODELS ---

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(20), default='Student')
    
    # Profile Fields
    full_name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    headline = db.Column(db.String(150), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    skills = db.Column(db.String(200), nullable=True)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    author_name = db.Column(db.String(50), default="Syed (You)")

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    date_str = db.Column(db.String(20), nullable=False)
    time_str = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)

class EventRegistration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)

class EventFeedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='feedbacks')
    event = db.relationship('Event', backref='feedbacks')

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_messages')

class Mentorship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mentor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='Pending')
    
    student = db.relationship('User', foreign_keys=[student_id], backref='mentorship_requests_sent')
    mentor = db.relationship('User', foreign_keys=[mentor_id], backref='mentorship_requests_received')

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    job_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    posted_date = db.Column(db.DateTime, default=datetime.utcnow)
    
class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    applied_date = db.Column(db.DateTime, default=datetime.utcnow)

# --- ROUTES ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required  # <--- FIXED
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required  # <--- FIXED
def home():
    all_posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('student/home.html', active_page='home', posts=all_posts, user=current_user)

@app.route('/create_post', methods=['POST'])
@login_required  # <--- FIXED
def create_post():
    post_content = request.form.get('content')
    if post_content:
        new_post = Post(content=post_content, author_name=current_user.username)
        db.session.add(new_post)
        db.session.commit()
    return redirect(url_for('home'))

@app.route('/notifications')
@login_required  # <--- FIXED
def notifications():
    all_notifs = Notification.query.order_by(Notification.timestamp.desc()).all()
    return render_template('student/notifications.html', active_page='notifications', notifications=all_notifs)

@app.route('/events')
@login_required  # <--- FIXED
def events():
    all_events = Event.query.all()
    my_registrations = EventRegistration.query.filter_by(user_id=current_user.id).all()
    registered_ids = [reg.event_id for reg in my_registrations]
    return render_template('student/events.html', active_page='events', events=all_events, registered_ids=registered_ids)

@app.route('/register/<int:event_id>')
@login_required  # <--- FIXED
def register_event(event_id):
    exists = EventRegistration.query.filter_by(user_id=current_user.id, event_id=event_id).first()
    if not exists:
        new_reg = EventRegistration(user_id=current_user.id, event_id=event_id)
        db.session.add(new_reg)
        db.session.commit()
        flash('Successfully registered!')
    return redirect(request.referrer or url_for('events'))

@app.route('/unregister/<int:event_id>')
@login_required  # <--- FIXED
def unregister_event(event_id):
    reg = EventRegistration.query.filter_by(user_id=current_user.id, event_id=event_id).first()
    if reg:
        db.session.delete(reg)
        db.session.commit()
        flash('Registration cancelled.', 'info')
    return redirect(request.referrer or url_for('events'))

@app.route('/messages')
@login_required  # <--- FIXED
def messages():
    sent_to = [m.receiver_id for m in Message.query.filter_by(sender_id=current_user.id).all()]
    received_from = [m.sender_id for m in Message.query.filter_by(receiver_id=current_user.id).all()]
    contact_ids = set(sent_to + received_from)
    contacts = User.query.filter(User.id.in_(contact_ids)).all()
    if not contacts:
        contacts = User.query.filter(User.id != current_user.id).all()
    return render_template('student/messages.html', active_page='messages', contacts=contacts)

@app.route('/chat/<int:user_id>', methods=['GET', 'POST'])
@login_required  # <--- FIXED
def chat(user_id):
    other_user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        body = request.form.get('body')
        if body:
            msg = Message(sender_id=current_user.id, receiver_id=other_user.id, body=body)
            db.session.add(msg)
            db.session.commit()
        return redirect(url_for('chat', user_id=user_id))
    
    conversation = Message.query.filter(
        or_(
            (Message.sender_id == current_user.id) & (Message.receiver_id == other_user.id),
            (Message.sender_id == other_user.id) & (Message.receiver_id == current_user.id)
        )
    ).order_by(Message.timestamp.asc()).all()
    return render_template('student/chat.html', other_user=other_user, messages=conversation)

@app.route('/jobs')
@login_required  # <--- FIXED
def jobs():
    all_jobs = Job.query.order_by(Job.posted_date.desc()).all()
    my_apps = JobApplication.query.filter_by(user_id=current_user.id).all()
    applied_ids = [app.job_id for app in my_apps]
    return render_template('student/jobs.html', active_page='jobs', jobs=all_jobs, applied_ids=applied_ids)

@app.route('/job/<int:job_id>')
@login_required  # <--- FIXED
def job_details(job_id):
    job = Job.query.get_or_404(job_id)
    application = JobApplication.query.filter_by(user_id=current_user.id, job_id=job_id).first()
    is_applied = True if application else False
    return render_template('student/component/job_details.html', job=job, is_applied=is_applied)

@app.route('/apply/<int:job_id>')
@login_required  # <--- FIXED
def apply_job(job_id):
    existing = JobApplication.query.filter_by(user_id=current_user.id, job_id=job_id).first()
    if not existing:
        new_app = JobApplication(user_id=current_user.id, job_id=job_id)
        db.session.add(new_app)
        db.session.commit()
        flash('Application sent successfully!', 'success')
    return redirect(request.referrer or url_for('jobs'))

@app.route('/mentorship')
@login_required  # <--- FIXED (This prevents the crash)
def mentorship():
    alumni_list = User.query.filter_by(role='Alumni').all()
    my_requests = Mentorship.query.filter_by(student_id=current_user.id).all()
    request_status = {req.mentor_id: req.status for req in my_requests}
    return render_template('student/mentorship.html', active_page='mentorship', alumni_list=alumni_list, request_status=request_status)

@app.route('/mentor/<int:mentor_id>')
@login_required  # <--- FIXED
def mentor_details(mentor_id):
    mentor = User.query.get_or_404(mentor_id)
    req = Mentorship.query.filter_by(student_id=current_user.id, mentor_id=mentor_id).first()
    status = req.status if req else None 
    return render_template('student/component/mentor_details.html', mentor=mentor, status=status)

@app.route('/edit_profile', methods=['POST'])
@login_required  # <--- FIXED
def edit_profile():
    if request.method == 'POST':
        current_user.full_name = request.form.get('full_name')
        current_user.email = request.form.get('email')
        current_user.phone = request.form.get('phone')
        current_user.address = request.form.get('address')
        current_user.headline = request.form.get('headline')
        current_user.location = request.form.get('location')
        current_user.bio = request.form.get('bio')
        current_user.skills = request.form.get('skills')
        db.session.commit()
        flash('Profile updated successfully!', 'success')
    return redirect(url_for('profile'))

@app.route('/request_mentor/<int:mentor_id>')
@login_required  # <--- FIXED
def request_mentor(mentor_id):
    existing = Mentorship.query.filter_by(student_id=current_user.id, mentor_id=mentor_id).first()
    if not existing:
        new_req = Mentorship(student_id=current_user.id, mentor_id=mentor_id)
        db.session.add(new_req)
        db.session.commit()
        flash('Mentorship request sent!', 'success')
    return redirect(request.referrer or url_for('mentorship'))

@app.route('/cancel_request/<int:mentor_id>')
@login_required  # <--- FIXED
def cancel_request(mentor_id):
    req = Mentorship.query.filter_by(student_id=current_user.id, mentor_id=mentor_id).first()
    if req:
        db.session.delete(req)
        db.session.commit()
        flash('Mentorship request cancelled.', 'info')
    return redirect(request.referrer or url_for('mentorship'))

@app.route('/event/<int:event_id>')
@login_required  # <--- FIXED
def event_details(event_id):
    event = Event.query.get_or_404(event_id)
    registration = EventRegistration.query.filter_by(user_id=current_user.id, event_id=event_id).first()
    is_registered = True if registration else False
    existing_feedback = EventFeedback.query.filter_by(user_id=current_user.id, event_id=event_id).first()
    all_reviews = EventFeedback.query.filter_by(event_id=event_id).order_by(EventFeedback.timestamp.desc()).all()
    return render_template('student/component/event_details.html', event=event, is_registered=is_registered, my_feedback=existing_feedback, reviews=all_reviews)

@app.route('/submit_feedback/<int:event_id>', methods=['POST'])
@login_required  # <--- FIXED
def submit_feedback(event_id):
    existing = EventFeedback.query.filter_by(user_id=current_user.id, event_id=event_id).first()
    if existing:
        flash('You have already reviewed this event.', 'warning')
        return redirect(url_for('event_details', event_id=event_id))
    rating = request.form.get('rating')
    comment = request.form.get('comment')
    if rating:
        new_feedback = EventFeedback(user_id=current_user.id, event_id=event_id, rating=int(rating), comment=comment)
        db.session.add(new_feedback)
        db.session.commit()
        flash('Thank you for your feedback!', 'success')
    return redirect(url_for('event_details', event_id=event_id))

@app.route('/profile')
@login_required  # <--- FIXED
def profile():
    my_posts = Post.query.filter_by(author_name=current_user.username).order_by(Post.timestamp.desc()).all()
    event_count = EventRegistration.query.filter_by(user_id=current_user.id).count()
    job_count = JobApplication.query.filter_by(user_id=current_user.id).count()
    mentor_count = Mentorship.query.filter_by(student_id=current_user.id).count()
    return render_template('student/profile.html', active_page='profile', user=current_user, posts=my_posts, event_count=event_count, job_count=job_count, mentor_count=mentor_count)

@app.route('/dashboard')
@login_required  # <--- FIXED
def dashboard():
    event_count = EventRegistration.query.filter_by(user_id=current_user.id).count()
    job_count = JobApplication.query.filter_by(user_id=current_user.id).count()
    mentor_reqs = Mentorship.query.filter_by(student_id=current_user.id).all()
    active_mentors = sum(1 for m in mentor_reqs if m.status == 'Accepted')
    recent_notifs = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.timestamp.desc()).limit(5).all()
    return render_template('student/dashboard.html', active_page='dashboard', event_count=event_count, job_count=job_count, active_mentors=active_mentors, notifications=recent_notifs)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5500)