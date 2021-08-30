from cassandra.cluster import Cluster
import csv
import pandas as pd

df = pd.DataFrame()
df.to_csv()
if __name__ == "__main__":
    cluster = Cluster(['127.0.0.1'], port=9042)
    session = cluster.connect()
    session.execute("create keyspace if not exists Data with replication = {'class' : 'SimpleStrategy', 'replication_factor':2};")
    session.execute('Use Data;')
    session.execute("DROP TABLE IF EXISTS Data.zomato;")
    session.execute("""CREATE TABLE if not exists zomato (url text,address text,name text,online_order text,
    book_table text,rate text,votes int,phone text,location text,rest_type text,dish_liked text,
    cuisines text,approx_cost text, reviews_list text, menu_item text, listed_in_type text,listed_in_city text,
     id_no Bigint, primary key(id_no));""")
    count = 0
    with open('data_given/zomato.csv', 'r') as file:
        csv.field_size_limit(10000000)
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            (url, address, name, online_order, book_table, rate, votes, phone,
                      location, rest_type, dish_liked,cuisines,approx_cost,reviews_list,
                      menu_item,listed_in_type,listed_in_city, id_no) = row
            print(id_no)
            session.execute("""INSERT INTO zomato ( url ,address, name, online_order, book_table, rate, votes, phone,
                        location, rest_type, dish_liked,cuisines,approx_cost,reviews_list,menu_item, listed_in_type ,
                        listed_in_city, id_no) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s,
                         %s, %s, %s);""", [url ,address, name, online_order, book_table, rate, int(votes), phone,
                        location, rest_type, dish_liked,cuisines,approx_cost,reviews_list,menu_item, listed_in_type ,
                        listed_in_city, int(id_no)])