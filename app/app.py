import os
from flask import Flask, render_template
from config import Config, DevelopmentConfig, ProductionConfig, TestingConfig

app = Flask(__name__)

# Flask will pick up FLASK_ENV from .flaskenv, so no need to manually check
app.config.from_object({
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}[app.config.get('ENV', 'development')])

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)