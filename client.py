from socket import socket, AF_INET, SOCK_STREAM
from json import loads, dumps

def create_socket(server_address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(server_address)

    print(f"Conectado ao servidor em {server_address}")

    return sock

def get_user_input():
    num1 = float(input("Digite o primeiro número: "))
    num2 = float(input("Digite o segundo número: "))
    operation = input("Digite a operação (+, -, *, /): ").strip()

    return {
        "num1": num1,
        "num2": num2,
        "operation": operation
    }

def receive_response(sock):
    response_data = sock.recv(1024).decode('utf-8')
    if not response_data:
        return None

    try:
        return loads(response_data)
    except Exception as e:
        print(f"Erro ao processar a resposta do servidor: {e}")
        return None

def process_response(response):
    if not response:
        print("Conexão encerrada pelo servidor.")
        return False

    if response.get('success'):
        print(f"Resultado: {response['result']}")
    else:
        print(f"Erro: {response['error']}")

    return True

def should_continue():
    continuar = input("Enviar outra operação? (s/n): ").lower()
    return continuar == 's'

def run_client():
    server_address = ('localhost', 5000)

    try:
        server_socket = create_socket(server_address)

        while True:
            try:
                data = get_user_input()

                json_data = dumps(data)
                server_socket.sendall(json_data.encode('utf-8'))

                response = receive_response(server_socket)
                process_response(response)
            except ValueError:
                print("Por favor, insira números válidos.")
                continue
            except KeyboardInterrupt:
                print("\nCliente encerrado pelo usuário.")
                break

            if not should_continue():
                break

    except ConnectionRefusedError:
        print("Não foi possível conectar ao servidor. Verifique se ele está em execução.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

    print("Conexão encerrada.")

if __name__ == "__main__":
    run_client()
