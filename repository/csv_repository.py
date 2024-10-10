import csv
from utils.help_util_data import get_week_range,parse_date,safe_int
from pymongo import UpdateOne
from config import *
from database.connect import day_collection,week_collection,month_collection

def read_csv(csv_path):
   with open(csv_path, 'r') as file:
       csv_reader = csv.DictReader(file)
       for row in csv_reader:
           yield row

def create_update_operation(doc_key, base_doc, injuries, factor):
    '''
    Constructs an action that will be used to update the documents in Mongo based on the information about the accident.
    If doc_key (the document identifier) does not exist in the dictionary,
    the function defines it and adds initial values for the update.
    If it already exists, it updates the existing values.
    '''
    if doc_key not in base_doc:
        base_doc[doc_key] = {
            'update': {
                '$setOnInsert': base_doc[doc_key]['update']['$setOnInsert'],
                '$inc': {
                    'total_accidents': 1,
                    'injuries.total': injuries['total'],
                    'injuries.fatal': injuries['fatal'],
                    'injuries.non_fatal': injuries['non_fatal'],
                    f'contributing_factors.{factor}': 1
                }
            }
        }
    else:
        # Ensure $inc exists
        if '$inc' not in base_doc[doc_key]['update']:
            base_doc[doc_key]['update']['$inc'] = {
                'total_accidents': 0,
                'injuries.total': 0,
                'injuries.fatal': 0,
                'injuries.non_fatal': 0
            }

        # Update the counts
        base_doc[doc_key]['update']['$inc']['total_accidents'] += 1
        base_doc[doc_key]['update']['$inc']['injuries.total'] += injuries['total']
        base_doc[doc_key]['update']['$inc']['injuries.fatal'] += injuries['fatal']
        base_doc[doc_key]['update']['$inc']['injuries.non_fatal'] += injuries['non_fatal']

        # Update contributing factors
        factor_key = f'contributing_factors.{factor}'
        if factor_key not in base_doc[doc_key]['update']['$inc']:
            base_doc[doc_key]['update']['$inc'][factor_key] = 1
        else:
            base_doc[doc_key]['update']['$inc'][factor_key] += 1

def process_batch_updates(collection, updates):
    '''
    The function performs all group updates (batch updates) in the given data collection (daily, weekly or monthly).
    Creates UpdateOne objects based on the updates and performs the operation in MongoDB using bulk_write.
    '''
    if not updates:
        return
    operations = [
        UpdateOne(
            update['filter'],
            update['update'],
            upsert=True
        ) for update in updates.values()
    ]
    result = collection.bulk_write(operations)




def ensure_indexes():

    # Drop existing indexes
    day_collection.drop_indexes()
    week_collection.drop_indexes()
    month_collection.drop_indexes()

    # Create new indexes
    day_collection.create_index([("date", 1), ("area", 1)], unique=True)
    week_collection.create_index([("week_start", 1), ("week_end", 1), ("area", 1)], unique=True)
    month_collection.create_index([("year", 1), ("month", 1), ("area", 1)], unique=True)


def init_accidents():

    # Drop existing collections and recreate indexes
    day_collection.drop()
    week_collection.drop()
    month_collection.drop()

    ensure_indexes()

    daily_updates = {}
    weekly_updates = {}
    monthly_updates = {}

    BATCH_SIZE = 1000
    processed_count = 0

    for row in read_csv(CSV_20K_URI):
        crash_date = parse_date(row['CRASH_DATE'])
        area = row['BEAT_OF_OCCURRENCE']
        factor = row['PRIM_CONTRIBUTORY_CAUSE']

        injuries = {
            'total': safe_int(row['INJURIES_TOTAL']),
            'fatal': safe_int(row['INJURIES_FATAL']),
            'non_fatal': safe_int(row['INJURIES_TOTAL']) - safe_int(row['INJURIES_FATAL'])
        }

        # Daily updates
        daily_key = f"{crash_date.strftime('%Y-%m-%d')}_{area}"
        if daily_key not in daily_updates:
            daily_updates[daily_key] = {
                'filter': {'date': crash_date, 'area': area},
                'update': {
                    '$setOnInsert': {'date': crash_date, 'area': area},
                    '$inc': {
                        'total_accidents': 0,
                        'injuries.total': 0,
                        'injuries.fatal': 0,
                        'injuries.non_fatal': 0
                    }
                }
            }
        create_update_operation(daily_key, daily_updates, injuries, factor)

        # Weekly updates
        week_start, week_end = get_week_range(crash_date)
        weekly_key = f"{week_start}_{week_end}_{area}"
        if weekly_key not in weekly_updates:
            weekly_updates[weekly_key] = {
                'filter': {'week_start': str(week_start), 'week_end': str(week_end), 'area': area},
                'update': {
                    '$setOnInsert': {'week_start': str(week_start), 'week_end': str(week_end), 'area': area},
                    '$inc': {
                        'total_accidents': 0,
                        'injuries.total': 0,
                        'injuries.fatal': 0,
                        'injuries.non_fatal': 0
                    }
                }
            }
        create_update_operation(weekly_key, weekly_updates, injuries, factor)

        # Monthly updates
        monthly_key = f"{crash_date.year}_{crash_date.month}_{area}"
        if monthly_key not in monthly_updates:
            monthly_updates[monthly_key] = {
                'filter': {'year': str(crash_date.year), 'month': str(crash_date.month), 'area': area},
                'update': {
                    '$setOnInsert': {'year': str(crash_date.year), 'month': str(crash_date.month), 'area': area},
                    '$inc': {
                        'total_accidents': 0,
                        'injuries.total': 0,
                        'injuries.fatal': 0,
                        'injuries.non_fatal': 0
                    }
                }
            }
        create_update_operation(monthly_key, monthly_updates, injuries, factor)

        processed_count += 1
        if processed_count % BATCH_SIZE == 0:
            process_batch_updates(day_collection, daily_updates)
            process_batch_updates(week_collection, weekly_updates)
            process_batch_updates(month_collection, monthly_updates)
            daily_updates = {}
            weekly_updates = {}
            monthly_updates = {}


    # Process remaining updates
    process_batch_updates(day_collection, daily_updates)
    process_batch_updates(week_collection, weekly_updates)
    process_batch_updates(month_collection, monthly_updates)