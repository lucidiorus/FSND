import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
from functools import wraps
from jose import jwt
import json
from flask_cors import CORS
from urllib.request import urlopen

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)


'''
@DONE uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()


## ROUTES
'''
@DONE implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()
    drinks_formatted = [drink.short() for drink in drinks]

    if len(drinks) == 0:
        abort(400)
    
    return jsonify({
      'success': True,
      'drinks' : drinks_formatted,
      'status': 200
    }), 200

    
'''
@DONE implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
@requires_auth('get:drink-detail')
def get_drinks_detail(payload):
    drinks = Drink.query.all()
    drinks_formatted = [drink.long() for drink in drinks]

    if len(drinks) == 0:
        abort(404)
    
    return jsonify({
      'success': True,
      'drinks' : drinks_formatted,
      'status': 200
    }), 200


'''
@DONE implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drink(payload):

    body = request.get_json()
    id = body.get('id', None)
    title = body.get('title', None)
    recipe = body.get('recipe', None)

    drink_formatted = []
    try:
        drink = Drink(id=id, title=title, recipe=json.dumps(recipe))
        drink.insert()
        drink_formatted = [drink.long()]
    except:
        abort(422)
    
        
    return jsonify({
      'success': True,
      'drinks' : drink_formatted,
      'status': 200
    }), 200


'''
@DONE implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drink(payload, id):

    body = request.get_json()
    title = body.get('title', None)
    recipe = body.get('recipe', None)

    drink = Drink.query.filter(Drink.id == id).one_or_none()
    if drink is None:
        abort(404)
    if title is not None:
        drink.title = title
    if recipe is not None:
        drink.recipe = recipe

    drink.update()
    
    drink_formatted = [drink.long()]
    
    return jsonify({
      'success': True,
      'drinks' : drink_formatted,
      'status': 200
    }), 200


'''
@DONE implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):

    drink = Drink.query.filter(Drink.id == id).one_or_none()
    if drink is None:
        abort(404)
    
    drink.delete()
    
    return jsonify({
      'success': True,
      'delete' : id,
      'status': 200
    }), 200


## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@DONE implement error handlers using the @app.errorhandler(error) decorator
'''  


'''
@DONE implement error handler for 404
    error handler should conform to general task above 
'''

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': "Resource Not Found"
    }), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': "Bad Request"
    }), 400
  

@app.errorhandler(422)
def unprocessable_entity(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': "Unprocessable Entity"
    }), 422


@app.errorhandler(405)
def not_allowed(error):
    return jsonify({
      'success': False,
      'error': 405,
      'message': "Method Not Allowed"
    }), 405


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        'success': False,
        'error': error.status_code,
        'message': error.error['description']
    }), error.status_code
