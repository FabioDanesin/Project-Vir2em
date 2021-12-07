systemctl stop apache2
cd Frontend
export FLASK_APP=MainPage.py
export FLASK_ENV=development
flask run --host=localhost --port=5000