from flask import Blueprint,request
from repository.csv_repoaitory import *
from repository.accident import fetch_total_accidents_from_db
from database.connect import month_collection,week_collection,day_collection
from services.accident import *
accident_bp = Blueprint('accident', __name__,url_prefix='/api/accident')

@accident_bp.route('/init_db', methods=['POST'])
def start_db():
    init_accidents()
    return {'message': 'success'}, 200

@accident_bp.route('/get_accidents_by_area/<string:beat>', methods=['GET'])
def get_accidents_by_area(beat):
    if beat is None:
        return {'error': 'beat (area) was NONE'}, 400

    total_accidents = fetch_total_accidents_from_db(beat)

    return {'total_accidents': total_accidents}, 200

@accident_bp.route('/get_accidents_by_area_and_date', methods=['GET'])
def get_accidents_by_area_and_date():
    beat = request.args.get('beat')
    time_type = request.args.get('time_period')
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    if not beat or not time_type:
        return {'error': 'beat and time_period parameters are required'}, 400
    total = accidents_by_area_and_date_service(beat,time_type,start_date_str,end_date_str)
    if total is None:
        return {'error': 'Invalid time_period parameter'}, 400
    return {'total_accidents': total}, 200


@accident_bp.route('/get_accidents_by_main_reason/<string:beat>', methods=['GET'])
def get_accidents_by_main_reason(beat):
        if not beat:
            return {'error': 'beat parameter is required'}, 400

        causes = accidents_by_main_reason_service(beat)
        if causes is None:
            return {'error': 'invalid beat parameter'}, 400
        return {'area': beat, 'causes': causes}, 200

@accident_bp.route('/get_injury_statistics/<string:beat>', methods=['GET'])
def get_injury_statistics(beat):

    if not beat:
        return {'error': 'beat parameter is required'}, 400

    response = get_injury_statistics_service(beat)
    if response is None:
        return {'error': 'No data found for the specified area'}, 404
    return response, 200
