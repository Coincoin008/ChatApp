import sqlite3
from sqlite3 import Error

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect("messagerie.db")
    except Error as e:
        print(e)
    return conn


def create_user(name, pw):
    try:
        conn = create_connection()
        cur = conn.cursor()
        query = f"INSERT INTO users (name, pw) VALUES ('{name}', '{pw}');"
        cur.execute(query)
        conn.commit()

        print("user ajouté")
    except Error as error:
        print("CREATE_USER > ", error)
    finally:
        if conn:
            conn.close()



def get_users(): 
    try:
        conn = create_connection()
        cur = conn.cursor()
        

        query = "SELECT * FROM users"
        cur.execute(query)
        records = cur.fetchall()
        return records

    except Error as error:
        print("GET_USERS > Failed ", error)
    finally:
        if conn:
            conn.close()

            """
            ->  [
                [name, password],
                [name, password],
                ...
            ]

            """


def add_friend_request(from_, to_):
    try:
        conn = create_connection()
        cur = conn.cursor()

        query = f"INSERT INTO demandes_de_contact (from_, to_) VALUES ('{from_}', '{to_}');"
        cur.execute(query)
        conn.commit()
    except Error as e:
        print("Add Friend request > Failed ", e)
    finally:
        if conn:
            conn.close()


def get_user_infos(user_name):
    users = get_users()
    for user in users:
        if user[1] == user_name:    # si le nom de l'utilisateur itéré == le nom de l'utilisateur actuel
            return user

def get_friend_request(username):
    try:
        conn = create_connection()
        cur = conn.cursor()

        query = "SELECT * FROM demandes_de_contact;"
        cur.execute(query)
        records = cur.fetchall()

        friend_requests = []

        for request in records:
            if request[2] == username:
                friend_requests.append(request[1])
        
        return friend_requests
    
    except Error as e:
        print("GET FRIEND REQUEST > Failed ", e)
    finally:
        if conn:
            conn.close()

def accept_friend_request(from_, to_):
    try:
        conn = create_connection()
        cur = conn.cursor()

        query = f"DELETE FROM demandes_de_contact WHERE from_='{from_}' AND to_='{to_}'"
        cur.execute(query)
        conn.commit()

        db_name = f"contacts_of_{to_}"
        db_name_from_ = f"contacts_of_{from_}"


        if not check_if_table_exists(db_name): create_table_of_contacts(to_)
        if not check_if_table_exists(db_name_from_): create_table_of_contacts(from_)

        add_contact_in_db(who=to_, new_friend=from_)
        add_contact_in_db(who=from_, new_friend=to_)


    except Error as e:
        print("ACCEPT FRIEND REQUEST > ", e)
    
    finally:
        if conn:
            conn.close()


def check_if_table_exists(tablename):
    try:
        conn = create_connection()
        cur = conn.cursor()

        exist = False

        query = f" SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{tablename}' "

        cur.execute(query)

        if cur.fetchone()[0]==1:
            exist = True

        conn.commit()
        conn.close()

        return exist
    
    except Error as e:
        print("TABLE EXISTS > ", e)

def add_contact_in_db(who, new_friend):
    try:
        conn = create_connection()
        cur = conn.cursor()

        query = f"INSERT INTO contacts_of_{who} (name) VALUES ('{new_friend}')"

        cur.execute(query)
        conn.commit()
    except Error as e:
        print("ADD_CONTACT_IN_DB > ", e)
    finally:
        if conn:
            conn.close()


def create_table_of_contacts(username):
    try:
        conn = create_connection()
        cur = conn.cursor()
        query = f"""CREATE TABLE contacts_of_{username} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT);
        """

        cur.execute(query)
        conn.commit()
    except Error as e:
        print(f"CREATE TABLE OF CONTACTS OF {username} > ", e)
    finally:
        if conn:
            conn.close()

def get_contacts(user):
    try:
        pass

    except Error as e:
        print("GET CONTACTS > ", e)
    
    finally:
        pass

if __name__ == "__main__":
    check_if_table_exists("users")


