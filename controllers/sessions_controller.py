from flask import Flask, Blueprint, render_template, request, redirect, session
from models.session import Session
from models.booking import Booking
from repositories import session_repository, member_repository, booking_repository

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
    session = Session(request.form['name'], request.form['start_time'], request.form['duration'], request.form['capacity'], True, id)
    session_repository.update(session)
    return redirect(f'/classes/{id}')

@sessions_blueprint.route('/classes/<id>/bookings')
def session_bookings(id):
    session = session_repository.select(id)
    num_bookings = len(session_repository.all_booked_members(session))
    spaces = session.capacity - num_bookings
    members = session_repository.all_booked_members(session)
    return render_template('/sessions/members_booked.html', title=f"{session} Bookings", session=session, bookings=num_bookings, spaces=spaces, members=members)

@sessions_blueprint.route('/classes/<id>/bookings', methods = ['POST'])
def add_session_booking(id):
    session = session_repository.select(id)
    member = member_repository.select(request.form['member_id'])
    booking = Booking(member, session)
    booking_repository.save(booking)
    return redirect(f'/classes/{id}/bookings')

@sessions_blueprint.route('/classes/<id>/deactivate/confirm')
def confirm(id):
    session = session_repository.select(id)
    return render_template('/sessions/confirm_deactivate.html', title="Confirm Deactivation", session=session)

@sessions_blueprint.route('/classes/<id>/deactivate')
def deactivate(id):
    session = session_repository.select(id)
    session_repository.deactivate(session)
    return render_template('/sessions/deactivate.html', title="Deactivate Class", session=session)

@sessions_blueprint.route('/classes/<id>/reactivate')
def reactivate(id):
    session = session_repository.select(id)
    session_repository.reactivate(session)
    return render_template('/sessions/reactivate.html', title="Class Reactivated", session=session)