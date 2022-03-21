from db.run_sql import run_sql
from models.member import Member
from models.session import Session

def save(member):
    sql = "INSERT INTO members (name, age, premium, activated) VALUES (%s, %s, %s, %s) RETURNING *"
    values = [member.name, member.age, member.premium, member.activated]
    result = run_sql(sql, values)[0]
    member.id = result['id']
    return member

def select(id):
    member = None
    sql = "SELECT * FROM members WHERE id = %s"
    values = [id]
    result = run_sql(sql, values)[0]
    if result is not None:
        member = Member(result['name'], result['age'], result['premium'], result['activated'], result['id'])
    return member

def select_all():
    members = []
    sql = "SELECT * FROM members"
    results = run_sql(sql)
    for row in results:
        member = Member(row['name'], row['age'], row['premium'], row['activated'], row['id'])
        members.append(member)
    return members

def select_all_activated_members():
    members = select_all()
    deactivated_members = []
    for member in members:
        if not member.activated:
            deactivated_members.append(member)
    for member in deactivated_members:
        members.remove(member)
    return members

def update(member):
    sql = "UPDATE members SET (name, age, premium, activated) = (%s, %s, %s, %s) WHERE id = %s"
    values = [member.name, member.age, member.premium, member.activated, member.id]
    run_sql(sql, values)

def sessions(member):
    sessions = []
    sql = "SELECT sessions.* FROM sessions INNER JOIN bookings ON sessions.id = bookings.session_id WHERE member_id = %s"
    values = [member.id]
    results = run_sql(sql, values)
    for row in results:
        session = Session(row['name'], row['start_time'], row['duration'], row['capacity'], row['activated'], row['id'])
        sessions.append(session)
    return sessions

def deactivate(member):
    member.activated = False
    update(member)

def reactivate(member):
    member.activated = True
    update(member)