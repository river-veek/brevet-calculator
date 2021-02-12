# Laptop Service

from flask import Flask
from flask_restful import Resource, Api

# Instantiate the app
app = Flask(__name__)
api = Api(app)

class Laptop(Resource):
    def get(self):
        return {
            'Laptops': ['Mac OS', 'Dell', 
            'Windozzee',
	    'Yet another laptop!',
	    'Yet yet another laptop!'
            ]
        }

class ListAll(Resource):
    def get(self):
        return {'Times': ["Time 1",
                         "Time 2",
                         "Time 3",
                         "Time 4"]
                }

# Create routes
# Another way, without decorators

api.add_resource(Laptop, '/')
api.add_resource(ListAll, '/listAll')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
