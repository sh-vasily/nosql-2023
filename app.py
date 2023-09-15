from flask import Flask

from routes import hello_world, save, get_all_students

app = Flask(__name__)

app.add_url_rule('/', view_func=hello_world, methods=['GET'])
app.add_url_rule('/students', view_func=get_all_students, methods=['GET'])
app.add_url_rule('/', view_func=save, methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True)
