from http import HTTPStatus

from flask import Flask, request
from flask_restful import Resource, Api 

from models import Mobil

app = Flask(__name__)
api = Api(app)        

class Recommendation(Resource):

    def post(self):
        criteria = request.get_json()
        validCriteria = ['nmobil', 'cc', 'bensin', 'daya', 'torsi', 'harga']
        mobil = Mobil()

        if not criteria:
            return 'criteria is empty', HTTPStatus.BAD_REQUEST.value

        if not all([v in validCriteria for v in criteria]):
            return 'criteria is not found', HTTPStatus.UNPROCESSABLE_ENTITY.value

        recommendations = mobil.get_recs(criteria)
        ranked_results = [{ "peringkat": i + 1,"Mobil": mobil.mobil_data_dict[rec[0]], "skor": rec[1]} for i, rec in enumerate(recommendations.items())]

        return {
            'WP ': "WeightedProduct",
            'alternatif': ranked_results
        }, HTTPStatus.OK.value


api.add_resource(Recommendation, '/recommendation')

if __name__ == '__main__':
    app.run(port='5005', debug=True)
