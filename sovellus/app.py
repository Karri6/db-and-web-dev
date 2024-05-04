"""
Launches the app when running flask

"""

from app_modules.main import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
