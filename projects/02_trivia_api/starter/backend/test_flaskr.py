import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres','EresTonto','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': "question test",
            'answer': "answer test",
            'category': 1,
            'difficulty': 3 
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    DONE
    Write at least one test for each test for successful operation and for expected errors.
    """
    # get questions without indicating pagination (default=1) should return success response
    def test_200_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['totalQuestions'])


    # get questions with pagination non existing should return 404 response
    def test_404_get_paginated_questions(self):
        res = self.client().get('/questions?page=9999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], "Resource Not Found")


    # delete existing question should return success response
    def test_200_delete_existing_question(self):
        res = self.client().delete('/questions/5')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEquals(data['success'], True)

    
    # delete non existing question should return 404 response
    def test_404_delete_non_existing_question(self):
        res = self.client().delete('/questions/999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable Entity")


    # post non existing question should return success response
    def test_200_post_non_existing_question(self):
        res = self.client().post('/questions', json={'question':"question non existing", 
        'answer': "non existing answer", 'difficulty': 3, 'category': "3"})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    # post question using wrong parameter (category non existing) should return 422 response
    def test_422_post_question_with_bad_parameters(self):
        res = self.client().post('/questions', json={'question':"question non existing", 
        'answer': "non existing answer", 'difficulty': 10, 'category': "10"})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable Entity")

    
    # get questions using existing search term should return success response
    def test_200_get_question_by_search_term(self):
        res = self.client().post('/search', json={'searchTerm':"the"})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    # get questions using non existing search term should return 404 response
    def test_404_get_question_by_inexisten_search_term(self):
        res = self.client().post('/search', json={'searchTerm':"supercalifragilistico"})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], "Resource Not Found")

    
    # get questions by existing category should return success response
    def test_200_get_questions_by_category(self):
        res = self.client().get('/categories/5/questions')
        
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    # get questions by non existing category should return 404 response
    def test_404_get_questions_by_inexistent_category(self):
        res = self.client().get('/categories/99/questions')
        
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], "Resource Not Found")


    # get quiz questions using correct request body should return success response
    def test_200_get_quizzes(self):
        res = self.client().post('/quizzes', json={'previous_questions':[], 'quiz_category': {'id':1,'type':'Science'}})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    # get quiz questions using wrong request parameters should return 404 response
    def test_404_get_quizzes_of_inexistent_category(self):
        res = self.client().post('/quizzes', json={'previous_questions':[], 'quiz_category': {'id':99,'type':'Non existing'}})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], "Resource Not Found")


    # get categories should return success response
    def test_200_get_categories(self):
        res = self.client().get('/categories')
        
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
 

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()