import dns
from pymongo import MongoClient, ReturnDocument
import config


def fetch_database():
    CONNECTION_STRING = config.DB_STRING
    client = MongoClient(CONNECTION_STRING)

    test_db = client['hu-announcement-db']
    user_configs = test_db['user_configs']

    return user_configs


def find_subscribers(departmentName):
    user_configs = fetch_database()
    users = user_configs.find({"departments": departmentName})

    subscribedUsers = []
    for user in users:
        subscribedUsers.append(user['user_id'])

    return subscribedUsers


def find_subscriptions(user_id):
    user_configs = fetch_database()
    user = user_configs.find_one({'user_id': user_id})

    return user['departments']


def find_all_users():
    user_configs = fetch_database()
    users = user_configs.find()
    user_IDs = []

    for user in users:
        user_IDs.append(user['user_id'])

    return user_IDs


def add_user(user_id, first_name, last_name):
    user_configs = fetch_database()
    user = user_configs.find_one({'user_id': user_id})

    if user is None:
        user_info = {'user_id': user_id, 'first_name': first_name, 'last_name': last_name, 'departments': [], 'language': 'tr'}
        user_configs.insert_one(user_info)
        print(f"{user_id} has been successfully enrolled the database!")


def update_subscriptions(user_id, subscribedDepartments):
    user_configs = fetch_database()

    user_configs.find_one_and_update({'user_id': user_id},
                                     {'$set': {'departments': subscribedDepartments}},
                                     return_document=ReturnDocument.AFTER)

    print(f"Subscriptions has been updated successfully for {user_id}!")