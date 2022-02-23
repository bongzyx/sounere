from app import app, db
import os

if __name__ == '__main__':

    if not os.path.exists('app/db.sqlite'):
        db.create_all()
        print("created db")
    app.run(debug=True, host="0.0.0.0", port=2455)
