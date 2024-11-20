from flask import Flask
from flask_restful import Api
from report import ReportsResource

app = Flask(__name__)
api = Api(app)

api.add_resource(ReportsResource, '/reports')

if __name__ == '__main__':
    app.run(debug=True)
