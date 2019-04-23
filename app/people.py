"""
People module supporting Rest actions for people collection
"""

# System modules
from datetime import datetime

# 3rd party modules
from flask import make_response, abort

# Application modules
from config import db
from models import Person, PersonSchema


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


def read_all():
    """
    Function for responding to request for /api/people with complete list of people

    :return:    json string of list of people
    """
    # Create list of people from data
    people = Person.query.order_by(Person.lname).all()

    # serialize data for making response
    person_schema = PersonSchema(many=True)
    data = person_schema.dump(people).data
    return data


def read_one(person_id):
    """
    Function for responding to requests for /api/people/{lname} with one matching person

    :param person_id: Id of person to find
    :return:    person matching last name
    """
    # Get requested person
    person = Person.query.filter(Person.person_id == person_id).one_or_none()

    # Did we find a person?
    if person is not None:
        # Serialize the data for response
        person_schema = PersonSchema()
        data = person_schema.dump(person).data
        return data
    # if there is no person in database
    else:
        abort(
            404,
            "Person not found for Id: {person_id}".format(person_id=person_id),
        )


def create(person):
    """
    Function responding to requests for creating a new person

    :param person:  person to create in people's structure
    :return: 201 on success, 406 if person already exists
    """
    lname = person.get("lname", None)
    fname = person.get("fname", None)

    existing_person = (
        Person.query.filter(Person.fname == fname).filter(Person.lname == lname).one_or_none()
    )

    if existing_person is None:
        # Create a person instance using schema and passed in person
        schema = PersonSchema()
        new_person = schema.load(person, session=db.session).data

        # Add person to the session and commit to database
        db.session.add(new_person)
        db.session.commit()

        # Serialize and return newly created person in response
        data = schema.dump(new_person).data

        return data, 201
    else:
        abort(
            409,
            "Person {fname} {lname} exists already".format(fname=fname, lname=lname),
        )


def update(person_id, person):
    """
    Function for updating existing person in people's structure

    :param person_id: Id of the person to update in people structure
    :param person: person to update
    :return: updated person structure
    """
    update_person = Person.query.filter(Person.person_id == person_id).one_or_none()

    # If person exists
    if update_person is not None:
        # create person from data passed
        schema = PersonSchema()
        update = schema.load(person, session=db.session).data

        # Set the id to the new person
        update.id = update_person.person_id

        # merge the new object in old and commit it to db
        db.session.merge(update)
        db.session.commit()

        # return updated person
        data = schema.dump(update_person).data

        return data, 200

    # Person does not exist
    else:
        abort(
            404,
            "Person not found for Id: {person_id}".format(person_id=person_id),
        )


def delete(person_id):
    """
    Function for handling requests for deleting a person from people structure

    :param person_id: Id of the person to delete
    :return: 200 on successful delete, 404 if person does not exist
    """
    # Get the person requested
    person = Person.query.filter(Person.person_id == person_id).one_or_none()

    # Check if person exists
    if person is not None:
        db.session.delete(Person)
        db.session.commit()
        return make_response(
            "Person {person_id} deleted".format(person_id=person_id), 200
        )
    # Error if the person does not exist
    else:
        abort(
            404,
            "Person not found for Id:{person_id}".format(person_id=person_id),
        )
