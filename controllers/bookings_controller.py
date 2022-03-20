from flask import Flask, Blueprint, render_template, request, redirect
from models.booking import Booking
from repositories import booking_repository, member_repository, session_repository

bookings_blueprint = Blueprint("bookings", __name__)

# all bookings
@bookings_blueprint.route('/bookings')
def all_bookings():
    bookings = booking_repository.select_all()
    return render_template('/bookings/index.html', title="All Bookings", bookings=bookings)

@bookings_blueprint.route('/bookings/new')
def new_booking():
    members = member_repository.select_all()
    sessions = session_repository.select_all()
    return render_template('/bookings/new_booking.html', title="New Booking", members=members, sessions=sessions)

@bookings_blueprint.route('/bookings', methods = ['POST'])
def add_booking():
    member = member_repository.select(request.form['member_id'])
    session = session_repository.select(request.form['session_id'])
    booking = Booking(member, session)
    booking_repository.save(booking)
    return redirect('/bookings')

@bookings_blueprint.route('/bookings/<id>/new')
def add_booking_to_class(id):
    session = session_repository.select(id)
    members = member_repository.select_all()
    num_bookings = len(session_repository.members(session))
    spaces = session.capacity - num_bookings
    # it would be nice if the members currently booked were removed from the drop-down menu
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
# re-factor so that you choose class first, then directs to class_booking page
# can't book twice - members greyed out/absent from list if already booked
# can't exceed capacity
# premium/ standard membership with benefits for premium
# deactivated members, who don't show up anymore