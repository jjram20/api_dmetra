from app import app
from utils.db import db

#Create the database in case it does not exist
with app.app_context():
    db.create_all()

PORT = 8000

#Run application
if __name__ == "__main__":
    app.run(host='0.0.0.0', port = PORT)