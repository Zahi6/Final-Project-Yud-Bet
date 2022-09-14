# author: Zahi Akad Yud bet 3 Hertzog Kfar Saba

# import:
# outer modules:
import random
import socket
import threading
import datetime
import time
import sys

#my files:
import tcp_by_size

# constants
#IP = "192.168.99.94"
PORT = 30017
#AREA_WIDTH = 10
MESSAGE_TYPE_LENGTH = 7
FILE_LOCATION = 'areas'

HOUSE_WIDTH = 50
HOUSE_HEIGHT = 50
AREA_WIDTH = 700//2
AREA_HEIGHT = 700//2
SPACES_IN_X = AREA_WIDTH//HOUSE_WIDTH
SPACES_IN_Y = AREA_HEIGHT//HOUSE_HEIGHT
SPACES = SPACES_IN_X * SPACES_IN_X
MAX_HOUSES = 4

# globals:
tid = 1
global_lock = threading.Lock()
my_id = -1
houses_needed = 0


def read_file(file_loc):
    print("reading from file", file_loc)
    with open(file_loc, 'r') as file:
        file_data = file.read()
    return file_data

# classes:-------------------------


class Thread(threading.Thread):
    def __init__(self):
        super(Thread, self).__init__()
        # another way to call to super __init__  (in case of multi inheritance)
        # threading.Thread.__init__(self)
        global tid
        self.tid = tid
        tid += 1
        self.lock = global_lock

    def run(self):
        print("thread " + str(tid) + " started at " + str(datetime.datetime.now()))

    def thread_started(self):
        print("Thread (tid=" + str(self.tid) + ") started at " + str(datetime.datetime.now()))


class MemoryThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        print("finished MemoryThread init")

    def run(self):
        self.thread_started()
        global my_id
        while my_id == -1:
            time.sleep(0.01)
        print("my_id", my_id)
        self.update_all_files()
        print("updated all files")

        global houses_needed
        prev_time = datetime.datetime.now()
        while True:
            curr_time = datetime.datetime.now()
            if houses_needed > 0:
                self.lock.acquire()
                self.update_file(houses_needed)
                print("updated file with " + str(houses_needed) + " houses")
                houses_needed = 0
                self.lock.release()
            if (curr_time - prev_time).seconds >= 1:
                prev_time = curr_time
                self.lock.acquire()
                self.update_all_files()
                self.lock.release()

    def update_all_files(self):
        for i in range(1, MAX_HOUSES+1):
            self.update_file(i)

    def update_file(self, num_of_houses):
        file_path = FILE_LOCATION + str(my_id) + '/area' + str(num_of_houses) + '.txt'
        #with open(file_path, 'w') as file:
        #    file.write('')
        spaces_list = []
        for i in range(SPACES):
            spaces_list.append(i)
        #print(SPACES)
        #print("spaces_list", spaces_list)
        to_write = ""
        for i in range(num_of_houses):
            index = random.randint(0, len(spaces_list)-1-i)
            space = spaces_list[index]
            spaces_list.pop(index)
            x = (space % 7) * 50
            y = (space // 7) * 50
            if i != num_of_houses - 1:
                to_write += str(x) + ", " + str(y) + '\n'
            else:
                to_write += str(x) + ", " + str(y)
        with open(file_path, 'w') as file:
            file.write(to_write)


class CommunicationThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.sock = socket.socket()
        ip = sys.argv[1]
        self.sock.connect((ip, PORT))
        # print("finished CommunicationThread init")

    def run(self):
        self.thread_started()
        self.send_with_size("HELPER_")

        msg_type, msg_body = self.receive_by_protocol()

        if msg_type != 'YOUR_ID':
            print("wrong protocol")
            return False
        global my_id, houses_needed
        my_id = int(msg_body)
        print("got id", my_id)
        while True:
            msg_type, msg_body = self.receive_by_protocol()
            self.lock.acquire()
            if msg_type != 'GETAREA':
                print("wrong protocol")
                self.lock.release()
                continue
            houses_needed = int(msg_body)
            area_str = read_file(FILE_LOCATION + str(my_id) + '/area' + str(houses_needed) + ".txt")
            print('area_str', area_str)
            self.send_with_size('RETAREA' + area_str)
            self.lock.release()

    def send_with_size(self, data):
        tcp_by_size.send_with_size(self.sock, data.encode())
        print("sent:", data)

    def receive_by_size(self):
        return tcp_by_size.recv_by_size(self.sock).decode()

    def receive_by_protocol(self):
        data = self.receive_by_size()
        msg_type = data[:MESSAGE_TYPE_LENGTH]
        msg_body = data[MESSAGE_TYPE_LENGTH:]
        print("received msg type:", msg_type)
        print("received msg body:", msg_body)
        return msg_type, msg_body


def main():

    memory_thread = MemoryThread()
    memory_thread.start()
    time.sleep(0.01)
    communication_thread = CommunicationThread()
    communication_thread.start()


if __name__ == '__main__':
    main()