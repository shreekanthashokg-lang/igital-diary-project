"""
MINI PRACTICE PROJECT DIGITAL DIARY 🎓
Flask + SQLAlchemy Web Application
STUDENTS DIGITAL DIARY MANAGEMENT
"""
print("=" * 70)
print("DIGITAL DIARY - MINI PROJECT")
print("Flask Web Application with Database")
print("=" * 70)

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import json

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'college-project-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///digital_diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ======== CONTEXT PROCESSOR ========
@app.context_processor
def inject_user():
    """Make current_user available as 'user' in all templates"""
    return dict(user=current_user)

print("✅ Flask application initialized")

# ==================== DATABASE MODELS ====================

class User(UserMixin, db.Model):
    """User model for authentication"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationship to diary entries
    entries = db.relationship('DiaryEntry', backref='author', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class DiaryEntry(db.Model):
    """Diary entry model"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    mood = db.Column(db.String(20), default='neutral')
    entry_date = db.Column(db.Date, nullable=False)
    weather = db.Column(db.String(50))
    location = db.Column(db.String(100))
    tags = db.Column(db.String(200))
    is_private = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

print("✅ Database models defined")

# ==================== HELPER FUNCTIONS ====================

def get_mood_emoji(mood):
    """Get emoji for mood"""
    emoji_map = {
        'happy': '😊',
        'excited': '🤩',
        'calm': '😌',
        'neutral': '😐',
        'sad': '😢',
        'angry': '😠',
        'tired': '😴'
    }
    return emoji_map.get(mood, '😐')

def get_mood_color(mood):
    """Get CSS class for mood"""
    color_map = {
        'happy': 'success',
        'excited': 'info',
        'calm': 'primary',
        'neutral': 'secondary',
        'sad': 'warning',
        'angry': 'danger',
        'tired': 'dark'
    }
    return color_map.get(mood, 'secondary')

def create_sample_data():
    """Create sample data for demonstration"""
    # Check if we already have users
    if User.query.count() == 0:
        print("📊 Creating sample data...")
        
        # Create demo user
        demo_user = User(
            username='demo_student',
            email='student@college.edu',
            full_name='College Student'
        )
        demo_user.set_password('password123')
        db.session.add(demo_user)
        
        # Create admin user
        admin_user = User(
            username='admin',
            email='admin@diary.com',
            full_name='System Administrator'
        )
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        
        db.session.commit()
        
        # Create sample entries
        sample_entries = [
            {
                'user_id': demo_user.id,
                'title': 'First Day of College Project',
                'content': """Today marks the beginning of my Digital Diary project development! 🎉

I decided to create a web-based diary application using Flask and SQLAlchemy. The goal is to build a fully functional application with:

✅ User Authentication
✅ CRUD Operations
✅ Mood Tracking
✅ Tagging System
✅ Responsive Design

I started by setting up the Flask environment and creating the basic folder structure. The database models for User and DiaryEntry are now ready.

Looking forward to implementing more features tomorrow!""",
                'mood': 'excited',
                'entry_date': datetime.now().date(),
                'weather': 'Sunny',
                'location': 'College Computer Lab',
                'tags': 'college,project,flask,python',
                'is_private': False
            },
            {
                'user_id': demo_user.id,
                'title': 'Database Schema Design',
                'content': """Spent the day designing the database schema. Key decisions:

1. **Users Table** - Stores user credentials and profile info
2. **Diary Entries Table** - Main content with foreign key to users
3. **Added Features:**
   - Mood tracking with emojis
   - Weather and location fields
   - Tagging system
   - Privacy settings (public/private)

Used SQLAlchemy ORM for database abstraction. The relationships are properly set up with cascade delete for data integrity.

Next step: Implement user authentication.""",
                'mood': 'calm',
                'entry_date': datetime.now().date(),
                'weather': 'Cloudy',
                'location': 'Library',
                'tags': 'database,design,sqlalchemy',
                'is_private': True
            },
            {
                'user_id': demo_user.id,
                'title': 'Flask Authentication System',
                'content': """Successfully implemented user authentication! Features added:

🔐 **Registration System:**
- Username and email validation
- Password hashing with werkzeug
- Duplicate user prevention

🔐 **Login System:**
- Session management
- Remember me functionality
- Last login tracking

🔐 **Security Features:**
- Password hashing (never store plain text)
- Session timeout
- Secure cookies

Also created beautiful login and registration forms with Bootstrap 5.""",
                'mood': 'happy',
                'entry_date': datetime.now().date(),
                'weather': 'Clear',
                'location': 'Dorm Room',
                'tags': 'authentication,security,flask',
                'is_private': False
            },
            {
                'user_id': admin_user.id,
                'title': 'System Administrator Welcome',
                'content': """Welcome to the Digital Diary system!

As an administrator, I can:
- Monitor system usage
- View public entries
- Ensure system security
- Help users with issues

The application is built with:
- **Backend:** Flask (Python)
- **Database:** SQLite with SQLAlchemy ORM
- **Frontend:** Bootstrap 5, HTML5, CSS3
- **Authentication:** Flask-Login

A perfect project for college demonstration!""",
                'mood': 'happy',
                'entry_date': datetime.now().date(),
                'weather': 'Perfect',
                'location': 'Server Room',
                'tags': 'administration,system,overview',
                'is_private': False
            }
        ]
        
        for entry_data in sample_entries:
            entry = DiaryEntry(**entry_data)
            db.session.add(entry)
        
        db.session.commit()
        print("✅ Sample data created successfully!")
    else:
        print("✅ Sample data already exists")

print("✅ Helper functions defined")

# Make helper functions available in templates
@app.context_processor
def utility_processor():
    return dict(get_mood_emoji=get_mood_emoji, get_mood_color=get_mood_color, now=datetime.utcnow)

# ==================== ROUTES ====================

@app.route('/')
def index():
    """Home page with project information"""
    total_users = User.query.count()
    total_entries = DiaryEntry.query.count()
    public_entries = DiaryEntry.query.filter_by(is_private=False)\
        .order_by(DiaryEntry.created_at.desc())\
        .limit(6).all()
    
    return render_template('index.html',
                         total_users=total_users,
                         total_entries=total_entries,
                         recent_entries=public_entries,
                         user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember') == 'on'
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            user.last_login = datetime.utcnow()
            db.session.commit()
            flash('✅ Login successful! Welcome back!', 'success')
            
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('❌ Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        full_name = request.form.get('full_name')
        
        # Validation
        if password != confirm_password:
            flash('❌ Passwords do not match', 'danger')
            return redirect(url_for('register'))
        
        if User.query.filter_by(username=username).first():
            flash('❌ Username already exists', 'danger')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('❌ Email already registered', 'danger')
            return redirect(url_for('register'))
        
        # Create new user
        new_user = User(
            username=username,
            email=email,
            full_name=full_name
        )
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('✅ Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    # Get user's entries
    entries = DiaryEntry.query\
        .filter_by(user_id=current_user.id)\
        .order_by(DiaryEntry.entry_date.desc(), DiaryEntry.created_at.desc())\
        .all()
    
    # Statistics
    total_entries = len(entries)
    public_count = DiaryEntry.query.filter_by(user_id=current_user.id, is_private=False).count()
    private_count = total_entries - public_count
    
    # Mood statistics
    mood_stats = {}
    for entry in entries:
        mood_stats[entry.mood] = mood_stats.get(entry.mood, 0) + 1
    
    return render_template('dashboard.html',
                         entries=entries,
                         total_entries=total_entries,
                         public_count=public_count,
                         private_count=private_count,
                         mood_stats=mood_stats,
                         user=current_user)

@app.route('/entry/add', methods=['GET', 'POST'])
@login_required
def add_entry():
    """Add new diary entry"""
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        mood = request.form.get('mood', 'neutral')
        entry_date_str = request.form.get('entry_date')
        weather = request.form.get('weather')
        location = request.form.get('location')
        tags = request.form.get('tags')
        is_private = request.form.get('is_private') == 'true'
        
        # Validate required fields
        if not title or not content:
            flash('❌ Title and content are required', 'danger')
            return redirect(url_for('add_entry'))
        
        # Parse date
        try:
            entry_date = datetime.strptime(entry_date_str, '%Y-%m-%d').date()
        except:
            entry_date = datetime.utcnow().date()
        
        # Create new entry
        new_entry = DiaryEntry(
            user_id=current_user.id,
            title=title,
            content=content,
            mood=mood,
            entry_date=entry_date,
            weather=weather,
            location=location,
            tags=tags,
            is_private=is_private
        )
        
        db.session.add(new_entry)
        db.session.commit()
        
        flash('✅ Diary entry added successfully!', 'success')
        return redirect(url_for('view_entry', entry_id=new_entry.id))
    
    today = datetime.now().strftime('%Y-%m-%d')
    return render_template('add_entry.html', today=today, action='Add', user=current_user)

@app.route('/entry/<int:entry_id>')
def view_entry(entry_id):
    """View a diary entry"""
    entry = DiaryEntry.query.get_or_404(entry_id)
    
    # Check privacy
    if entry.is_private and (not current_user.is_authenticated or current_user.id != entry.user_id):
        flash('🔒 This entry is private', 'warning')
        return redirect(url_for('index'))
    
    # Parse tags
    tags_list = []
    if entry.tags:
        tags_list = [tag.strip() for tag in entry.tags.split(',') if tag.strip()]
    
    return render_template('view_entry.html',
                         entry=entry,
                         tags_list=tags_list,
                         user=current_user)

@app.route('/entry/<int:entry_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_entry(entry_id):
    """Edit a diary entry"""
    entry = DiaryEntry.query.get_or_404(entry_id)
    
    # Check ownership
    if entry.user_id != current_user.id:
        flash('❌ You cannot edit this entry', 'danger')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        entry.title = request.form.get('title')
        entry.content = request.form.get('content')
        entry.mood = request.form.get('mood', 'neutral')
        entry_date_str = request.form.get('entry_date')
        entry.weather = request.form.get('weather')
        entry.location = request.form.get('location')
        entry.tags = request.form.get('tags')
        entry.is_private = request.form.get('is_private') == 'true'
        entry.updated_at = datetime.utcnow()
        
        # Parse date
        try:
            entry.entry_date = datetime.strptime(entry_date_str, '%Y-%m-%d').date()
        except:
            pass
        
        db.session.commit()
        flash('✅ Entry updated successfully!', 'success')
        return redirect(url_for('view_entry', entry_id=entry.id))
    
    # Convert date to string for form
    entry_date_str = entry.entry_date.strftime('%Y-%m-%d') if entry.entry_date else datetime.now().strftime('%Y-%m-%d')
    
    return render_template('add_entry.html',
                         entry=entry,
                         today=entry_date_str,
                         action='Edit',
                         user=current_user)

@app.route('/entry/<int:entry_id>/delete')
@login_required
def delete_entry(entry_id):
    """Delete a diary entry"""
    entry = DiaryEntry.query.get_or_404(entry_id)
    
    # Check ownership
    if entry.user_id != current_user.id:
        flash('❌ You cannot delete this entry', 'danger')
        return redirect(url_for('dashboard'))
    
    db.session.delete(entry)
    db.session.commit()
    
    flash('🗑️ Entry deleted successfully!', 'info')
    return redirect(url_for('dashboard'))

@app.route('/search')
def search():
    """Search diary entries"""
    query = request.args.get('q', '').strip()
    
    if not query:
        return redirect(url_for('index'))
    
    # Search in public entries or user's own entries
    if current_user.is_authenticated:
        entries = DiaryEntry.query.filter(
            (DiaryEntry.user_id == current_user.id) |
            (DiaryEntry.is_private == False)
        ).filter(
            (DiaryEntry.title.contains(query)) |
            (DiaryEntry.content.contains(query)) |
            (DiaryEntry.tags.contains(query))
        ).order_by(DiaryEntry.created_at.desc()).all()
    else:
        entries = DiaryEntry.query.filter_by(is_private=False).filter(
            (DiaryEntry.title.contains(query)) |
            (DiaryEntry.content.contains(query)) |
            (DiaryEntry.tags.contains(query))
        ).order_by(DiaryEntry.created_at.desc()).all()
    
    return render_template('search.html',
                         entries=entries,
                         query=query,
                         user=current_user)

@app.route('/profile')
@login_required
def profile():
    """User profile page"""
    user_stats = {
        'total_entries': DiaryEntry.query.filter_by(user_id=current_user.id).count(),
        'public_entries': DiaryEntry.query.filter_by(user_id=current_user.id, is_private=False).count(),
        'private_entries': DiaryEntry.query.filter_by(user_id=current_user.id, is_private=True).count(),
        'account_age': (datetime.utcnow() - current_user.created_at).days
    }
    
    return render_template('profile.html',
                         user_stats=user_stats,
                         user=current_user)

@app.route('/api/stats')
def api_stats():
    """API endpoint for statistics"""
    stats = {
        'total_users': User.query.count(),
        'total_entries': DiaryEntry.query.count(),
        'public_entries': DiaryEntry.query.filter_by(is_private=False).count(),
        'database': 'SQLite',
        'status': 'online',
        'timestamp': datetime.utcnow().isoformat()
    }
    return jsonify(stats)

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('👋 Logged out successfully', 'info')
    return redirect(url_for('index'))

print("✅ All routes defined")

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', user=current_user), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', user=current_user), 500

# ==================== MAIN EXECUTION ====================

if __name__ == '__main__':
    # Create database tables within app context
    with app.app_context():
        db.create_all()
        create_sample_data()
        
        print("\n✅ Database initialized successfully")
        print("📊 Database Statistics:")
        print(f"   Users: {User.query.count()}")
        print(f"   Diary Entries: {DiaryEntry.query.count()}")
        print(f"   Public Entries: {DiaryEntry.query.filter_by(is_private=False).count()}")
    
    print("\n🌐 Starting Flask development server...")
    print("=" * 70)
    print("📚 PROJECT ACCESS LINKS:")
    print("   Home Page:      http://localhost:5000")
    print("   Login:          http://localhost:5000/login")
    print("   Register:       http://localhost:5000/register")
    print("   Dashboard:      http://localhost:5000/dashboard")
    print("   Add Entry:      http://localhost:5000/entry/add")
    print("   API Stats:      http://localhost:5000/api/stats")
    print("=" * 70)
    print("🎓 DEMO CREDENTIALS:")
    print("   Username: demo_student")
    print("   Password: password123")
    print("=" * 70)
    print("📁 Database file: digital_diary.db (auto-created)")
    print("=" * 70)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
