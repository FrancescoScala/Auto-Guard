# from flask import Flask
# from flask_restful import Api
# from report import ReportsResource
#
# app = Flask(__name__)
# api = Api(app)
#
# api.add_resource(ReportsResource, '/reports')


from flask import Flask, request, jsonify

app = Flask(__name__)
@app.route('/echo', methods=['POST'])
def hello():
   return jsonify(request.json)

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=6002, debug=True)
