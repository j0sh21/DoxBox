import mariadb
import configparser
from datetime import datetime


def setup_db(cur, con):
    try:
        e = "SELECT * from TBL_Status"
        cur.execute(e)
        test_select = cur.fetchall()
        print("Starting DoxBox...")
    except mariadb.Error as db_err:
        print(f"Database error occurred: {db_err}")
        print("Initializing database...")
        try:
            # Create necessary tables and views
            statements = [
                "CREATE TABLE IF NOT EXISTS TBL_Status (command_id INT PRIMARY KEY, command_description VARCHAR(255))"
                "ENGINE=InnoDB DEFAULT CHARSET=utf8mb4",
                "INSERT INTO TBL_Status (command_id, command_description) VALUES (0, 'normal'),"
                "(1, 'begin_picture'), (2, 'begin_print'), (3, 'take_picture')",
                "CREATE TABLE IF NOT EXISTS TBL_Job (job_id INT AUTO_INCREMENT PRIMARY KEY, curr_Hash VARCHAR(255),"
                "time_created DATETIME, status INT, command_id INT, FOREIGN KEY (status)"
                "REFERENCES TBL_Status(command_id)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4",
                "CREATE TABLE IF NOT EXISTS TBL_Customer (lfd_nr INT PRIMARY KEY, curr_hash VARCHAR(255))"
                "ENGINE=InnoDB DEFAULT CHARSET=utf8mb4",
                "CREATE OR REPLACE VIEW V_Status AS SELECT command_id FROM TBL_Job WHERE job_id = (SELECT MAX(job_id)"
                "FROM TBL_Job WHERE status = 0)"
            ]
            for statement in statements:
                cur.execute(statement)
                con.commit()
                print(f"Statement\n{statement}\nsucessfully")
            print("Database setup completed.")
            print("Starting DoxBox...")
        except mariadb.Error as init_err:
            print(f"Error initializing the database: {init_err}")


def config():
    conf = configparser.ConfigParser()
    conf.read('cfg.ini')

    user = conf.get('DATABASE', 'user')
    password = conf.get('DATABASE', 'password')
    host = conf.get('DATABASE', 'host')
    database = conf.get('DATABASE', 'database')

    print('CFG loaded sucessfully')

    return user, password, host, database


def setup():
    user, password, host, database = config()
    cur, con = build_con(user, password, host, database)
    setup_db(cur, con)


def build_con(user, password, host, database):
    con = mariadb.connect(user=user, password=password, host=host, database=database)
    cur = con.cursor()
    return cur, con


def getInstruction():
    user, password, host, database = config()
    cur, con = build_con(user, password, host, database)
    e = f"Select * from V_Status"
    cur.execute(e)
    command_id = cur.fetchone()
    if command_id:
        command_id = command_id[0]
    return command_id


def finishJob():
    user, password, host, database = config()
    cur, con = build_con(user, password, host, database)
    e = "SELECT MAX(job_id) FROM TBL_Job where status = 0"
    cur.execute(e)
    job_id_tuple = cur.fetchone()

    if job_id_tuple:
        job_id = job_id_tuple[0]  # Extract the job_id value from the tuple

        # Update the job with the extracted job_id
        e = f"UPDATE TBL_Job SET status = 1 WHERE job_id = {job_id}"
        cur.execute(e)
        con.commit()
        print(f"Finished Job with ID: {job_id}")



def setInstructions(command_id, curr_Hash):
    user, password, host, database = config()
    cur, con = build_con(user, password, host, database)
    time_created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    e = f"INSERT INTO TBL_Job (curr_Hash, time_created, status, command_id) VALUES ('{curr_Hash}', '{time_created}', 0, {command_id})"
    cur.execute(e)
    con.commit()
    print(f"Set new Job with command {command_id}")


if __name__ == "__main__":
    setup()
    setInstructions(2, "fdhufifk")
    foo = getInstruction()
    print(foo)
    finishJob()
    foo = getInstruction()
    print(foo)
