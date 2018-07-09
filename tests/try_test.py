from pymongo import MongoClient
from bson import ObjectId


def concurrency_update():
    """Test concurrency update

    Test $inc

    :return:
    """
    mc = MongoClient()
    col = mc['blog']['articles']

    _id = '5b432a42f04705565525529d'
    col.update_one(
        {'_id': ObjectId(_id)},
        {'$set': {'views': 0}}
    )

    for x in range(10000):
        col.update_one(
            {'_id': ObjectId(_id)},
            {'$inc': {'views': 1}}
        )


if __name__ == '__main__':
    concurrency_update()
