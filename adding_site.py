import mysql.connector

mysql_table = {
    'user': 'root',
    'password': '2105393',
    'host': 'localhost',
    'database': 'siteconnchecker'
}

conn = mysql.connector.connect(**mysql_table)
cursor = conn.cursor()
create_sites_table = """
create table if not exists sites (
    id int auto_increment Primary key,
    name varchar(300) not null,
    url varchar(300) not null
)
"""

cursor.execute(create_sites_table)
def add_site(name, url):
    insert_query = "insert into  sites (name, url) values (%s, %s)"
    values = (name, url)
    cursor.execute(insert_query, values)
    conn.commit()
    print("Site added")

add_site("Effitrac","https://www.effitrac.com/")
add_site("Google","https://www.google.com/")
add_site("Youtube","https://www.youtube.com")
add_site("Fake site","https://www.fakesitedemosite.com")


cursor.close()
conn.close()