"""
People module supporting Rest actions for people collection
"""

# System modules
from datetime import datetime

# 3rd party modules
from flask import make_response, abort


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


# Data to server with API
PEOPLE = {
    "Farrell": {
        "fname": "Doug",
        "lname": "Farrell",
        "timestamp": get_timestamp()
    },
    "Brockman": {
        "fname": "Kent",
        "lname": "Brockman",
        "timestamp": get_timestamp(),
    },
    "Easter": {
        "fname": "Bunny",
        "lname": "Easter",
        "timestamp": get_timestamp(),
    },
}


def read_all():
    """
    Function for responding to request for /api/people with complete list of people

    :return:    json string of list of people
    """
    return [PEOPLE[key] for key in sorted(PEOPLE.keys())]


def read_one(lname):
    """
    Function for responding to requests for /api/people/{lname} with one matching person

    :param lname: last name of person to find
    :return:    person matching last name
    """
    if lname in PEOPLE:
        person = PEOPLE.get(lname)
    else:
        abort(404, "Person with last name {lname} not found".format(lname=lname))

    return person


def create(person):
    """
    Function responding to requests for creating a new person

    :param person:  person to create in people's structure
    :return: 201 on success, 406 if person already exists
    """
    lname = person.get("lname", None)
    fname = person.get("fname", None)

    if lname not in PEOPLE and lname is not None:
        PEOPLE[lname] = {
            "lname": lname,
            "fname": fname,
            "timestamp": get_timestamp()
        }
        return PEOPLE[lname], 201
    else:
        abort(
            406,
            'Person with last name {lname} already exists'.format(lname=lname)
        )


def update(lname, person):
    """
    Function for updating existing person in people's structure

    :param lname: Last name of person to update the people structure
    :param person: person to update
    :return: updated person structure
    """
    # Check if person exists
    if lname in PEOPLE:
        PEOPLE[lname]["fname"] = person.get("fname")
        PEOPLE[lname]["timestamp"] = get_timestamp()

        return PEOPLE[lname]
    # Person does not exist
    else:
        abort(404, "Person with last name {lname} not found".format(lname=lname))


def delete(lname):
    """
    Function for handling requests for deleting a person from people structure

    :param lname: lastname of person to delete
    :return: 200 on successfull delete, 404 if person does not exist
    """
    # Check if person exists
    if lname in PEOPLE:
        del PEOPLE[lname]
        return make_response("{lname} successfully deleted".format(lname=lname), 200)
    # Error if the person does not exist
    else:
        abort(404, "Person with last name {lname} not found".format(lname=lname))
