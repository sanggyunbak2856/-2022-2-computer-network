import socket

FLAGS = _ = None
DEBUG = False


def main():
    if DEBUG:
        print(f'Parsed arguments {FLAGS}')
        print(f'Unparsed arguments {_}')

    method = input('Input method: ').strip().upper()

    key = input('Input key: ').strip()

    message = f'{method} {key}\r\n'
    if method == 'SET':
        value = input('Input value: ').strip()
        message = f'{message}{value}'

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((FLAGS.host, FLAGS.port))
        s.sendall(message.encode('utf-8'))
        data = s.recv(1500)
        data = data.decode('utf-8')

    print(f'Received:')
    print(f'{data}')

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='The present debug message')
    parser.add_argument('--host', default='127.0.0.1', type=str,
                        help='IP address')
    parser.add_argument('--port', default=8080, type=int,
                        help='Port number')


    FLAGS, _ = parser.parse_known_args()
    DEBUG = FLAGS.debug

    main()

