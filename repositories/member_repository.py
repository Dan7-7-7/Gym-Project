from db.run_sql import run_sql
from models.member import Member

def save(member):
    sql = "INSERT INTO members (name, age) VALUES (%s, %s) RETURNING *"
    values = [member.name, member.age]
    result = run_sql(sql, values)[0]
    member.id = result['id']
    return member