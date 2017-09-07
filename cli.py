import sqlite3
import argparse
from datetime import datetime
from getpass import getpass

from jenkins import Jenkins

argparser = argparse.ArgumentParser()
argparser.add_argument("url", help="the url of the jenkins instance")
argparser.add_argument("-U", "--username", help="the username of a valid jenkins user")
args = argparser.parse_args()

def create_db():
    """
    Creates an sqlite connection, the required db, and returns the connection instance
    """
    conn = sqlite3.connect("jenkins.db")
    cursor = conn.cursor()
    try:
        cursor.execute('''CREATE TABLE jenkins_jobs 
            (name text, status text, url text, checktime text)''')
        conn.commit()
    except sqlite3.OperationalError:
        print("Table exits ... ")
    return conn

def save_jobs(jobs, conn):
    """
    Recieves a list of jenkins jobs as a list and saves them in a sqlite3 db.
    """
    for job in jobs:
        print job
        conn.execute('''INSERT INTO jenkins_jobs VALUES (?,?,?,?)''', 
            [job["name"], job["color"], job["url"], datetime.now()])

    conn.commit()

conn = create_db()
if __name__ == "__main__":
    #connect to jenkins instance
    password = getpass("Enter use password ")
    remote_jenkins = Jenkins(args.url, username=args.username, 
        password=password)

    #retrive jobs from server
    jobs = remote_jenkins.get_all_jobs()
    save_jobs(jobs, conn)
    conn.close()