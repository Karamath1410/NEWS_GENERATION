# AI News Generator

An AI-powered multilingual news generation platform that delivers personalized news content in Telugu, Hindi, and English.

## Features

- Multilingual news generation (English, Telugu, Hindi)
- User-based category preferences
- Real-time news translation
- Fact-checking integration
- Responsive design with image handling

## Prerequisites

- Python 3.11 or higher
- News API key (from newsapi.org)
- Google Fact Check API key

## Setup Instructions

1. Clone the repository
```bash
git clone <repository-url>
cd ai-news-generator
```

2. Create and activate a virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -e .
```

4. Create a .env file in the root directory with your API keys:
```
news_api_key=your_news_api_key_here
fact_check_api_key=your_fact_check_api_key_here
```

5. Initialize the database
```bash
python
>>> from app import init_db
>>> init_db()
```

6. Run the application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Project Structure

```
├── app.py                 # Main application file
├── static/               # Static files (CSS, JS, images)
│   ├── styles.css       # Main stylesheet
│   ├── js/             
│   │   └── image-handler.js  # Image loading and handling
│   └── images/         
│       └── placeholder.svg   # Placeholder for missing images
├── templates/           # HTML templates
│   ├── index.html      # Main news page
│   ├── login.html      # Login page
│   └── signup.html     # Registration page
└── users.db            # SQLite database file
```

## Environment Variables

- `news_api_key`: Your News API key from newsapi.org
- `fact_check_api_key`: Your Google Fact Check API key

## Usage

1. Create an account or login
2. Select your preferred news categories
3. Use the search bar to find specific news
4. Switch between languages using the language selector

## License

This project is licensed under the MIT License - see the LICENSE file for details
