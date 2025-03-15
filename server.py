from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread
from json import loads

def create_socket(server_address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    sock.bind(server_address)
    sock.listen(5)
    return sock

def handle_server(server_socket):
    client_socket, client_address = server_socket.accept()
    print(f'Conexão estabelecida com {client_address}')

    client_thread = Thread(
        target=handle_client,
        args=(client_socket, client_address)
    )
    client_thread.start()

def handle_operation(num1, num2, operation):
    if operation == '+':
        return num1 + num2
    elif operation == '-':
        return num1 - num2
    elif operation == '*':
        return num1 * num2
    elif operation == '/':
        if num2 != 0:
            return num1 / num2
        raise ValueError("Divisão por zero não é permitida.")
    raise ValueError("Operação inválida.")

def handle_client(client_socket, client_address):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            operation_dict = loads(data.decode('utf-8'))
            print(f'Payload recebido: {operation_dict}')

            try:
                result = handle_operation(operation_dict['num1'], operation_dict['num2'], operation_dict['operation'])
                response = { 'success': True, 'result': result }
            except ValueError as e:
                response = { 'success': False, 'error': str(e) }

            print(f'Payload enviado: {response}')
            client_socket.sendall(str(response).encode('utf-8'))
    finally:
        client_socket.close()
        print(f'Conexão com {client_address} encerrada')

def start_server():
    server_address = ('localhost', 5000)
    server_socket = create_socket(server_address)

    print(f"Servidor iniciado em http://{server_address[0]}:{server_address[1]}")

    try:
        while True:
            handle_server(server_socket)
    except KeyboardInterrupt:
        print("Servidor encerrado.")
    finally:
        server_socket.close()

if __name__ == '__main__':
    start_server()