from dotenv import load_dotenv
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from flask_cors import CORS
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.getenv("DB_URI")

#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] =  DATABASE_URL   

# create an object of SQLAlchemy named as db, which will handle our ORM-related activities.
db = SQLAlchemy(app)

###Models####
# declare a class as LetsTodo which will hold the schema for the todos table:
class LetsTodo(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self
    def __init__(self,title):
        self.title = title
    def __repr__(self):
        return '' % self.id\
# instructs the application to create all the tables and database specified in the application.
db.create_all()


class LetsTodoSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = LetsTodo
        sqla_session = db.session
    id = fields.Number(dump_only=True)
    title = fields.String(required=True)

@app.route('/todos', methods = ['GET'])
def getTodos():
    get_todos = LetsTodo.query.all()
    letstodo_schema = LetsTodoSchema(many=True)
    todos = letstodo_schema.dump(get_todos)
    return make_response(jsonify({"todo": todos}))



@app.route('/todos', methods = ['POST'])
def createTodos():
    data = request.get_json()
    # print(data)
    letstodo_schema = LetsTodoSchema()
    todo = letstodo_schema.load(data)
    result = letstodo_schema.dump(todo.create())
    return make_response(jsonify({"todo": result}),200)
    # return jsonify(data)


@app.route('/todos/<id>', methods = ['DELETE'])
def deleteTodosById(id):
    get_todo = LetsTodo.query.get(id)
    db.session.delete(get_todo)
    db.session.commit()
    return make_response("",204)



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=port)