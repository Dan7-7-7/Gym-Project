from models.booking import Booking
from models.member import Member
from models.session import Session
from repositories import booking_repository, member_repository, session_repository

member1 = Member("Sergio Marquina", 35, True)
member2 = Member("Daniel Ramos", 23)
member3 = Member("Agata Jimenez", 31, True)
member4 = Member("Radko Dragic", 37, False, False)

session1 = Session("Pilates", 1730, 45, 12)
session2 = Session("Tai Chi", 2030, 60, 15)
session3 = Session("Yoga", 1830, 45, 10)

booking1 = Booking(member1, session1)
booking2 = Booking(member2, session2)
booking3 = Booking(member3, session3)
booking4 = Booking(member1, session3)

member_repository.save(member1)
member_repository.save(member2)
member_repository.save(member3)
member_repository.save(member4)

session_repository.save(session1)
session_repository.save(session2)
session_repository.save(session3)

booking_repository.save(booking1)
booking_repository.save(booking2)
booking_repository.save(booking3)
booking_repository.save(booking4)

# print(member_repository.select(member1.id).__dict__)
# print(session_repository.select(session1.id).__dict__)
# print(booking_repository.select(booking1.id).__dict__)

# members = member_repository.select_all()
# for member in members:
#     print(member.__dict__)

# sessions = session_repository.select_all()
# for session in sessions:
#     print(session.__dict__)

# bookings = booking_repository.select_all()
# for booking in bookings:
#     print(booking.__dict__)
#     print(booking.member.__dict__)
#     print(booking.session.__dict__)

# member1.name = "el profesor"
# member_repository.update(member1)
# print(member_repository.select(member1.id).__dict__)

# session1.name = "Zumba"
# session_repository.update(session1)
# print(session_repository.select(session1.id).__dict__)

# booking1.session = session3
# booking_repository.update(booking1)
# print(booking_repository.select(booking1.id).session.__dict__)

# prof_sessions = member_repository.sessions(member1)
# for session in prof_sessions:
#     print(session.__dict__)

# yoga_members = session_repository.members(session3)
# for member in yoga_members:
#     print(member.__dict__)