# author: Zahi Akad Yud bet 3 Hertzog Kfar Saba

# import outer modules:
import sqlite3

# constants:

AMOUNT_OF_RECORDS = 5
MAX_STAGE = 9 * 4
DB_FILE_LOCATION = r'sqlite_files\UsersRecords.db'


# classes:

class User(object):
    def __init__(self, user_name, salt, password_hash, stage):
        self.user_name = user_name
        self.salt = salt
        self.password_hash = password_hash
        self.stage = stage

    def __str__(self):
        return "user: " + self.user_name + ", " + self.password_hash + ", " + str(self.stage)


class Record(object):
    def __init__(self, rank, time, stage, user_name, date):
        self.rank = rank
        self.time = time
        self.stage = stage
        self.user_name = user_name
        self.date = date


class UserRecordORM:
    def __init__(self, file_location):
        self.conn = None  # will store the DB connection
        self.cursor = None  # will store the DB connection cursor
        self.file_location = file_location

    def open_db(self):
        """
        will open DB file and put value in:
        self.conn (need DB file name)
        and self.cursor
        """
        self.conn = sqlite3.connect(self.file_location)
        self.cursor = self.conn.cursor()

    def close_db(self):
        self.conn.close()

    def commit(self):
        self.conn.commit()

    # All read SQL:
    def get_user_salt(self, username):
        self.open_db()
        sql = "SELECT Salt FROM Users WHERE UserName = '" + username + "';"
        res = self.cursor.execute(sql)
        salt = self.get_str(res)
        salt = salt.replace("(", "")
        salt = salt.replace(")", "")
        salt = salt.replace(",", "")
        salt = salt.replace("\'", "")
        return salt

    def try_get_user(self, username, salted_password_hash):
        self.open_db()
        #salt = self.get_user_salt(username)
        #salted_password = password + salt
        #import hashlib
        #pass_hash = hashlib.sha256(salted_password.encode()).hexdigest()
        sql = "SELECT * FROM Users WHERE UserName = '" + username + "' AND SaltedPasswordHash = '" + salted_password_hash + "';"
        user_str = self.cursor.execute(sql)
        user_str = self.get_str(user_str)
        if user_str == "":
            return None
        #print("users_str", user_str)
        user_str = user_str.replace("(", "")
        user_str = user_str.replace(")", "")
        user_list = user_str.split(',')
        print(user_list)
        for i in range(len(user_list)):
            if i != 0:
                user_list[i] = user_list[i][1:]
            if i != len(user_list) - 1:
                user_list[i] = user_list[i][1:]
                user_list[i] = user_list[i][:-1]
        print(user_list)
        return User(user_list[0], user_list[1], user_list[2], int(user_list[3]))

    def check_username_exists(self, username):
        usernames_str = self.get_all_user_names()
        usernames_str = usernames_str.replace("\'", "")
        users_list = usernames_str.split('\n')
        for i in range(len(users_list)):
            users_list[i] = users_list[i][:-2]
            users_list[i] = users_list[i][1:]
            if username == users_list[i]:
                return True
        return False

    def get_all_user_names(self):
        self.open_db()
        res = self.cursor.execute("SELECT UserName FROM Users;")
        return self.get_str(res)

    def get_records_of_time(self, t):
        self.open_db()
        res = self.cursor.execute("SELECT * FROM Records WHERE TimeInMinutes = " + str(t) + " ORDER BY Rank;")
        return self.get_str(res)

    '''def get_all_users(self):
        self.open_db()
        res = self.cursor.execute("SELECT * FROM Users;")
        return self.get_str(res)'''

    '''def get_all_records(self):
        self.open_db()
        res = self.cursor.execute("SELECT * FROM Records ORDER BY Rank;")
        return self.get_str(res)'''

    '''def get_records_list(self):
        records_str = self.get_all_records()
        records_str = records_str.replace("(", "")
        records_str = records_str.replace(")", "")
        records_list = records_str.split('\n')
        return records_list'''

    # __________________________________________________________________________________________________________________
    # __________________________________________________________________________________________________________________
    # ______end of read start write ____________________________________________________________________________________
    # __________________________________________________________________________________________________________________
    # __________________________________________________________________________________________________________________
    # __________________________________________________________________________________________________________________

    # All write SQL:

    def try_insert_user(self, user):
        #print("trying to insert user")
        #print("salt", user.salt)
        #print("hash", user.password_hash)
        if self.check_username_exists(user.user_name):
            return False
        if user.stage < 1:
            user.stage = 1
        sql = "INSERT INTO Users (UserName, Salt, SaltedPasswordHash, Stage)"
        sql += " VALUES('" + user.user_name + "','"  + user.salt + "', '" + user.password_hash + "'," + str(user.stage) + ")"
        self.open_db()
        try:
            res = self.cursor.execute(sql)
            self.commit()
        except Exception as e:
            print(e)
        self.close_db()
        return True

    def insert_record(self, record):
        sql = "INSERT INTO Records (Rank, TimeInMinutes, Stage, UserName, Date)"
        sql += " VALUES(" + str(record.rank) + "," + str(record.time) + "," + str(record.stage) + ",'" \
               + record.user_name + "','" + record.date + "')"
        self.open_db()
        res = self.cursor.execute(sql)
        self.commit()
        self.close_db()
        return "res", res

    def get_str(self, res):
        ret_str = ""
        for row in res:
            ret_str += str(row) + "\n"
        if ret_str != "":
            ret_str = ret_str[:-1]
        self.close_db()
        return ret_str

    def get_str_num(self, res):
        ret_str = ""
        for row in res:
            ret_str += str(row)[1:-2] + "\n"
        if ret_str != "":
            ret_str = ret_str[:-1]
        self.close_db()
        return ret_str

    def increase_stage(self, user):
        if user.stage <= MAX_STAGE + 1:
            self.open_db()
            sql = "UPDATE Users SET Stage = Stage+1" + " WHERE UserName = '" + user.user_name + "';"
            res = self.cursor.execute(sql)
            self.commit()
            self.close_db()

    '''def remove_user(self, user_name):
        self.open_db()
        sql = "DELETE FROM Users WHERE UserName = '" + user_name + "';"
        res = self.cursor.execute(sql)
        self.commit()
        self.close_db()'''

    def update_records(self, record):
        self.open_db()
        sql = "UPDATE Records SET Rank = Rank + 1 WHERE TimeInMinutes = " + str(record.time) + " AND Stage < " + \
              str(record.stage) + ";"
        # sql = "UPDATE Records SET Stage = " + str(record.stage) + ", UserName = '" + record.user_name + \
        #      "'," + "Date ='" + record.date + "' WHERE TimeInMinutes = " + str(record.time) + ";"
        res = self.cursor.execute(sql)
        self.commit()
        self.close_db()
        self.insert_record(record)
        self.remove_records()
    def remove_records(self):
        self.open_db()
        sql = "DELETE FROM Records WHERE Rank > 5"
        res = self.cursor.execute(sql)
        self.commit()
        self.close_db()
    def check_record_broken(self, record):
        s = self.get_records_of_time(record.time)
        if s == "":
            #print("first record")
            record.rank = 1
            self.insert_record(record)
            return True
        else:
            records_str_list = s.split('\n')
            records_list = []
            # print('records_str_list', records_str_list)
            for i in range(len(records_str_list)):
                records_str_list[i] = records_str_list[i][1:len(records_str_list[i]) - 1]
                # print("records_str_list[i]", records_str_list[i])
                r_lst = records_str_list[i].split(', ')
                # print("r_lst", r_lst)
                records_list.append([int(r_lst[0]), int(r_lst[2])])
            #print("records_list", records_list)
            #print("record.stage", record.stage)
            better_than = 0
            for i in range(len(records_list)):
                if record.stage > records_list[i][1]:
                    better_than += 1
            #print("better than", better_than)
            if better_than == 0:
                if len(records_list) < AMOUNT_OF_RECORDS:
                    record.rank = len(records_list) + 1
                    #print("record.rank", record.rank)
                    self.update_records(record)
                    #print("in the top")
                    return True
                #print("not in the top")
                return False
            else:
                record.rank = len(records_list) - better_than + 1
                #print("record.rank", record.rank)
                if record.rank <= AMOUNT_OF_RECORDS:
                    self.update_records(record)
                    #print("in the top")
                    return True
                #print("not in the top")
                return False

    '''def remove_users(self, usernames_list):
        for username in usernames_list:
            self.remove_user(username)'''
#d= UserRecordORM(DB_FILE_LOCATION)
#n=d.get_all_user_names()
