from socket import socket, AF_INET, SOCK_DGRAM
import json

SERVER_PORT = 53533
RECEIVE_PORT = 2048
r_socket = socket(AF_INET, SOCK_DGRAM)
r_socket.bind(('', SERVER_PORT))

while True:
    message, _ = r_socket.recvfrom(2048)
    json_data = json.loads(message.decode())
    response = ''
    
    if len(data) == 4:
        with open('infor.txt', 'w') as outfile:
            json.dump(json_data, outfile)
        response = '201'
    elif len(data) == 2:
        with open('infor.txt', 'r', encoding='utf-8') as infile:
            stored_data = json.load(infile)
            if all(json_data.get(k) == stored_data.get(k) for k in ['TYPE', 'NAME']):
                response = json.dumps(stored_data)
    
    r_socket.sendto(response.encode(), _)

