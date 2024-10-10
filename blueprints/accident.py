from flask import Blueprint

accident_bp = Blueprint('accident', __name__,url_prefix='/api/accident')

@accident_bp.route('', methods=['GET'])
def get_accidents_by_area():
    pass

@accident_bp.route('', methods=['GET'])
def get_accidents_by_area_and_date():
    pass

@accident_bp.route('', methods=['GET'])
def get_accidents_by_main_reason():
    pass

@accident_bp.route('', methods=['GET'])
def get_injury_statistics():
    pass
