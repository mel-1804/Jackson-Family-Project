"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

John={
    'first_name': 'John',
    'last_name': 'Jackson',
    'age': 33,
    'lucky_numbers':[7, 13, 22]
}

Jane={
    'first_name': 'Jane',
    'last_name': 'Jackson',
    'age': 35,
    'lucky_numbers':[10, 14, 3]
}

Jimmy={
    'first_name': 'Jimmy',
    'last_name': 'Jackson',
    'age': 5,
    'lucky_numbers': [1]
}


jackson_family.add_member(John)
jackson_family.add_member(Jane)
jackson_family.add_member(Jimmy)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    member = jackson_family.get_member(id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"message": "Member not found"}), 404

@app.route('/addMember', methods=['POST'])
def add_member():
    member = request.json
    print(member)
    jackson_family.add_member(member)
    if member is not None:
        return "member created", 200

@app.route('/deleteMember/<int:id>', methods=['DELETE'])
def delete_member(id):
    member = jackson_family.get_member(id)

    if member:
        jackson_family.delete_member(id)
        return jsonify({"message": f"Member deleted"}), 200
    else:
        return jsonify({"message": f"Not found"}), 404


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
