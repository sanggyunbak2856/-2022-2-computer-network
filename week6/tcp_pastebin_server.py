import socket

FLAGS = _ = None
DEBUG = False


def main():
    if DEBUG:
        print(f'Parsed arguments {FLAGS}')
        print(f'Unparsed arguments {_}')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((FLAGS.host, FLAGS.port))
        s.listen(FLAGS.backlog)
        print(f'Start server')
        db = {}
        while True:
            try:
                conn, addr = s.accept()
                print(f'Connected: {addr=}')
                with conn:
                    data = conn.recv(1500)
                    if DEBUG:
                        print(f'{data=}')
                    ptr = data.find('\r\n'.encode('utf-8'))
                    header = data[:ptr]
                    body = data[ptr:]
                    if DEBUG:
                        print(f'{header=}')
                        print(f'{body=}')
                    request = header.decode('utf-8')
                    if DEBUG:
                        print(f'{request=}')
                    chunks = request.split(' ')
                    method = chunks[0]
                    key = chunks[1]
                    print(f'{method=}')
                    print(f'{key=}')
                    value = 'Invalid request'
                    if method == 'GET':
                        value = db.get(key, '')
                    elif method == 'SET':
                        value = body.decode('utf-8')
                        db[key] = value
                    conn.sendall(value.encode('utf-8'))
            except KeyboardInterrupt:
                print('Shutdown server')
                break

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='The present debug message')
    parser.add_argument('--host', default='0.0.0.0', type=str,
                        help='IP address')
    parser.add_argument('--port', default=8080, type=int,
                        help='Port number')
    parser.add_argument('--backlog', default=1, type=int,
                        help='Backlog')

    FLAGS, _ = parser.parse_known_args()
    DEBUG = FLAGS.debug

    main()
