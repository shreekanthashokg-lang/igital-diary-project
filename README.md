
Mini Project 📓 Digital Diary 
A full-featured digital diary Web Application built with Flask, SQLAlchemy, and Bootstrap 5.
Designed as a college project to demonstrate user authentication, CRUD operations, mood tracking, tagging, and responsive design.

https://img.shields.io/badge/Flask-2.3.3-blue
https://img.shields.io/badge/SQLAlchemy-3.0.5-red
https://img.shields.io/badge/Bootstrap-5-purple
https://img.shields.io/badge/license-MIT-green

✨ Features
User Authentication – Registration, login, logout, password hashing, “remember me”

Diary Entries – Create, read, update, delete entries with rich text content

Mood Tracking – Choose mood (happy, excited, calm, sad, etc.) with emoji & colour coding

Privacy Control – Mark entries as public or private

Tagging System – Add comma-separated tags, search by tags

Search – Find entries by title, content or tags (public entries + your own)

Statistics Dashboard – See total entries, public/private split, mood distribution

User Profile – Account age, entry counts, last login tracking

Public Entries Feed – Explore recent public entries on the home page

REST API Endpoint – /api/stats returns global usage statistics (JSON)

Responsive UI – Works on desktop, tablet, and mobile (Bootstrap 5)

🛠️ Tech Stack
Layer	Technology
Backend	Flask (Python)
Database	SQLite + SQLAlchemy ORM
Authentication	Flask-Login + Werkzeug password hashing
Frontend	Bootstrap 5, HTML5, CSS3, Jinja2 templates
Icons	Emoji (mood indicators)
📁 Project Structure
text
digital-diary/
├── app.py                 # Main application entry point
├── requirements.txt       # Python dependencies
├── digital_diary.db       # SQLite database (auto-created on first run)
├── templates/             # HTML templates (Jinja2)
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── add_entry.html
│   ├── view_entry.html
│   ├── search.html
│   ├── profile.html
│   ├── 404.html
│   └── 500.html
├── static/                # Custom CSS, JS, images (if any)
│   └── style.css
└── README.md
Note: The templates and static folder are required for the app to run.
If they are missing, you can create them based on the routes defined in app.py.

🚀 Getting Started
Prerequisites
Python 3.8 or higher

pip (Python package manager)

Installation
Clone the repository

bash
git clone https://github.com/your-username/digital-diary.git
cd digital-diary
Create a virtual environment (recommended)

bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
Install dependencies

bash
pip install -r requirements.txt
Run the application

bash
python app.py
On first run, the script will:

Create digital_diary.db (SQLite database)

Create all tables (User, DiaryEntry)

Populate sample data (demo user, admin user, and 4 sample entries)

Open your browser and go to:
http://localhost:5000

🔐 Demo Credentials
Use these accounts to test the application immediately:

Role	Username	Password
Student (Demo)	demo_student	password123
Admin	admin	admin123
You can also register a new account from the login page.

📚 Usage Guide
After logging in
Dashboard – View all your diary entries, filter by mood, see statistics.

Add Entry – Write a new diary entry, choose mood, set privacy, add tags.

Edit/Delete – Each entry has edit/delete buttons (only for your own entries).

Search – Use the search bar in the navigation to find entries by keyword.

Profile – View your account info and overall statistics.

Logout – Click the logout button in the navbar.

Public area (not logged in)
See recent public entries on the home page.

View individual public entries (private entries are hidden).

Search public entries (limited to public content).

API endpoint
URL: /api/stats

Method: GET

Response example:

json
{
  "total_users": 2,
  "total_entries": 5,
  "public_entries": 3,
  "database": "SQLite",
  "status": "online",
  "timestamp": "2025-01-29T12:34:56"
}
🧪 Running in Production (Optional)
The current configuration uses debug=True and a hardcoded SECRET_KEY, which is fine for development/demonstration.
For a real deployment, set the following environment variables:

bash
export SECRET_KEY="your-random-secret-key"
export FLASK_ENV="production"
Then modify app.py to read from os.environ.get() and set debug=False.

📸 Screenshots
(Add actual screenshots of your running app here)

Home Page	Dashboard	Add Entry
https://screenshots/home.png	https://screenshots/dashboard.png	https://screenshots/add.png
🧰 Customization
Add more moods – Edit get_mood_emoji() and get_mood_color() in app.py.

Change database – Update SQLALCHEMY_DATABASE_URI to PostgreSQL, MySQL, etc.

Extend models – Add new fields to User or DiaryEntry and run database migrations (consider Flask-Migrate).

🤝 Contributing
This is a college project, but suggestions and improvements are welcome!
Feel free to open an issue or submit a pull request.

📄 License
This project is open-source and available under the MIT License.

📬 Contact:
Project Author – College Student

GitHub: https://github.com/shreekanthashokg-lang
Email:  2222509208@svysa-sas.edu.in
Email:  shreekanthashokg@gmail.com
