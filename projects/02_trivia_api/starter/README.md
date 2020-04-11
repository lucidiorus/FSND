# Full Stack API Final Project

This project is a trivia app created for Udacity employees and students. 
At the beginning the code was uncompleted, indicating different tasks to be done to complete the project. After creating, completing, and finishing all these task, the result is what you are reading right now.
The goal was to be able to understand the use and creation of RESTful APIs and their proper documentation.

## Structure and final code

The structure of the project has been remained. The only files that have been modified have been those with #TODO taks, that now are marked as #DONE.

Most of the previous comments also remain in the code to help the reviewer the job of analyzing the result but also new comments have been added where needed. As the operations of the methods was simple, it is easy to understand most of them just reading the names of methods and variables.

All backend code follows PEP8 style guidelines.


## Getting Started

### Pre-requisities and Local Development

Developers using this project should already have Python2, pip and node installed on their local machines

A virual environment has been created and is in the main folder inside the folder 'venv'

### Backend

To install all the requirements run `pip install requirements.txt` from the backend folder

To run the application run the following commands:
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the __init__.py file in our flaskr folder.

The application is run on http://127.0.0.1:5000/ by default and is a proxy in the frontend configuration.


#### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 


#### Database Setup

Before anything you should set the database config in the models.py file with the variables database_name and database_path

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Frontend

#### Installing Node and NPM

This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

#### Installing project dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

#### Running Your Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.

```bash
npm start
```


### Testing
Before anything you should set the database changing the self.database_path in "test_flaskr.py

To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```


## API Reference

### Getting Started

* Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `htto:/127.0.0.1:5000`, which is set as a proxy in the frontend configuration.
* Authentication: This version of the application does not requiere authentication or API keys

### Error Handling

Errors are returned as JSON objects in the following format:
```
{
    'success': False,
    'error': 400,
    'message' : "Bad Request"
}
```

The API will return three error types when request fail:
* 400: Bad Request
* 404: Resource Not Found
* 422: Not Processable


## Endpoints

### GET /questions

* General:
    * Return a list of question objects, success value, total number of questions, list of categories and current category
    * Resulst are paginated in groups of 10. Include a request argument to choose a page number
* Sample: `curl http://127:0.0.1:5000/questions`
```
{
"categories": {
1: "Science",
2: "Art",
3: "Geography",
4: "History",
5: "Entertainment",
6: "Sports"
},
"currentCategory": 0,
"questions": [
  {
"answer": "Maya Angelou",
"category": 4,
"difficulty": 2,
"id": 5,
"question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
},
  {
"answer": "Edward Scissorhands",
"category": 5,
"difficulty": 3,
"id": 6,
"question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
},
  {
"answer": "Muhammad Ali",
"category": 4,
"difficulty": 1,
"id": 9,
"question": "What boxer's original name is Cassius Clay?"
},
  {
"answer": "Brazil",
"category": 6,
"difficulty": 3,
"id": 10,
"question": "Which is the only team to play in every soccer World Cup tournament?"
}],
"success": true,
"totalQuestions": 10
```

### POST /questions

* General:
    * Create a new question using the question field, answer, difficulty and category.  
    Return success value and the id of the question created
* Sample: `curl http://127:0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"question1", "answer":"answer1", "category":"1", "difficulty":"5"}'`
```
{
  "id": 30, 
  "success": true
}
```

### DELETE /questions/{question_id}

* General:
    * Delete a question using the question id. Return success value and the id of the question deleted
* Sample: `curl -X DELETE http://127:0.0.1:5000/questions/18`
```
{
"id": 18,
"success": true
}

```

### POST /search

* General:
    * Search a question of group of questions which contains the search term included in the body of the request. Return success value, a bundle of questions, the list of categories and the current category
* Sample: `curl http://127:0.0.1:5000/search -X POST -H "Content-Type: application/json" -d '{"searchTerm":"lake"}'`
```
{
"currentCategory": 0,
"questions": [
  {
"answer": "Lake Victoria",
"category": 3,
"difficulty": 2,
"id": 13,
"question": "What is the largest lake in Africa?"
}
],
"success": true,
"total_questions": 1
}
```


### GET /categories/<int:category_id>/questions

* General:
    * Get all the questions in a specific category. Return success value, a bundle of questions, the number of questions returned and the current category
* Sample: `curl http://127:0.0.1:5000/categories/3/questions`
```
{
"current_category": 3,
"questions": [
  {
"answer": "Lake Victoria",
"category": 3,
"difficulty": 2,
"id": 13,
"question": "What is the largest lake in Africa?"
},
  {
"answer": "The Palace of Versailles",
"category": 3,
"difficulty": 3,
"id": 14,
"question": "In which royal palace would you find the Hall of Mirrors?"
},
  {
"answer": "Agra",
"category": 3,
"difficulty": 2,
"id": 15,
"question": "The Taj Mahal is located in which Indian city?"
}
],
"success": true,
"total_questions": 3
}
```


### POST /quizzes

* General:
    * Returns the next question of the quiz, avoiding to give a question already used. Return success value and the following question
* Sample: `curl http://127:0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions":[], "quiz_category": { "id":0, "type":"All" }}'`
```
{
"question": {
"answer": "Maya Angelou",
"category": 4,
"difficulty": 2,
"id": 5,
"question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
},
"success": true
}
```