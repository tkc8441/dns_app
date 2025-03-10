from flask import Flask, request
from socket import socket, AF_INET, SOCK_DGRAM
from urllib.request import urlopen
import json

app = Flask(__name__)

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    """Handles the Fibonacci request by resolving the hostname via a DNS query and forwarding the request."""
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')
    
    if not all([hostname, fs_port, number, as_ip, as_port]):
        return '400', 400
    
    ip_request = {'TYPE': 'A', 'NAME': hostname}
    server_name = as_ip
    server_port = 53533
    
    us_socket = socket(AF_INET, SOCK_DGRAM)
    message = json.dumps(ip_request)
    us_socket.sendto(message.encode(), (server_name, server_port))
    response, _ = us_socket.recvfrom(2048)
    
    infor = json.loads(response.decode())
    ip_address = infor.get('VALUE')
    us_socket.close()
    
    url = f'http://{ip_address}:{fs_port}/fibonacci?number={number}'
    with urlopen(url) as link:
        return link.read()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

