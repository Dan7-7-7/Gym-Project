from flask import Flask, Blueprint, render_template, request, redirect, session
from models.session import Session
from repositories import session_repository

sessions_blueprint = Blueprint("sessions", __name__)

@sessions_blueprint.route('/classes')
def show_classes():
    sessions = session_repository.select_all()
    return render_template('/sessions/index.html', title="Classes", sessions=sessions)

@sessions_blueprint.route('/classes/new')
def new_session():
    return render_template('/sessions/new_session.html', title="New Class")

@sessions_blueprint.route('/classes', methods=['POST'])
def create_session():
    session = Session(request.form['name'], request.form['start_time'], request.form['duration'], request.form['capacity'])
    session_repository.save(session)
    return redirect('/classes')

@sessions_blueprint.route('/classes/<id>')
def single_session(id):
    session = session_repository.select(id)
    return render_template('/sessions/single_session.html', title="Class Details", session=session)

@sessions_blueprint.route('/classes/<id>/edit')
def edit_session(id):
    session = session_repository.select(id)
    return render_template('/sessions/edit_session.html', title="Edit Session Details", session=session)

@sessions_blueprint.route('/classes/<id>', methods=['POST'])
def update_session(id):
    session = Session(request.form['name'], request.form['start_time'], request.form['duration'], request.form['capacity'], id)
    session_repository.update(session)
    return redirect(f'/classes/{id}')

@sessions_blueprint.route('/classes/<id>/bookings')
def session_bookings(id):
    session = session_repository.select(id)
    num_bookings = len(session_repository.members(session))
    spaces = session.capacity - num_bookings
    members = session_repository.members(session)
    return render_template('/sessions/members_booked.html', title=f"{session} Bookings", session=session, bookings=num_bookings, spaces=spaces, members=members)
    