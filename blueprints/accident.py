from flask import Blueprint,request
from repository.csv_repoaitory import init_db
from repository.accident import fetch_total_accidents_from_db
from database.connect import month_collection,week_collection,day_collection

accident_bp = Blueprint('accident', __name__,url_prefix='/api/accident')

@accident_bp.route('/init_db', methods=['POST'])
def start_db():
    init_db()
    return {'message': 'success'}, 200

@accident_bp.route('/get_accidents_by_area', methods=['GET'])
def get_accidents_by_area():
    beat = request.args.get('beat')

    if not beat:
        return {'error': 'beat (area) was NONE'}, 400

    total_accidents = fetch_total_accidents_from_db(beat)

    return {'total_accidents': total_accidents}, 200

@accident_bp.route('/get_accidents_by_area_and_date', methods=['GET'])
def get_accidents_by_area_and_date():
    pass

@accident_bp.route('/get_accidents_by_main_reason', methods=['GET'])
def get_accidents_by_main_reason():
    pass

@accident_bp.route('/get_injury_statistics', methods=['GET'])
def get_injury_statistics():
    pass
