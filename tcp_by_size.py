__author__ = 'Yossi'

# from  tcp_by_size import send_with_size ,recv_by_size


SIZE_HEADER_FORMAT = "000000000~"  # n digits for data size + one delimiter
size_header_size = len(SIZE_HEADER_FORMAT)
TCP_DEBUG = True

VER = 'Python3'


def str_byte(_s, direction):
    if VER == 'Python3':
        if direction == 'encode':
            return _s.encode()
        else:
            return _s.decode('utf8')
    else:
        return _s


def recv_by_size(sock):
    size_header = b''
    data_len = 0
    while len(size_header) < size_header_size:
        _s = sock.recv(size_header_size - len(size_header))
        if _s == b'':
            break
        else:
            size_header += _s
    data = b''
    if size_header != b'':
        data_len = int(size_header[:size_header_size - 1])
        while len(data) < data_len:
            _d = sock.recv(data_len - len(data))
            if _d == b'':
                break
            else:
                data += _d

    if TCP_DEBUG and size_header != b'':
        print("\nRecv(%s)>>>" % (size_header,), end='')
        if len(data) <= 200000000:
            """print ("%s"%(data,))"""
            print("")
        else:
            print("TOO BIG over 200000000")
    if data_len != len(data):
        data = b''  # Partial data is like no data !
    return data  # ( or data.decode() if want it as string)


def send_with_size(sock, bdata):
    len_data = len(bdata)
    header_data = str(len(bdata)).zfill(size_header_size - 1) + "~"

    bytea = bytearray(header_data, encoding='utf8') + bdata



    sock.send(bytea)
    #print("sent", bytea)
    if TCP_DEBUG and len_data > 0:
        print("\nSent(%s)>>>" % (len_data,), end='')
        if len_data <= 200000000:
            """print("%s"%(bytea.decode(),))"""
            print("")
        else:
            print("TOO BIG over 200000000")
