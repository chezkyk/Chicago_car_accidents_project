import pytest
from flask import Flask
from blueprints.accident import accident_bp

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(accident_bp)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_start_db(client):
    response = client.post('/api/accident/init_db')
    assert response.status_code == 200
    assert response.json == {'message': 'The data has been successfully entered into the database.'}

def test_get_accidents_by_area(client):
    response = client.get('/api/accident/get_accidents_by_area/225')
    assert response.status_code == 200
    assert 'total_accidents' in response.json
    
    
def test_get_accidents_by_area_with_missing_parameter(client):
    # parameter beat is missing
    response = client.get('/api/accident/get_accidents_by_area')
    assert response.status_code == 404


def test_get_accidents_by_area_and_date(client):
    response = client.get('/api/accident/get_accidents_by_area_and_date?beat=123&time_period=day&start_date=2020-10-10&end_date=2024-10-10')
    assert response.status_code == 200
    assert 'total_accidents' in response.json
    
def test_get_accidents_by_area_and_date_with_missing_parameter(client):
    # parameter beat is missing
    response = client.get('/api/accident/get_accidents_by_area_and_date?beat=123&start_date=2020-10-10&end_date=2024-10-10')
    assert response.status_code == 404

def test_get_accidents_by_main_reason(client):
    response = client.get('/api/accident/get_accidents_by_main_reason/225')
    assert response.status_code == 200
    data = response.json
    assert 'area' in data
    assert 'causes' in data
    assert isinstance(data['causes'], dict)


def test_get_accidents_by_main_reason_with_missing_parameter(client):
    # parameter beat is missing
    response = client.get('/api/accident/get_accidents_by_main_reason')
    assert response.status_code == 404

def test_get_injury_statistics(client):
    response = client.get('/api/accident/get_injury_statistics/225')
    assert response.status_code == 200
    data = response.json
    assert 'area' in data
    assert 'statistics' in data
    assert 'accidents' in data
    assert isinstance(data['accidents'], list)
    if len(data['accidents']) > 0:
        first_entry = data['accidents'][0]
        assert 'date' in first_entry
        assert 'injuries' in first_entry
        assert isinstance(first_entry['injuries'], dict)

def test_get_injury_statistics_with_missing_parameter(client):
    # parameter beat is missing
    response = client.get('/api/accident/get_injury_statistics')
    assert response.status_code == 404
