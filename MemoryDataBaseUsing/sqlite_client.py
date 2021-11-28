from sqlite3 import connect
from json import dumps

from TrackParallelTasks.main import time_wrapper


@time_wrapper
def bulk_create(cursor, connection, names, data):
    cursor.executemany("INSERT into transcript values (?, ?)", zip(names, data))
    connection.commit()


@time_wrapper
def select_all(cursor):
    cursor.execute("select * from transcript")
    return cursor.fetchall()


@time_wrapper
def select_one(cursor):
    cursor.execute("select * from transcript where name = 123567")
    return cursor.fetchone()


def main():
    MAX_COPIES = 1000000
    data = {
        'name': "Paul",
        'Age': '25',
        'address': {
            'location': "USA"
        }
    }
    names = [f'employee_{n}' for n in range(MAX_COPIES)]
    data = [dumps(data)] * MAX_COPIES

    conn = connect(":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE transcript (name text, data text);")

    # SET 1m data in memory SQlite
    bulk_create(cursor=cur, connection=conn, names=names, data=data)  # 2.451 sec
    select_all(cursor=cur)  # 1.464 sec
    select_one(cursor=cur)  # 0.174 sec


if __name__ == '__main__':
    main()
