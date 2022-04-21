# Following Moses Maina's Section blog post
from flask import Flask

## Init app

app = Flask(__name__)


# Start the app
if __name__ == '__main__':
	app.run(debug = True)

# --------------------------------------------

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

ma = Marshmallow(app)

# This will make up a sample todo list stored in the SQLite database.
class Todo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100))
	description = db.Column(db.String(400))

	def __init__(self,title,description):
		# Add the data to the instance
		self.title = title
		self.description = description

#  SQLite database: set up a schema that will store our todo.
#  The schema will be called when querying the todos data.
class TodoSchema(ma.Schema):
	class Meta:
		fields = ('id','title','description')

# To initialize the above schema, we have to do it differently for a single todo and multiple todos.
todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)

# --------------------------------------------------------------
# request will be used to get the payload (data sent),
# whereas jsonify will be used to return JSON data.
# CORS and cross_origin for setting up the access policy.
from flask import Flask,request, jsonify
from flask_cors import CORS,cross_origin

# we accept all origins hitting the /api endpoint from which we will expose the API.
CORS(app,resources={r"/api": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

# CREATING A TODO ----------------------------------------------
# From the route, we accept all origins,
# receive the todo’s title and description from the payload,
# save it to the database, and return the saved todo.
@app.route('/api/todo', methods=['POST'])
@cross_origin(origin='*',headers=['content-type'])
def add_todo():
	# get the data
	title = request.json['title']
	description = request.json['description']

	# Create an instance
	new_todo = Todo(title, description)

	# Save the todo in the db
	db.session.add(new_todo)
	db.session.commit()

	# return the created todo
	return todo_schema.jsonify(new_todo)

# GETTING ALL TODOs ----------------------------------------------
# accepting all origins, fetching all saved todos, and returning them.
@app.route('/api/todo', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type'])
def get_todos():
	# get the todos from db
	all_todos = Todo.query.all()
	# get the todos as per the schema
	result = todos_schema.dump(all_todos)
	# return the todos
	return jsonify(result)

# GETTING A SINGLE ROUTE ----------------------------------------------
# accept all origins,
# accept the todo’s id from the URL, get that specific todo, and return it
# Get a single todo
@app.route('/api/todo/<id>', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type'])
def get_todo(id):
	# get a single todo
	todo = Todo.query.get(id)
	# return the todo as per the schema
	return todo_schema.jsonify(todo)

# UPDATING A TODO ROUTE ----------------------------------------------
# accept all origins,
# accept the todo’s id to be updated, get the specific todo and the data,
#  set the new data, save to the database, and return the saved database
# update a todo
@app.route('/api/todo/<id>', methods=['PUT'])
@cross_origin(origin='*',headers=['Content-Type'])
def update_todo(id):
	# get the todo first
	todo = Todo.query.get(id)
	# get the data
	title = request.json['title']
	description = request.json['description']

	# set the data
	todo.title = title
	todo.description = description

	# commit to the database
	db.session.commit()

	# return the new todo as per the schema
	return todo_schema.jsonify(todo)

# UPDATING A TODO ROUTE ----------------------------------------------
# accept the todo’s id to be deleted, getting the todo,
# deleting it from the database, and returning the deleted todo
# Delete a todo
@app.route('/api/todo/<id>', methods=['DELETE'])
@cross_origin(origin='*',headers=['Content-Type'])
def delete_todo(id):
	# get the todo to be deleted
	todo = Todo.query.get(id)

	# delete from the database
	db.session.delete(todo)

	# commit on the database
	db.session.commit()

	# return thr deleted todo as per the schema
	return todo_schema.jsonify(todo)