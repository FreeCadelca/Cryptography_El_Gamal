import socket
from functions import *
import pickle


def server():
    # Генерирование ключей
    keys = key_gen()
    public_key = keys['public']
    private_key = keys['private']

    # Создание сокета (ip + порт)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 55555))  # Привязываем к 127.0.0.1:55555
    server_socket.listen(1)
    print("Сервер ждет соединение на порту 55555...")

    conn, addr = server_socket.accept()
    print(f"Соединение установлено на {addr}")

    # Отправляем публичный ключ клиенту
    conn.send(pickle.dumps(public_key))

    # Получаем зашифрованное сообщение
    data = conn.recv(4096)
    ciphertext = pickle.loads(data)
    print(f"Полученный шифротекст: {ciphertext}")

    # Расшифровываем сообщение
    decrypted_message = decrypt(private_key, public_key, ciphertext)
    print(f"Расшифрованное сообщение: {decrypted_message}")

    conn.close()
    server_socket.close()


if __name__ == "__main__":
    server()
