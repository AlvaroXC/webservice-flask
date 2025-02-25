import numpy as np
import pandas as pd
from sklearn.preprocessing import KBinsDiscretizer
import json
from flask import Flask, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

@app.route('/')
def home(): 
    return "<h1>Flask Endpoint</h1>"

@app.route('/api/test')
def test():
    return jsonify({
        'name': 'Alvaro',
        'email': 'alvaroxool@gmail.com'
    })

class Discretizacion(Resource):
    def post(self):
        json_data = request.get_json()

        array_numbers = json_data['numbers']
        bins = json_data['bins']

        data = np.array(array_numbers).reshape(-1,1).astype(float)
        discretizer = KBinsDiscretizer(n_bins=bins, encode='ordinal', strategy='uniform')
        data_disc = discretizer.fit_transform(data)

        df = pd.DataFrame({
            'Valor Original': data.flatten(),
            'Intervalo': data_disc.flatten()
        })
        df_json = df.to_json(orient='records')

        return df_json
    

api.add_resource(Discretizacion, '/discretizacion')

if __name__ == '__main__':
    app.run(debug=True)

