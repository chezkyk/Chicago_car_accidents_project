from flask import Blueprint
from repository.csv_repoaitory import init_db
accident_bp = Blueprint('accident', __name__,url_prefix='/api/accident')

@accident_bp.route('/init_db', methods=['POST'])
def start_db():
    init_db()
    return {'message': 'success'}, 200

@accident_bp.route('/get_accidents_by_area', methods=['GET'])
def get_accidents_by_area():
    pass

@accident_bp.route('/get_accidents_by_area_and_date', methods=['GET'])
def get_accidents_by_area_and_date():
    pass

@accident_bp.route('/get_accidents_by_main_reason', methods=['GET'])
def get_accidents_by_main_reason():
    pass

@accident_bp.route('/get_injury_statistics', methods=['GET'])
def get_injury_statistics():
    pass
