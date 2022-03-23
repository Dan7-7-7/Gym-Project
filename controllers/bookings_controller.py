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
    sessions = session_repository.select_all_available_sessions()
    num_sessions = len(sessions)
    return render_template('/bookings/new_booking.html', title="New Booking", sessions=sessions, num_sessions=num_sessions)

@bookings_blueprint.route('/bookings/class/new', methods = ['POST'])
def book_member():
    session = session_repository.select(request.form['session_id'])
    num_bookings = len(session_repository.all_booked_members(session))
    spaces = session.capacity - num_bookings
    if 1900 > session.start_time > 1700:
        members = session_repository.premium_unbooked_members(session)
    else:
        members = session_repository.all_unbooked_members(session)
    num_members = len(members)
    return render_template('/bookings/new_class_booking.html', title=f"New Booking for {session}", spaces=spaces, session=session, members=members, num_members=num_members)

@bookings_blueprint.route('/bookings/<id>/new')
def add_booking_to_session(id):
    session = session_repository.select(id)
    num_bookings = len(session_repository.all_booked_members(session))
    spaces = session.capacity - num_bookings
    if 1900 > session.start_time > 1700:
        members = session_repository.premium_unbooked_members(session)
    else:
        members = session_repository.all_unbooked_members(session)
    num_members = len(members)
    return render_template('/bookings/new_class_booking.html', title=f"New Booking for {session}", session=session, members=members, spaces=spaces, num_members=num_members)

@bookings_blueprint.route('/bookings/<id>')
def booking_details(id):
    booking = booking_repository.select(id)
    return render_template('/bookings/booking_details.html', title="Booking Details", booking=booking)
  
@bookings_blueprint.route('/bookings/<id>/edit')
def edit_booking(id):
    booking = booking_repository.select(id)
    member = member_repository.select(booking.member.id)
    session = session_repository.select(booking.session.id)
    sessions = session_repository.select_all_available_sessions()
    if not member.premium:
        sessions = session_repository.select_all_available_sessions_standard_only()
    sessions = session_repository.filter_sessions_by_member_booking(member, sessions)
    return render_template('/bookings/edit_booking.html', title="Edit Booking", booking=booking, sessions=sessions, session=session, member=member)

@bookings_blueprint.route('/bookings/<id>', methods = ['POST'])
def update_booking(id):
    booking = booking_repository.select(id)
    member = member_repository.select(booking.member.id)
    session = session_repository.select(request.form['session_id'])
    updated_booking = Booking(member, session, id)
    booking_repository.update(updated_booking)
    return redirect(f'/bookings/{id}')




# BACK-END TO-DO LIST
# edit bookings DONE!!!!!
# re-factor so that you choose class first, then directs to class_booking page DONE BUT NOT DRY
# can't book twice - members greyed out/absent from list if already booked DONE!!!
# can't exceed capacity DONE!!!!!
# homepage total bookings and classes DONE!!!!
# classes appear in chronological order (make it datetime?) DONE!!!!
# premium/ standard membership with benefits for premium DONE!!!
# deactivated members, who don't show up anymore DONE!!!!
# re-factor with a sessions_repo function which returns all sessions with availability DONE!!!!
# search function for bookings list?!? (and classes) NOT LIKELY MATE