from db.run_sql import run_sql
from models.booking import Booking

def save(booking):
    sql = "INSERT INTO bookings (member_id, session_id) VALUES (%s, %s) RETURNING *"
    values = [booking.member.id, booking.session.id]
    result = run_sql(sql, values)[0]
    booking.id = result['id']
    return booking