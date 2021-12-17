import psycopg2
from psycopg2.extras import RealDictCursor
import time

dbconnect = None

def get_session():

        global dbconnect
        while (not dbconnect):
                try:
                    dbconnect = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='Belguard0', cursor_factory=RealDictCursor)
                    print("Successfully connected to database fastapi")
                except Exception as error:
                    print (f"Connection failed: {error}")
                    time.sleep(2)
        
        return dbconnect