from flask import session
from db.run_sql import run_sql
from models.booking import Booking
from repositories import member_repository, session_repository

def save(booking):
    sql = "INSERT INTO bookings (member_id, session_id) VALUES (%s, %s) RETURNING *"
    values = [booking.member.id, booking.session.id]
    result = run_sql(sql, values)[0]
    booking.id = result['id']
    return booking

def select(id):
    booking = None
    sql = "SELECT * FROM bookings WHERE id = %s"
    values = [id]
    result = run_sql(sql, values)[0]
    if result is not None:
        member = member_repository.select(result['member_id'])
        session = session_repository.select(result['session_id'])
        booking = Booking(member, session, result['id'])
    return booking

def select_all():
    bookings = []
    sql = "SELECT * FROM bookings"
    results = run_sql(sql)
    for row in results:
        member = member_repository.select(row['member_id'])
        session = session_repository.select(row['session_id'])
        booking = Booking(member, session, row['id'])
        bookings.append(booking)
    return bookings

def update(booking):
    sql = "UPDATE bookings SET (%s, %s) WHERE id = %s"
    values = [booking.member.id, booking.session.id, booking.id]
    run_sql(sql, values)