from flask import Flask, request
from socket import socket, AF_INET, SOCK_DGRAM
import json

app = Flask(__name__)

def fibonacci(n):
    if n == 1:
        return 0
    elif n == 2:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)

@app.route('/fibonacci', methods=['GET'])
def get_fibonacci_number():
    print("got request")
    try:
        num = int(request.args.get('number', -1))
        if num < 0:
            return 'ERROR 400', 400
        return f'sequence {num} fibonacci {fibonacci(num)}, 200 OK'
    except ValueError:
        return 'ERROR 400', 400

@app.route('/register', methods=['PUT'])
def register():
    infor = request.get_json()
    hostname = infor.get('hostname')
    ip = infor.get('ip')
    as_ip = infor.get('as_ip')
    as_port = infor.get('as_port')
    
    server_name = as_ip
    server_port = 53533
    
    fs_socket = socket(AF_INET, SOCK_DGRAM)
    dns_request = {
        'TYPE': 'A',
        'NAME': hostname,
        'VALUE': ip,
        'TTL': 10
    }
    
    message = json.dumps(dns_request)
    fs_socket.sendto(message.encode(), (server_name, server_port))
    response, _ = fs_socket.recvfrom(2048)
    fs_socket.close()
    
    return response.decode()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090, debug=True)

