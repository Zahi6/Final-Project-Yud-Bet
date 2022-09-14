import tcp_by_size
import socket
from secrets import token_bytes
import random
from Crypto.Cipher import AES
# ezer: https://www.youtube.com/watch?v=GYCVmMCRmTM
import time
import tcp_by_size
import datetime
import hashlib

LARGE_PRIME = 36484957213536676883
MESSAGE_TYPE_LENGTH = 7


def send_encrypted_data(sock, key, msg):
    nonce, cipher_text, tag = encrypt(key, msg)
    nonce = add_data_len(nonce)
    cipher_text = add_data_len(cipher_text)
    tag = add_data_len(tag)
    to_send = b'' + nonce + cipher_text + tag
    print("to_send", to_send)
    print(len(to_send))
    tcp_by_size.send_with_size(sock, to_send)


def receive_encrypted_data(sock, key):
    data = tcp_by_size.recv_by_size(sock)
    nonce, cipher_text, tag = get_nonce_cipher_text_tag(data)
    print("nonce", nonce)
    print("cipher_text", cipher_text)
    print("tag", tag)
    original_text = decrypt(key, nonce, cipher_text, tag).decode()
    print("original text:", original_text)
    return original_text


def add_data_len(data_bytes):
    data_len = str(len(data_bytes)).zfill(4)
    return data_len.encode() + data_bytes


def get_nonce_cipher_text_tag(data):
    SIZE_LEN = 4
    curr_len = 0
    nonce_cipher_text_tag = []
    for i in range(3):
        field_len = int(data[curr_len:curr_len + SIZE_LEN].decode())
        print(field_len)
        field = data[curr_len + SIZE_LEN:curr_len + SIZE_LEN + field_len]
        curr_len += SIZE_LEN + field_len
        print("field", field)
        nonce_cipher_text_tag.append(field)
    return nonce_cipher_text_tag


def encrypt(key, msg):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    cipher_text, tag = cipher.encrypt_and_digest(msg.encode('ascii'))
    return nonce, cipher_text, tag


def decrypt(key, nonce, cipher_text, tag):
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    decrypted_msg = cipher.decrypt(cipher_text)
    try:
        cipher.verify(tag)
        print("The message is authentic:", decrypted_msg)
    except ValueError:
        print("Key incorrect or message corrupted")
    return decrypted_msg


def get_key_from_shared_data(shared_data): # used in Diffie Helman function
    random.seed(shared_data)
    l = [b'a', b'b', b'c', b'd', b'e', b'f', b'g', b'h', b'i', b'j', b'k', b'l', b'm', b'n', b'o', b'p']
    print("len", len(l))
    random.shuffle(l)
    key = b''
    for b in l:
        key += b
    print("list:", l)
    print("key:", key)
    return key


def DiffieHelman_send_pg(sock):
    start_time = datetime.datetime.now()

    b = random.randint(50000, 125000)
    p = LARGE_PRIME
    g = p // 6

    # send p and g
    sock.send(("PUBLICP" + str(p) + ',' + str(g)).encode())
    print("p", p)
    print("g", g)
    print("len p ", len(str(p)))
    print("len g ", len(str(g)))
    # new_sock.send(str(p).encode())
    # new_sock.send(str(g).encode())

    # receive gamodp
    data = sock.recv(2056).decode()
    msg_type = data[:MESSAGE_TYPE_LENGTH]
    if msg_type != "RESULTA":
        print("protocol error")
    msg_body = data[MESSAGE_TYPE_LENGTH:]
    A = int(msg_body)
    print("A", A)

    # send gbmodp
    B = (g ** b) % p
    print("B", B)
    to_send = ("RESULTB" + str(B)).encode()
    print("to send", to_send)
    sock.send(to_send)

    shared_data = (A ** b) % p
    print("shared data:")
    print(shared_data)
    print("time Diffie Helman took:", datetime.datetime.now() - start_time)
    key = get_key_from_shared_data(shared_data)
    return key

def DiffieHelman_recieve_pg(sock):
    start_time = datetime.datetime.now()
    #a = 120301
    a = random.randint(50000, 125000)
    data = sock.recv(1024).decode()
    msg_type = data[:MESSAGE_TYPE_LENGTH]
    if msg_type != "PUBLICP":
        print("protocol error")
    msg_body = data[MESSAGE_TYPE_LENGTH:]
    p_g_str = msg_body
    print(p_g_str)
    # receive p and g:
    p_g_lst_str = p_g_str.split(',')
    p, g = int(p_g_lst_str[0]), int(p_g_lst_str[1])
    print("p", p)
    print("g", g)
    print("len p ", len(str(p)))
    print("len g ", len(str(g)))

    # send A(g**a%p):

    A = (g ** a) % p
    print("A", A)
    sock.send(("RESULTA" + str(A)).encode())

    # receive B(g**b%p):
    data = sock.recv(2056).decode()
    msg_type = data[:MESSAGE_TYPE_LENGTH]
    if msg_type != "RESULTB":
        print("protocol error")
    msg_body = data[MESSAGE_TYPE_LENGTH:]
    print("B", msg_body)
    B = int(msg_body)

    shared_data = (B ** a) % p
    print("shared data:")
    print(shared_data)
    print("time Diffie Helman took:", datetime.datetime.now() - start_time)
    key = get_key_from_shared_data(shared_data)
    return key


