from dotenv import load_dotenv
import psycopg2
import os
from os.path import join, dirname


def Extract():
    try:
        # Load env and connect to DB
        dotenv_path=(join(dirname(__file__), '../.env'))
        print(dotenv_path)
        load_dotenv(dotenv_path)
        print(os.getenv("USER"))
        print(os.getenv("PASSWORD"))
        print(os.getenv("HOST"))
        print(os.getenv("PORT"))
        print(os.getenv("DATABASE"))

        connection = psycopg2.connect(user = os.getenv("USER"),
                                      password = os.getenv("PASSWORD"),
                                      host =os.getenv("HOST"),
                                      port = os.getenv("PORT"),
                                      database = os.getenv("DATABASE"))
        print("gg")
        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        print ( connection.get_dsn_parameters(),"\n")
        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record,"\n")
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
        #closing database connection.
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")

Extract()