from flask import Flask, Blueprint, render_template, request, redirect
from models.booking import Booking
from repositories import booking_repository, member_repository, session_repository

bookings_blueprint = Blueprint("bookings", __name__)

@bookings_blueprint.route('/bookings')
def all_bookings():
    bookings = booking_repository.select_all()
    return render_template('/bookings/index.html', title="All Bookings", bookings=bookings)

@bookings_blueprint.route('/bookings/new')
def new_booking():
    sessions = session_repository.select_all()
    full_sessions = []
    for session in sessions:
        if session.capacity - len(session_repository.all_booked_members(session)) == 0:
            full_sessions.append(session)
    for session in full_sessions:
        sessions.remove(session)
    # refactor this!
    return render_template('/bookings/new_booking.html', title="New Booking", sessions=sessions)

@bookings_blueprint.route('/bookings/class/new', methods = ['POST'])
def book_member():
    session = session_repository.select(request.form['session_id'])
    num_bookings = len(session_repository.all_booked_members(session))
    spaces = session.capacity - num_bookings
    if session.start_time > 1700 and session.start_time < 1900:
        members = session_repository.premium_unbooked_members(session)
    else:
        members = session_repository.all_unbooked_members(session)
    return render_template('/bookings/new_class_booking.html', title=f"New Booking for {session}", spaces=spaces, session=session, members=members)

# @bookings_blueprint.route('/bookings', methods = ['POST'])
# def add_booking(): 
#     member = member_repository.select(request.form['member_id'])
#     session = session_repository.select(request.form['session_id'])
#     booking = Booking(member, session)
#     booking_repository.save(booking)
#     return redirect('/bookings')

@bookings_blueprint.route('/bookings/<id>/new')
def add_booking_to_session(id):
    session = session_repository.select(id)
    num_bookings = len(session_repository.all_booked_members(session))
    spaces = session.capacity - num_bookings
    if session.start_time > 1700 and session.start_time < 1900:
        members = session_repository.premium_unbooked_members(session)
    else:
        members = session_repository.all_unbooked_members(session)
    return render_template('/bookings/new_class_booking.html', title=f"New Booking for {session}", session=session, members=members, spaces=spaces)

@bookings_blueprint.route('/bookings/<id>')
def booking_details(id):
    booking = booking_repository.select(id)
    return render_template('/bookings/booking_details.html', title="Booking Details", booking=booking)
  
@bookings_blueprint.route('/bookings/<id>/edit')
def edit_booking(id):
    booking = booking_repository.select(id)
    sessions = session_repository.select_all()
    members = member_repository.select_all()
    return render_template('/bookings/edit_booking.html', title="Edit Booking", booking=booking, sessions=sessions, members=members)

@bookings_blueprint.route('/bookings/<id>', methods = ['POST'])
def update_booking(id):
    member = member_repository.select(request.form['member_id'])
    session = session_repository.select(request.form['session_id'])
    booking = Booking(member, session, id)
    booking_repository.update(booking)
    return redirect(f'/bookings/{id}')




# BACK-END TO-DO LIST
# edit bookings DONE!!!!!
# re-factor so that you choose class first, then directs to class_booking page DONE BUT NOT DRY
# can't book twice - members greyed out/absent from list if already booked DONE!!!
# can't exceed capacity DONE!!!!!
# homepage total bookings and classes DONE!!!!
# classes appear in chronological order (make it datetime?) DONE!!!!
# premium/ standard membership with benefits for premium DONE!!!
# deactivated members, who don't show up anymore
    # NEXT STEP: make deactivated members disappear from all lists
    # will have to edit and/or add functions in member and session repos (the selectall functions?)
    # then use them in controllers
# re-factor with a sessions_repo function which returns all sessions with availability
# search function for bookings list?!? (and classes)