import os

from flask import Flask, request
from pymongo import MongoClient

app = Flask(__name__)


class Person:
    def __init__(self, id, frst_name, last_name, date_of_birth, addresses=None, family_members=None):
        self.id = id
        self.first_name = frst_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.addresses = [Address.from_json_dict(x) for x in addresses]
        self.family_members = [FamilyMember.from_json_dict(x) for x in family_members]

    @staticmethod
    def from_json_dict(json_dict):
        return Person(**json_dict)


class FamilyMember(object):
    def __init__(self, id_, relation):
        self.id = id_,
        self.relation = relation

    @staticmethod
    def from_json_dict(json_dict):
        return FamilyMember(**json_dict)


class Address:
    def __init__(self, city, street, house_number):
        self.city = city
        self.street = street
        self.house_number = house_number

    @staticmethod
    def from_json_dict(json_dict):
        return Address(**json_dict)


@app.route('/people', methods=['GET', 'POST'])
def people():
    if request.method == 'GET':
        mongo = MongoClient(os.environ['MONGO_HOST'], os.environ['MONGO_PORT'])
        db = mongo.get_database('default')
        people = db.get_collection('people')
        return list(people.find())

    if request.method == 'POST':
        mongo = MongoClient(os.environ['MONGO_HOST'], os.environ['MONGO_PORT'])
        db = mongo.get_database('default')
        people = db.get_collection('people')
        people.insert_one(request.json)
        return 'OK'


@app.route('/people/first_name/<first_name>')
def get_people_by_first_name(first_name):
    mongo = MongoClient(os.environ['MONGO_HOST'], os.environ['MONGO_PORT'])
    db = mongo.get_database('default')
    people = db.get_collection('people')
    return list(people.find({'first_name': first_name}))


@app.route('/people/last_name/<last_name>')
def get_people_by_last_name(first_name):
    mongo = MongoClient(os.environ['MONGO_HOST'], os.environ['MONGO_PORT'])
    db = mongo.get_database('default')
    people = db.get_collection('people')
    return list(people.find({'last_name': first_name}))


@app.route('/people/current_city/<city>')
def get_people_by_current_city(city):
    mongo = MongoClient(os.environ['MONGO_HOST'], os.environ['MONGO_PORT'])
    db = mongo.get_database('default')
    people = db.get_collection('people')
    return list(people.find({'addresses.0': { '$elemMatch': { 'city': city}}}))


@app.route('/people/lived_at/<city>')
def get_people_by_lived_at_city(city):
    mongo = MongoClient(os.environ['MONGO_HOST'], os.environ['MONGO_PORT'])
    db = mongo.get_database('default')
    people = db.get_collection('people')
    return list(people.find({'addresses': {'$elemMatch': {'city': city}}}))


@app.route('/people/<id>', methods=['GET', 'POST', 'DELETE'])
def person(id_):
    mongo = MongoClient(os.environ['MONGO_HOST'], os.environ['MONGO_PORT'])
    db = mongo.get_database('default')
    people = db.get_collection('people')

    person = Person.from_json_dict(people.find_one({'id': id_}))

    if request.method == 'GET':
        return person

    if request.method == 'DELETE':
        people.delete_one({'id': id_})
        return 'OK'

    if request.method == 'POST':
        updated_person = request.json
        for k, v in updated_person:
            if k in ['family_members', 'addresses']:
                attr = getattr(person, k, [])
                attr.extend(v)
                setattr(person, k, attr)
            else:
                setattr(person, k, v)
        return 'OK'


@app.route('/people/<id>/family_members')
def person(id_):
    mongo = MongoClient(os.environ['MONGO_HOST'], os.environ['MONGO_PORT'])
    db = mongo.get_database('default')
    people = db.get_collection('people')

    person = Person.from_json_dict(people.find_one({'id': id_}))

    return people.find({'_id': {'$in': [x.id for x in person.family_members]}})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
