import socket
from functions import *
import pickle


def client(message):
    # Создание соединения
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))

    # Получение открытого ключа от сервера
    public_key_data = client_socket.recv(4096)
    public_key = pickle.loads(public_key_data)
    print(f"Получен открытый ключ: {public_key}")

    # Шифрование сообщения
    ciphertext = encrypt_line(message, public_key)
    print(f"Зашифрованное сообщение: {ciphertext}")

    # Отправка шифротекста серверу
    client_socket.send(pickle.dumps(ciphertext))

    client_socket.close()


if __name__ == "__main__":
    message = input("Введите сообщение для зашифрования ")
    client(message)
