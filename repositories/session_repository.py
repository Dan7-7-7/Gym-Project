from msilib.schema import Class
from db.run_sql import run_sql
from models.session import Session

def save(session):
    sql = "INSERT INTO sessions (name, start_time, duration, capacity) VALUES (%s, %s, %s, %s) RETURNING *"
    values = [session.name, session.start_time, session.duration, session.capacity]
    result = run_sql(sql, values)[0]
    session.id = result['id']
    return session