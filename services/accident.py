from database.connect import day_collection, week_collection, month_collection
from utils.help_util_data import parse_date_bluprint
from repository.accident import accidents_by_area_and_date_from_db

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

