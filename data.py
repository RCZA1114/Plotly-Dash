import mysql.connector
import pandas as pd
import threading
#from streamlit_autorefresh import st_autorefresh

def get_data():
    mydb = mysql.connector.connect(    #GEt The Data from the Database
        host="115.147.39.104",

        user="aptadmin",
        passwd="Pe*UyxpBZ_C0VL2c",
        database="airlock",
        port=5061,
    )
    #3query = "select *, DATE(last_update) as date, TIME(last_update) as time, HOUR(last_update) as hour, MINUTE(last_update) as minute, SECOND(last_update) as second, MONTH(last_update) AS month, DAY(last_update) as day, YEAR(last_update) as year from failures where last_update > '2023-01-01'"
    sql_query = pd.read_sql(
        "select *, DATE(last_update) as date, TIME(last_update) as time, HOUR(last_update) as hour, MINUTE(last_update) as minute, SECOND(last_update) as second, MONTH(last_update) AS month, DAY(last_update) as day, YEAR(last_update) as year from failures where last_update > '2023-01-10'",
        mydb
    )
    #sql_query = pd.read_sql("select * from failures", mydb)

    data = pd.DataFrame(sql_query, columns=['tower_id', 'pm2_5', 'humidity', 'temp', 'voc', 'pressure','last_update'])


    data['last_update'] = pd.to_datetime(data['last_update'])


    data.rename(
        columns={"tower_id": "Tower ID", "pm2_5": "PM2.5", "voc": "VOC", "humidity": "Humidity", "temp": "Temperature", "pressure": "Pressure", "last_update": "Date/Time"},
        inplace=True,
    )   #Update the Names


    data = data.replace({'Tower ID': {'T0703220001': 'Tower 1', 'T0703220002': 'Tower 2', 'T0703220005': 'Tower 5',
                                      'T0703220006': 'Tower 6', 'T0703220008': 'Tower 8', 'T0703220009': 'Tower 9'}})



    p = threading.Timer(300, get_data)

    p.start()    #Timer to Update the Data


    return data


