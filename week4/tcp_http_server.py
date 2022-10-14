import os
import socket

HOST = ''
PORT = 8080

extension_map = {
    'html' : 'text/html;charset=utf8',
    'css' : 'text/css',
    'js' : 'text/javascript',
    'jpg' : 'image/jpeg',
    'jpeg' : 'image/jpeg',
    'png' : 'image/png'
}

status_code_map = {
    '200' : 'OK',
    '400' : 'NOT FOUND',
}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print('Start server')
    while True:
        try:
            conn, addr = s.accept()
            with conn:
                print(f'Connected by {addr}')
                data = conn.recv(1500)
                ptr = data.find('\r\n'.encode('utf-8'))
                header = data[:ptr]
                left = data[ptr:]
                request = header.decode('utf-8')
                method, path, protocol = request.split(' ')
                extension = path.split('.')[1] # 파일 확장자
                status_code = '200' # 상태코드
                print(f'Received: {method} {path} {protocol} {extension}')
                if not data:
                    break
                if path == '/':
                    path = '/index.html'
                path = f'.{path}'
                if not os.path.exists(path):
                    path = './notfound.html'
                    extension = 'html'
                    status_code = '404'
                with open(path, 'rb') as f:
                    body = f.read()
                    # if(extension is not ('jpeg' or 'jpg' or 'png')):
                    #     body = body.encode('utf-8')
                mimetype = extension_map.get(extension)
                status_code_message = status_code_map.get(status_code)
                header = f'HTTP/1.1 {status_code} {status_code_message}\r\n'
                header = f'{header}Server: Our server\r\n'
                header = f'{header}Connection: close\r\n'
                header = f'{header}Content-Type: {mimetype}\r\n'
                header = f'{header}Content-Length: {len(body)}\r\n'
                header = f'{header}\r\n'
                print(header)
                header = header.encode('utf-8')
                response = header + body
                conn.sendall(response)

        except KeyboardInterrupt:
            print('Shutdown server')
            break
