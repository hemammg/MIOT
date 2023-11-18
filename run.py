import os

from app import app

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ['true', '1']
    app.run(debug=debug_mode)
