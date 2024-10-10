from database.connect import day_collection, week_collection, month_collection
from utils.help_util_data import parse_date_bluprint
from repository.accident import *

def accidents_by_area_and_date_service(beat,time_type,start_date_str,end_date_str):
    start_date = parse_date_bluprint(start_date_str) if start_date_str else None
    end_date = parse_date_bluprint(end_date_str) if end_date_str else None

    match time_type:
        case 'day':
            collection = day_collection
            query = {'area': beat}
            if start_date and end_date:
                query['date'] = {'$gte': start_date, '$lte': end_date}
        case 'week':
            collection = week_collection
            query = {'area': beat}
            if start_date and end_date:
                query['week_start'] = {'$gte': str(start_date)}
                query['week_end'] = {'$lte': str(end_date)}
        case 'month':
            collection = month_collection
            query = {'area': beat}
            if start_date and end_date:
                query['year'] = {'$gte': str(start_date.year), '$lte': str(end_date.year)}
                query['month'] = {'$gte': str(start_date.month), '$lte': str(end_date.month)}
        case _:
            return None

    total_accidents = accidents_by_area_and_date_from_db(query,collection)
    return {'total_accidents': total_accidents}, 200

def accidents_by_main_reason_service(beat):
    pipeline = [
        {'$match': {'area': beat}},
        {'$group': {
            '_id': None,
            'contributing_factors': {
                '$push': {
                    'k': {'$objectToArray': '$contributing_factors'},
                }
            }
        }},
        {'$unwind': '$contributing_factors'},
        {'$unwind': '$contributing_factors.k'},
        {'$group': {
            '_id': '$contributing_factors.k.k',
            'count': {'$sum': '$contributing_factors.k.v'}
        }},
        {'$sort': {'count': -1}}
    ]
    results = accidents_by_main_reason_from_db(pipeline)

    if not results:
        return None


    causes = {str(item['_id']): item['count'] for item in results}
    return causes
def get_injury_statistics_service(beat):

    pipeline = [
        {'$match': {'area': beat}},
        {'$group': {
            '_id': None,
            'total_injuries': {'$sum': '$injuries.total'},
            'fatal_injuries': {'$sum': '$injuries.fatal'},
            'non_fatal_injuries': {'$sum': '$injuries.non_fatal'},
            'accidents': {
                '$push': {
                    'date': '$date',
                    'injuries': '$injuries'
                }
            }
        }}
    ]

    result = get_injury_statistics_from_db(pipeline)

    if not result:
        return None

    stats = result[0]
    response = {
        'area': beat,
        'statistics': {
            'total_injuries': stats['total_injuries'],
            'fatal_injuries': stats['fatal_injuries'],
            'non_fatal_injuries': stats['non_fatal_injuries']
        },
        'accidents': stats['accidents']
    }
    return response
