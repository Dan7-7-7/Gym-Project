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
    all_sessions = session_repository.select_all_activated_sessions()
    num_classes = len(all_sessions)
    num_members = 0
    for session in all_sessions:
        num_members += len(session_repository.all_booked_members(session))
    if num_members == 1:
        booked_members = "1 member"
    else:
        booked_members = f"{num_members} members"
    if num_classes == 1:
        booked_classes = "1 class"
    else:
        booked_classes = f"{num_classes} classes"
    return render_template('index.html', title="Homepage", booked_classes=booked_classes, booked_members=booked_members)

if __name__ == '__main__':
    app.run(debug=True)