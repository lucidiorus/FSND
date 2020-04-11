import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


# This method to paginate the questions has been created to make the code less complex
def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app)

  '''
  @DONE: Use the after_request decorator to set Access-Control-Allow
  '''
  # CORS Headers 
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  '''
  @DONE: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    categories = Category.query.all()
    formatted_categories = {category.id:category.type for category in categories}
    
    return jsonify({
      'categories': formatted_categories
    })


  '''
  @DONE: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def get_paginated_questions():
    questions = Question.query.order_by(Question.id).all()
    formatted_questions = paginate_questions(request, questions)
    total_questions = len(formatted_questions)
    current_category = request.args.get('currentCategory', 0, type=int)
    categories = Category.query.all()
    formatted_categories = formatted_categories = {category.id:category.type for category in categories}
    
    # if there are no questions -> Error 404: Resource Not Found
    if total_questions == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': formatted_questions,
      'totalQuestions' : total_questions,
      'categories' : formatted_categories,
      'currentCategory' : current_category
    })

  '''
  @DONE: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      # if there is no question, this launch the 422 exception, Unprocessable Entity
      if question is None:
        abort(404)

      question.delete()
      
      return jsonify({
        'success': True
      })

    except:
      abort(422)


  '''
  @DONE: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():

    body = request.get_json()

    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_difficulty = body.get('difficulty', None)
    new_category = body.get('category', None)

    try:
      question = Question(question=new_question, answer=new_answer, 
      difficulty=new_difficulty, category=new_category)
      question.insert()

      return jsonify({
        'success': True
      })

    # If well formatted question but not possible to process. 422 exception, Unprocessable Entity
    except:
      abort(422)

  '''
  @DONE: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/search', methods=['POST'])
  def get_questions_by_search_term():

    body = request.get_json()

    search_term = body.get('searchTerm', None)
    questions = Question.query.filter(Question.question.ilike('%'+search_term+'%')).all()
    formatted_questions = paginate_questions(request, questions)
    total_questions = len(questions)
    current_category = request.args.get('currentCategory', 0, type=int)

    # if there are no questions -> Error 404: Resource Not Found
    if total_questions == 0:
      abort(404)
    
    return jsonify({
      'success': True,
      'questions': formatted_questions,
      'total_questions' : total_questions,
      'currentCategory' : current_category
    })



  '''
  @DONE: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def get_questions_by_category(category_id):

    questions = Question.query.filter_by(category=category_id).all()
    formatted_question = [question.format() for question in questions]
    total_questions = len(questions)
    current_category = category_id

    # if there are no questions -> Error 404: Resource Not Found
    if total_questions == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': formatted_question,
      'total_questions': total_questions,
      'current_category': current_category
    })


  '''
  @DONE: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def get_quizz_question():

    body = request.get_json()

    previous_questions = body.get('previous_questions', None)
    quiz_category = body.get('quiz_category', None)
    quiz_category_id = quiz_category['id']

    if quiz_category_id == 0:
      new_question = Question.query.filter(Question.id.notin_(previous_questions)).first()
    else:
      new_question = Question.query.filter(Question.id.notin_(previous_questions)).filter_by(category=quiz_category_id).first()

    # if there is no question -> Error 404: Resource Not Found
    if new_question is None:
      abort(404)
      
    return jsonify({
      'success': True,
      'question': new_question.format()
    })


  '''
  @DONE: 
  Create error handlers for all expected errors 
  including 404 and 422. 
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



  return app

    