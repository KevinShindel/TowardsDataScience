from sqlite3 import connect

from pandas import read_sql


def main():
    """
    This block explain how to use in-memory DataBase working
    Create table, run query, use pandas for exchange data in DB
    :return: None
    """

    # Connect to Database
    conn = connect(":memory:")
    names = ['John', 'Mike', 'Jane', 'Bella']
    grades = [90, 95, 92, 98]

    # Create a New Table and Insert Records
    cur = conn.cursor()
    cur.execute("CREATE TABLE transcript (name text, grade integer);")
    cur.executemany("INSERT into transcript values (?, ?)", zip(names, grades))
    conn.commit()

    # Query Records
    cur.execute("select * from transcript order by grade desc")
    all_ = cur.fetchall()
    one_ = cur.fetchone()

    # Delete Records
    _ = cur.execute("delete from transcript where name='John'")
    cur.execute("select * from transcript order by grade desc")
    all_ = cur.fetchall()

    #  Read SQLite Data With Pandas
    df = read_sql(sql="select * from transcript", con=conn)

    # Write DataFrame to SQLite
    df['name'] = 'Alex'
    df['grade'] = 12
    df.to_sql(name="transcript", con=conn, if_exists="append", index=False)  # Append to existing table!
    all_ = list(cur.execute("select * from transcript order by grade desc"))

    df['gpa'] = [4.0, 3.8, 3.9]
    df.to_sql(name="transcript", con=conn, if_exists="replace", index=False)  # Replace table if exist!
    all_ = list(cur.execute("select * from transcript order by grade desc"))

    conn.close()


if __name__ == '__main__':
    main()
