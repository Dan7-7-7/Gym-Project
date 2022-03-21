from db.run_sql import run_sql
from models.session import Session
from models.member import Member
from repositories import member_repository

def save(session):
    sql = "INSERT INTO sessions (name, start_time, duration, capacity, activated) VALUES (%s, %s, %s, %s, %s) RETURNING *"
    values = [session.name, session.start_time, session.duration, session.capacity, session.activated]
    result = run_sql(sql, values)[0]
    session.id = result['id']
    return session

def select(id):
    session = None
    sql = "SELECT * FROM sessions WHERE id = %s"
    values = [id]
    result = run_sql(sql, values)[0]
    if result is not None:
        session = Session(result['name'], result['start_time'], result['duration'], result['capacity'], result['activated'], result['id'])
    return session

def select_all():
    sessions = []
    sql = "SELECT * FROM sessions"
    results = run_sql(sql)
    for row in results:
        session = Session(row['name'], row['start_time'], row['duration'], row['capacity'], row['activated'], row['id'])
        sessions.append(session)
    return sessions

def select_all_activated_sessions():
    sessions = select_all()
    deactivated_sessions = []
    for session in sessions:
        if not session.activated:
            deactivated_sessions.append(session)
    for session in deactivated_sessions:
        sessions.remove(session)
    return sessions

def update(session):
    sql = "UPDATE sessions SET (name, start_time, duration, capacity, activated) = (%s, %s, %s, %s, %s) WHERE id = %s"
    values = [session.name, session.start_time, session.duration, session.capacity, session.activated, session.id]
    run_sql(sql, values)

def all_booked_members(session):
    members = []
    sql = "SELECT members.* FROM members INNER JOIN bookings ON members.id = bookings.member_id WHERE session_id = %s"
    values = [session.id]
    results = run_sql(sql, values)
    for row in results:
        member = Member(row['name'], row['age'], row['premium'], row['activated'], row['id'])
        members.append(member)
    return members

def all_unbooked_members(session):
    members = member_repository.select_all_activated_members()
    booked_members = []
    session_members = all_booked_members(session)
    for session_member in session_members:
        for member in members:
            if member.id == session_member.id:
                booked_members.append(member)
    for member in booked_members:
        members.remove(member)
    return members

def premium_unbooked_members(session):
    members = all_unbooked_members(session)
    standard_members = []
    for member in members:
        if not member.premium:
            standard_members.append(member)
    for member in standard_members:
        members.remove(member)
    return members

def select_all_available_sessions():
    sessions = select_all_activated_sessions()
    full_sessions = []
    for session in sessions:
        if session.capacity - len(all_booked_members(session)) == 0:
            full_sessions.append(session)
    for session in full_sessions:
        sessions.remove(session)
    return sessions

def deactivate(session):
    session.activated = False
    update(session)

def reactivate(session):
    session.activated = True
    update(session)