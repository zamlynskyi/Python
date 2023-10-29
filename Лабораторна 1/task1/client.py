import socket

def main():
    host = '127.0.0.1'
    port = 8080

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
    except ConnectionRefusedError:
        print("Помилка: Неможливо підключитися до сервера. Переконайтеся, що сервер запущений.")
        return

    while True:
        message = input("Введіть текст для відправки на сервер (або 'exit' для завершення): ")
        client_socket.send(message.encode())

        if message.lower() == "exit":
            break

    client_socket.close()

if __name__ == "__main__":
    main()
