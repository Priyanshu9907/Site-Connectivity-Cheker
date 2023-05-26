import mysql.connector
import requests
import schedule
import time
from datetime import datetime

mysql_config = {
    'user': 'root',
    'password': '2105393',
    'host': 'localhost',
    'database': 'siteconnchecker'
}

conn = mysql.connector.connect(**mysql_config)
cursor = conn.cursor()

create_results_table = """
create table if not exists results (
    id int auto_increment primary key,
    siteid int not NULL,
    statuscode int not NULL,
    responsetime float Not NULL,
    date datetime not NULL,
    foreign key (siteid) References sites(id)
)
"""
cursor.execute(create_results_table)

create_latestdata_table = """
create table if not exists latestdata (
    id int auto_increment primary key,
    siteid int not NULL,
    statuscode int not NULL,
    responsetime float Not NULL,
    date datetime not NULL,
    foreign key (siteid) References sites(id)
)
"""
cursor.execute(create_latestdata_table)

def connectivity_check():
    select= "Select id, name, url from sites"
    cursor.execute(select)
    sites = cursor.fetchall()

    for site in sites:
        siteid, name, url = site
        starttime = time.time()

        try:
            response = requests.get(url)
            status_code = response.status_code
        except requests.exceptions.RequestException:
            status_code = -1

        endtime = time.time()
        responsetime = endtime - starttime
        date = datetime.now()

        insert_query = "insert into results (siteid, statuscode, responsetime, date) values (%s, %s, %s, %s)"
        values = (siteid, status_code, responsetime,date)
        cursor.execute(insert_query, values)
        conn.commit()
        print(f"Site: {name}, Status Code: {status_code}, Response Time: {responsetime}")

    truncate = "truncate table latestdata"
    cursor.execute(truncate)
    conn.commit()

    select= """
    Select r.siteid, r.statuscode, r.responsetime, r.date
    from results r where r.date = (select max(date) from results where siteid = r.siteid)
    """
    
    cursor.execute(select)
    latestdata = cursor.fetchall()

    for data in latestdata:
        siteid, status_code, responsetime, date = data
        insert = "insert into latestdata (siteid, statuscode, responsetime, date) values (%s, %s, %s, %s)"
        values = (siteid, status_code, responsetime, date)
        cursor.execute(insert, values)
        conn.commit()

print("program started!!!")
schedule.every(1).minutes.do(connectivity_check)

while True:
    schedule.run_pending()
    time.sleep(1)
cursor.close()