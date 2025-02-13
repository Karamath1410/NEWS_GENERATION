import os
from flask import Flask, request, render_template, redirect, url_for, flash, session, g
import requests
import json
from googletrans import Translator
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key

# Configure SQLite database
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'users.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    categories = db.Column(db.String(200))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

# Create database tables
def init_db():
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("Database initialized successfully")
        except Exception as e:
            print(f"Error initializing database: {e}")

# Initialize database tables
init_db()

translator = Translator()

def fetch_news(api_key, query, language='en', limit=20):
    url = f"https://newsapi.org/v2/everything?q={query}&language={language}&apiKey={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get('status') != 'ok':
            print(f"News API error: {data.get('message')}")
            return []

        articles = data.get('articles', [])[:limit]
        processed_articles = []

        for article in articles:
            processed_article = {
                'title': article.get('title', ''),
                'description': article.get('description', ''),
                'url': article.get('url', ''),
                'image': article.get('urlToImage') if article.get('urlToImage') else '/static/images/placeholder.svg'
            }
            processed_articles.append(processed_article)

        return processed_articles
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

def translate_articles(articles, dest_language):
    translated_articles = []
    for article in articles:
        try:
            translated_article = {
                'title': translator.translate(article['title'], dest=dest_language).text,
                'description': translator.translate(article['description'], dest=dest_language).text if article['description'] else '',
                'url': article['url'],
                'image': article['image']
            }
        except Exception as e:
            print(f"Error translating article: {e}")
            translated_article = {
                'title': article['title'],
                'description': article['description'] if article['description'] else '',
                'url': article['url'],
                'image': article['image']
            }
        translated_articles.append(translated_article)
    return translated_articles

def fetch_fact_check(query, api_key):
    url = f"https://factchecktools.googleapis.com/v1alpha1/claims:search?query={query}&key={api_key}"
    response = requests.get(url)
    fact_checks = response.json().get('claims', [])
    return fact_checks

@app.before_request
def clear_session():
    if not session.get('logged_in'):
        session.clear()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Get categories and ensure at least one is selected
        categories = request.form.getlist('categories')
        if not categories:
            flash('Please select at least one category', 'danger')
            return redirect(url_for('signup'))
        selected_categories = ','.join(categories)
        age = request.form['age']
        gender = request.form['gender']

        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('signup'))

        user = User(username=username, categories=selected_categories, age=age, gender=gender)
        user.set_password(password)
        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            print(f"Error during registration: {e}")
            flash('Registration failed. Please try again.', 'danger')
            return redirect(url_for('signup'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['logged_in'] = True
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def home():
    query = 'latest news'
    language = 'en'
    user_data = None

    if session.get('logged_in'):
        try:
            user = User.query.get(session['user_id'])
            if user:
                print(f"Found user: {user.username}")  # Debug log
                print(f"Raw categories: {user.categories}")  # Debug log

                if user.categories:
                    # Split categories and filter out empty strings
                    categories = [cat.strip() for cat in user.categories.split(',') if cat.strip()]
                    print(f"Processed categories: {categories}")  # Debug log

                    if categories:
                        query = ' OR '.join(categories)
                        user_data = {
                            "username": user.username,
                            "categories": categories
                        }
                    else:
                        user_data = {
                            "username": user.username,
                            "categories": ["No categories selected"]
                        }
                else:
                    user_data = {
                        "username": user.username,
                        "categories": ["No categories selected"]
                    }
        except Exception as e:
            print(f"Error getting user data: {e}")
            user_data = None

    if request.method == 'POST':
        query = request.form.get('query', 'latest news')
        language = request.form.get('language', 'en')

    news_api_key = os.getenv("news_api_key")
    fact_check_api_key = os.getenv("fact_check_api_key")

    print(f"User data being sent to template: {user_data}")  # Debug log

    articles = fetch_news(news_api_key, query)
    print(f"Fetched {len(articles)} articles")  # Debug log

    if language != 'en':
        articles = translate_articles(articles, language)

    fact_checks = fetch_fact_check(query, fact_check_api_key)

    return render_template('index.html',
                         articles=articles,
                         fact_checks=fact_checks,
                         selected_language=language,
                         user=user_data)

@app.route('/guest')
def guest():
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)