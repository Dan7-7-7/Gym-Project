from flask import Flask, render_template
from repositories import session_repository

from controllers.bookings_controller import bookings_blueprint
from controllers.members_controller import members_blueprint
from controllers.sessions_controller import sessions_blueprint

app = Flask(__name__)

app.register_blueprint(bookings_blueprint)
app.register_blueprint(members_blueprint)
app.register_blueprint(sessions_blueprint)

@app.route('/')
def home():
    all_sessions = session_repository.select_all()
    num_classes = len(all_sessions)
    num_members = 0
    for session in all_sessions:
        num_members += len(session_repository.all_booked_members(session))
    return render_template('index.html', title="Homepage", num_classes=num_classes, num_members=num_members)

if __name__ == '__main__':
    app.run(debug=True)