import os
from app import create_app

# Get the configuration from environment or use 'default' configuration
config_name = os.getenv('FLASK_CONFIG', 'default')

# Create the app instance with the specified configuration
app = create_app(config_name)

# Run the app if this file is run directly
if __name__ == '__main__':
    app.run()
