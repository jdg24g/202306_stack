import os

from flask import Flask

from dotenv import load_dotenv

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY')

load_dotenv()