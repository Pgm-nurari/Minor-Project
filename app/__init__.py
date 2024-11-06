from flask import Flask

app = Flask(__name__)

from app import routes
from app import home
from app import admin
from app import event_manager
from app import finance_manager