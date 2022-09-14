# author: Zahi Akad Yud bet 3 Hertzog Kfar Saba

# import:
# outer modules:
import random
import threading
import datetime
import time
import socket

import hashlib
import uuid

# my files:
import tcp_by_size
import dh_aes
import sql_orm

from Crypto.Cipher import AES
# written by me:


# constants
IP = "0.0.0.0"
PORT = 30017
MESSAGE_TYPE_LENGTH = 7
DB_FILE_LOCATION = r'sqlite_files\UsersRecords.db'

# globals:
tid = 0  # thread id
db = sql_orm.UserRecordORM(DB_FILE_LOCATION)
helper_server_thread_count = 0
global_lock = threading.Lock()
houses_for_helper = [0, 0, 0, 0]
helpers_available = [False, False, False, False]
areas = [[], [], [], []]


# classes:-------------------------


class Thread(threading.Thread):
    def __init__(self):
        super(Thread, self).__init__()
        # another way to call to super __init__  (in case of multi inheritance)
        # threading.Thread.__init__(self)
        global tid, global_lock
        self.tid = tid
        tid += 1
        self.lock = global_lock

    def run(self):
        print("thread " + str(tid) + " started at " + str(datetime.datetime.now()))

    def thread_started(self):
        print("Thread (tid=" + str(self.tid) + ") started at " + str(datetime.datetime.now()))


class CommunicationThread(Thread):
    def __init__(self, socket_address):
        Thread.__init__(self)
        (self.sock, self.address) = socket_address
        print("self.address", self.address)
        print("self.address type", type(self.address))
        self.key = None
        global db
        self.db = db
        self.user = None

    def run(self):
        global helper_server_thread_count
        self.thread_started()
        msg_type, msg_body = self.receive_by_protocol()
        print("data_str---", msg_type + msg_body)
        if msg_type == "HELPER_":
            helper_id = self.get_helper_id()
            if helper_id != -1:
                self.tid = helper_id
                print("helper" + str(self.tid) + " connected")
                self.run_thread_helper_server()
        else:
            self.run_thread_client()

    def get_helper_id(self):
        global helpers_available
        self.lock.acquire()
        for i, b in enumerate(helpers_available):
            if not b:
                helpers_available[i] = True
                self.lock.release()
                return i
        self.lock.release()
        return -1

    def run_thread_helper_server(self):
        global houses_for_helper
        self.send_with_size('YOUR_ID' + str(self.tid))
        while True:
            time.sleep(0.01)
            if houses_for_helper[self.tid] > 0:
                got_it = self.get_area_from_helper()
                if not got_it:
                    print("didn't get the area")
                    return False

    def get_area_from_helper(self):
        global houses_for_helper, areas
        self.send_with_size('GETAREA' + str(houses_for_helper[self.tid]))
        try:
            msg_type, msg_body = self.receive_by_protocol()
        except Exception as e:
            print(e)
            return False
        if msg_type == 'RETAREA' and msg_body != 'none' and msg_body:
            print("protocol - correct")
            points_str = msg_body.split('\n')
            print("points_str", points_str)
            points = []
            for p in points_str:
                points.append(p.split(', '))
            for i in range(len(points)):
                points[i][0] = int(points[i][0])
                points[i][1] = int(points[i][1])
            print("tid", self.tid, "points list:", points)
            areas[self.tid] = points
            houses_for_helper[self.tid] = 0
            return True
        areas[self.tid] = []
        return False

    def run_thread_client(self):
        global houses_for_helper, areas
        #self.lock = client_thread_lock
        try:
            self.key = dh_aes.DiffieHelman_send_pg(self.sock)
        except Exception as e:
            print(e)
            return False
        user = None
        while user is None:
            try:
                user = self.account_comm()
            except Exception as e:
                print(e)
                return False
            if type(user) == bool:
                return False
        print("User got in:")
        print("username:", user.user_name)
        print("passhash:", user.password_hash)
        print("stage:", user.stage)
        while True:
            try:
                data = self.receive_by_size()
            except Exception as e:
                print(e)
                return False

            msg_type = data[:MESSAGE_TYPE_LENGTH]
            print("msg_type", msg_type)
            msg_body = data[MESSAGE_TYPE_LENGTH:]
            print("msg body", msg_body)

            if msg_type == 'GETSTAG':
                self.send_campaign_stage(int(msg_body))
            elif msg_type == 'BEATSTA':
                print("user" + user.user_name + "beat stage" + str(user.stage))
                self.lock.acquire()
                db.increase_stage(user)
                self.lock.release()
            elif msg_type == 'GETCOMP':
                self.send_comp_stage(int(msg_body))
            elif msg_type == 'STATIME':
                sta_time = msg_body.split('\n')
                sta, t = int(sta_time[0]), float(sta_time[1])
                self.check_record(sta, t)
            elif msg_type == 'RECORDS':
                self.send_all_records_of_time(int(msg_body))
            elif msg_type == "DISCONN":
                print("dc")
                return False
            # fields = msg_body.split('\n')
            # print("fields", fields)

    def send_all_records_of_time(self, records_time):
        self.lock.acquire()
        records_str = db.get_records_of_time(records_time)
        self.lock.release()
        self.send_with_size('RECORDS' + records_str)
        print("sent", 'RECORDS' + records_str)

    def check_record(self, stage, t):
        # r = sql_orm.Record(datetime.datetime.date(datetime))
        d = datetime.datetime.today().strftime('%Y-%m-%d-%H:%M')
        r = sql_orm.Record(rank=None, time=t, stage=stage, user_name=self.user.user_name, date=d)
        print(r.rank, r.stage, r.time, r.user_name, r.date)
        self.lock.acquire()
        broken = db.check_record_broken(r)
        self.lock.release()
        if broken:
            self.send_with_size('NEWRECO')
        else:
            self.send_with_size('NOTRECO')

    def send_campaign_stage(self, stage_wanted):
        world = (stage_wanted - 1) // 9 + 1
        stage_in_world = stage_wanted % 9
        print("stage_wanted", stage_wanted)
        print("world", world)
        print("stage_in_world", stage_in_world)
        if stage_in_world == 0:
            stage_in_world = 9
        stage_file = 'campaign/world' + str(world) + '/stage' + str(stage_in_world) + '.txt'
        try:
            with open(stage_file) as file:
                file_data = file.read()
        except Exception as e:
            print(e)
            file_data = "none"
        print("file_data", file_data)
        if file_data == "":
            self.send_with_size("RETSTAGnone")
        else:
            self.send_with_size("RETSTAG" + file_data)


    def send_comp_stage(self, difficulty):
        global areas, houses_for_helper
        self.lock.acquire()

        if check_dc():
            print("helper server disconnected")
            self.send_with_size('RETCOMPnone')
            self.lock.release()
            return False
        total_houses_amount = difficulty + 3
        houses_for_helper = [0, 0, 0, 0]
        least_houses = total_houses_amount // 4
        for i in range(len(houses_for_helper)):
            houses_for_helper[i] = least_houses
        for i in range(total_houses_amount % 4):
            r = random.randint(0, 3)
            houses_for_helper[r] += 1
        print("houses_for_helper", houses_for_helper)
        global helpers_available
        print('helpers_available', helpers_available)

        wait_for_all = True
        while wait_for_all:
            time.sleep(0.01)
            wait_for_all = False
            for i in range(len(houses_for_helper)):
                if houses_for_helper[i] != 0:
                    wait_for_all = True
                    if not helpers_available[i]:
                        print("helper server disconnected")
                        self.send_with_size('RETCOMPnone')
                        houses_for_helper = [0, 0, 0, 0]
                        self.lock.release()
                        return False
        print("finished waiting for all")

        print("areas", areas)
        real_areas = []
        real_areas_pointer = 0
        for i, a in enumerate(areas):
            if a != []:
                real_areas.append([])
                print('real areas', real_areas)
                print('real_areas_pointer', real_areas_pointer)
                print('a', a, 'len of a', len(a))
                for j in range(len(a)):
                    real_areas[real_areas_pointer].append(a[j])
                add_x = 0
                add_y = 0
                if i == 1:
                    add_x = 350
                elif i == 2:
                    add_y = 350
                elif i == 3:
                    add_x = 350
                    add_y = 350
                for j in range(len(real_areas[real_areas_pointer])):
                    real_areas[real_areas_pointer][j][0] += add_x
                    real_areas[real_areas_pointer][j][1] += add_y
                real_areas_pointer += 1
        print("real_areas", real_areas)
        points_str = ""
        for r_area in real_areas:
            for point in r_area:
                points_str += str(point[0]) + ", " + str(point[1]) + '\n'
        points_str = points_str[:-1]
        self.send_with_size('RETCOMP' + points_str)
        print('RETCOMP' + points_str)
        # houses_for_helper = [0 ,0, 0, 0]
        areas = [[], [], [], []]
        self.lock.release()
        return True

    def account_comm(self):
        data = self.receive_encrypted_msg()
        msg_type = data[:MESSAGE_TYPE_LENGTH]
        print("msg_type", msg_type)
        msg_body = data[MESSAGE_TYPE_LENGTH:]
        print("msg body", msg_body)
        fields = msg_body.split('\n')
        print("fields", fields)
        if msg_type == "DISCONN":
            return False
        if msg_type == "NEWUSER":
            username, password = fields[0], fields[1]
            salt = uuid.uuid4().hex
            salted_password = password + salt
            print("saletd_pass", salted_password)
            salted_password_hash = hashlib.sha256(salted_password.encode()).hexdigest()
            print("salted_pass hash", salted_password_hash)
            #password_hash = hashlib.sha256(password.encode()).hexdigest()
            print("username!!!", username)
            print("password_hash!!!", salted_password_hash)
            print("salt!!!", salt)
            print(msg_type)
            new_user = sql_orm.User(username, salt, salted_password_hash, 1)
            self.lock.acquire()
            inserted = db.try_insert_user(new_user)
            self.lock.release()
            print("inserted", inserted)
            if inserted:
                self.user = new_user
                self.send_with_size("NEWUSER")
                return new_user
            else:
                self.send_with_size("ERRNEW_") #Username already exists
                return None
        elif msg_type == "EXSUSER":
            print("in exs user")
            username, password = fields[0], fields[1]
            print("about to get salt")
            self.lock.acquire()
            salt = db.get_user_salt(username)
            self.lock.release()
            print("salt", salt)
            salted_password = password + salt
            print("salted pass", salted_password)
            salted_password_hash = hashlib.sha256(salted_password.encode()).hexdigest()
            print("username!!!", username)
            print("salted_password_hash!!!", salted_password_hash)
            print(msg_type)
            self.lock.acquire()
            login_user = db.try_get_user(username, salted_password_hash)
            self.lock.release()
            print("is it none:", login_user is None)
            if login_user != None:
                self.user = login_user
                self.send_with_size("EXSUSER" + str(login_user.stage))
                return login_user
            else:
                print("incorrect username or password lets send that")
                self.send_with_size("ERREXS_")
                return None
        return None

    def send_with_size(self, data):
        tcp_by_size.send_with_size(self.sock, data.encode())

    def receive_by_size(self):
        return tcp_by_size.recv_by_size(self.sock).decode()

    def receive_by_protocol(self):
        data = self.receive_by_size()
        msg_type = data[:MESSAGE_TYPE_LENGTH]
        msg_body = data[MESSAGE_TYPE_LENGTH:]
        return msg_type, msg_body

    def send_encrypted_msg(self, msg):
        dh_aes.send_encrypted_data(self.sock, self.key, msg)

    def receive_encrypted_msg(self):
        return dh_aes.receive_encrypted_data(self.sock, self.key)


# 'static' functions:
def check_dc():
    dc = False
    for i in range(len(helpers_available)):
        if not helpers_available[i]:
            dc = True
            # break
    return dc


def main():

    server_socket = socket.socket()
    server_socket.bind((IP, PORT))

    server_socket.listen()
    threads = []

    while True:
        (new_sock, address) = server_socket.accept()
        t = CommunicationThread((new_sock, address))
        t.start()
        threads.append(t)


if __name__ == '__main__':
    main()
