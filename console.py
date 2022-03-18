from models.booking import Booking
from models.member import Member
from models.session import Session
from repositories import booking_repository, member_repository, session_repository

member1 = Member("The Professor", 35)
member2 = Member("Denver", 23)
member3 = Member("Nairobi", 31)

session1 = Session("Pilates", 1730, 45, 12)
session2 = Session("Tai Chi", 2030, 60, 15)
session3 = Session("Yoga", 1830, 45, 10)

booking1 = Booking(member1, session2)
booking2 = Booking(member2, session1)
booking3 = Booking(member3, session3)

member_repository.save(member1)
member_repository.save(member2)
member_repository.save(member3)

session_repository.save(session1)
session_repository.save(session2)
session_repository.save(session3)

booking_repository.save(booking1)
booking_repository.save(booking2)
booking_repository.save(booking3)