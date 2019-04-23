# System modules
import os

# Application modules
from app.config import db
from app.models import Person

# Base data
PEOPLE = [
    {"fname": "Doug", "lname": "Farrell"},
    {"fname": "Kent", "lname": "Brockman"},
    {"fname": "Bunny", "lname": "Easter"}
]


# Delete existing database file
if os.path.exists("people.db"):
    os.remove("people.db")

# Create the databse
db.create_all()

# Load data into database
for person in PEOPLE:
    p = Person(lname=person.get('lname'), fname=person.get('fname'))
    db.session.add(p)

db.session.commit()

