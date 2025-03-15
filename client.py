import socket
import json
import ast

def main():
    host = 'localhost'
    port = 5000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        print("Conectado ao servidor.")

        while True:
            try:
                num1 = float(input("Digite o primeiro número: "))
                num2 = float(input("Digite o segundo número: "))
                operation = input("Digite a operação (+, -, *, /): ").strip()

                data = {
                    "num1": num1,
                    "num2": num2,
                    "operation": operation
                }

                json_data = json.dumps(data)
                sock.sendall(json_data.encode('utf-8'))

                response_data = sock.recv(1024).decode('utf-8')
                if not response_data:
                    print("Conexão encerrada pelo servidor.")
                    break

                try:
                    response = ast.literal_eval(response_data)
                    if response.get('success'):
                        print(f"Resultado: {response['result']}")
                    else:
                        print(f"Erro: {response['error']}")
                except Exception as e:
                    print(f"Erro ao processar a resposta do servidor: {e}")

            except ValueError:
                print("Por favor, insira números válidos.")
                continue
            except KeyboardInterrupt:
                print("\nCliente encerrado pelo usuário.")
                break

            continuar = input("Enviar outra operação? (s/n): ").lower()
            if continuar != 's':
                break

    print("Conexão encerrada.")

if __name__ == "__main__":
    main()