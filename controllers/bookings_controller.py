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

# new booking for specific session - pre populated