from db.run_sql import run_sql
from models.member import Member
from models.session import Session

def save(member):
    sql = "INSERT INTO members (name, age) VALUES (%s, %s) RETURNING *"
    values = [member.name, member.age]
    result = run_sql(sql, values)[0]
    member.id = result['id']
    return member

def select(id):
    member = None
    sql = "SELECT * FROM members WHERE id = %s"
    values = [id]
    result = run_sql(sql, values)[0]
    if result is not None:
        member = Member(result['name'], result['age'], result['id'])
    return member

def select_all():
    members = []
    sql = "SELECT * FROM members"
    results = run_sql(sql)
    for row in results:
        member = Member(row['name'], row['age'], row['id'])
        members.append(member)
    return members

def update(member):
    sql = "UPDATE members SET (name, age) = (%s, %s) WHERE id = %s"
    values = [member.name, member.age, member.id]
    run_sql(sql, values)

def sessions(member):
    sessions = []
    sql = "SELECT sessions.* FROM sessions INNER JOIN bookings ON sessions.id = bookings.session_id WHERE member_id = %s"
    values = [member.id]
    results = run_sql(sql, values)
    for row in results:
        session = Session(row['name'], row['start_time'], row['duration'], row['capacity'], row['id'])
        sessions.append(session)
    return sessions