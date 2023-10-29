import socket
import datetime
import threading

def handle_client(client_socket):
    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Отримано ({current_time}): {data}")

        # Перевірка на певну команду (наприклад, "exit")
        if data.lower() == "exit":
            break

def main():
    host = '127.0.0.1'
    port = 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Сервер слухає на {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"З'єднано з {addr}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()
