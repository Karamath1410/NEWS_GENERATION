from setuptools import setup, find_packages

setup(
    name="ai-news-generator",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "flask>=3.1.0",
        "flask-sqlalchemy>=3.1.1",
        "googletrans==3.1.0a0",
        "python-dotenv>=1.0.1",
        "requests>=2.32.3",
        "werkzeug>=3.1.3",
        "flask-login>=0.6.3",
        "flask-wtf>=1.2.2",
        "email-validator>=2.2.0",
        "gunicorn>=23.0.0",
    ],
    python_requires=">=3.11",
    author="Your Name",
    description="AI-powered multilingual news generation platform",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
