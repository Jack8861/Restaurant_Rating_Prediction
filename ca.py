from cassandra.cluster import Cluster
import csv

if __name__ == "__main__":
    cluster = Cluster(['127.0.0.1'], port=9042)
    session = cluster.connect()
    session.execute("create keyspace if not exists Data with replication = {'class' : 'SimpleStrategy', 'replication_factor':2}")
    session.execute('Use Data')
    session.execute("DROP TABLE IF EXISTS Data.zomato;")
    session.execute("""CREATE TABLE if not exists zomato (url text,address text,name text,online_order text,
    book_table text,rate text,votes int,phone text,location text,rest_type text,dish_liked text,
    cuisines text,approx_cost text, reviews_list text, menu_item text, listed_in_type text,listed_in_city text,
     id_no Bigint, primary key(id_no));""")
    session