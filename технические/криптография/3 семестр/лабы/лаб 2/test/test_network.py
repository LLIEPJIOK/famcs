"""
Тесты для модуля network.py - сетевые функции
"""

import pytest
import socket
import pickle
import threading
import time
import sys
import os

# Добавляем путь к app в PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from crypto.network import send_msg, recv_msg, recvall


class TestRecvAll:
    """Тесты для функции recvall"""

    def test_recvall_full_data(self):
        """Получение полных данных"""
        # Создаем пару сокетов
        server_sock, client_sock = socket.socketpair()
        
        try:
            data = b"test data 12345"
            client_sock.sendall(data)
            client_sock.close()
            
            received = recvall(server_sock, len(data))
            assert received == data
        finally:
            server_sock.close()

    def test_recvall_partial_reads(self):
        """Получение данных частями"""
        server_sock, client_sock = socket.socketpair()
        
        try:
            data = b"x" * 1000
            
            # Отправляем в отдельном потоке с задержками
            def sender():
                for i in range(0, len(data), 100):
                    client_sock.send(data[i:i+100])
                    time.sleep(0.01)
                client_sock.close()
            
            thread = threading.Thread(target=sender)
            thread.start()
            
            received = recvall(server_sock, len(data))
            thread.join()
            
            assert received == data
        finally:
            server_sock.close()

    def test_recvall_eof_before_complete(self):
        """EOF до получения всех данных"""
        server_sock, client_sock = socket.socketpair()
        
        try:
            # Отправляем меньше данных и закрываем
            client_sock.send(b"short")
            client_sock.close()
            
            result = recvall(server_sock, 100)  # Ожидаем 100 байт
            assert result is None
        finally:
            server_sock.close()

    def test_recvall_empty_socket(self):
        """Пустой сокет (сразу закрыт)"""
        server_sock, client_sock = socket.socketpair()
        
        try:
            client_sock.close()
            result = recvall(server_sock, 10)
            assert result is None
        finally:
            server_sock.close()

    def test_recvall_zero_bytes(self):
        """Запрос нуля байт"""
        server_sock, client_sock = socket.socketpair()
        
        try:
            result = recvall(server_sock, 0)
            assert result == b''
        finally:
            server_sock.close()
            client_sock.close()


class TestSendRecvMsg:
    """Тесты для функций send_msg и recv_msg"""

    def test_send_recv_simple_dict(self):
        """Отправка и получение простого словаря"""
        server_sock, client_sock = socket.socketpair()
        
        try:
            msg = {"key": "value", "number": 42}
            
            send_msg(client_sock, msg)
            received = recv_msg(server_sock)
            
            assert received == msg
        finally:
            server_sock.close()
            client_sock.close()

    def test_send_recv_bytes(self):
        """Отправка и получение байтов"""
        server_sock, client_sock = socket.socketpair()
        
        try:
            msg = b"binary data \x00\x01\x02"
            
            send_msg(client_sock, msg)
            received = recv_msg(server_sock)
            
            assert received == msg
        finally:
            server_sock.close()
            client_sock.close()

    def test_send_recv_list(self):
        """Отправка и получение списка"""
        server_sock, client_sock = socket.socketpair()
        
        try:
            msg = [1, 2, 3, "four", b"five"]
            
            send_msg(client_sock, msg)
            received = recv_msg(server_sock)
            
            assert received == msg
        finally:
            server_sock.close()
            client_sock.close()

    def test_send_recv_none(self):
        """Отправка и получение None"""
        server_sock, client_sock = socket.socketpair()
        
        try:
            send_msg(client_sock, None)
            received = recv_msg(server_sock)
            
            assert received is None
        finally:
            server_sock.close()
            client_sock.close()

    def test_send_recv_nested_structure(self):
        """Отправка и получение вложенной структуры"""
        server_sock, client_sock = socket.socketpair()
        
        try:
            msg = {
                "level1": {
                    "level2": {
                        "level3": [1, 2, 3]
                    }
                },
                "data": b"binary"
            }
            
            send_msg(client_sock, msg)
            received = recv_msg(server_sock)
            
            assert received == msg
        finally:
            server_sock.close()
            client_sock.close()

    def test_send_recv_large_message(self):
        """Отправка и получение большого сообщения"""
        server_sock, client_sock = socket.socketpair()
        
        try:
            msg = b"x" * 100000
            
            send_msg(client_sock, msg)
            received = recv_msg(server_sock)
            
            assert received == msg
        finally:
            server_sock.close()
            client_sock.close()

    def test_send_recv_multiple_messages(self):
        """Отправка и получение нескольких сообщений"""
        server_sock, client_sock = socket.socketpair()
        
        try:
            messages = ["msg1", {"key": "value"}, b"bytes", 12345]
            
            for msg in messages:
                send_msg(client_sock, msg)
            
            received = []
            for _ in messages:
                received.append(recv_msg(server_sock))
            
            assert received == messages
        finally:
            server_sock.close()
            client_sock.close()

    def test_recv_msg_closed_socket(self):
        """Получение сообщения из закрытого сокета"""
        server_sock, client_sock = socket.socketpair()
        
        try:
            client_sock.close()
            result = recv_msg(server_sock)
            assert result is None
        finally:
            server_sock.close()

    def test_recv_msg_incomplete_length(self):
        """Получение с неполными данными длины"""
        server_sock, client_sock = socket.socketpair()
        
        try:
            # Отправляем только 2 байта из 4 для длины
            client_sock.send(b'\x00\x00')
            client_sock.close()
            
            result = recv_msg(server_sock)
            assert result is None
        finally:
            server_sock.close()

    def test_recv_msg_incomplete_data(self):
        """Получение с неполными данными сообщения"""
        server_sock, client_sock = socket.socketpair()
        
        try:
            # Указываем длину 100, но отправляем только 10 байт
            client_sock.send((100).to_bytes(4, 'big'))
            client_sock.send(b'x' * 10)
            client_sock.close()
            
            result = recv_msg(server_sock)
            assert result is None
        finally:
            server_sock.close()


class TestNetworkEdgeCases:
    """Краевые случаи для сетевых функций"""

    def test_send_recv_empty_dict(self):
        """Пустой словарь"""
        server_sock, client_sock = socket.socketpair()
        
        try:
            send_msg(client_sock, {})
            received = recv_msg(server_sock)
            assert received == {}
        finally:
            server_sock.close()
            client_sock.close()

    def test_send_recv_empty_list(self):
        """Пустой список"""
        server_sock, client_sock = socket.socketpair()
        
        try:
            send_msg(client_sock, [])
            received = recv_msg(server_sock)
            assert received == []
        finally:
            server_sock.close()
            client_sock.close()

    def test_send_recv_empty_bytes(self):
        """Пустые байты"""
        server_sock, client_sock = socket.socketpair()
        
        try:
            send_msg(client_sock, b'')
            received = recv_msg(server_sock)
            assert received == b''
        finally:
            server_sock.close()
            client_sock.close()

    def test_send_recv_empty_string(self):
        """Пустая строка"""
        server_sock, client_sock = socket.socketpair()
        
        try:
            send_msg(client_sock, '')
            received = recv_msg(server_sock)
            assert received == ''
        finally:
            server_sock.close()
            client_sock.close()

    def test_send_recv_unicode_string(self):
        """Unicode строка"""
        server_sock, client_sock = socket.socketpair()
        
        try:
            msg = "Привет мир! 🌍🔐"
            send_msg(client_sock, msg)
            received = recv_msg(server_sock)
            assert received == msg
        finally:
            server_sock.close()
            client_sock.close()

    def test_send_recv_tuple(self):
        """Кортеж (конвертируется pickle)"""
        server_sock, client_sock = socket.socketpair()
        
        try:
            msg = (1, 2, 3)
            send_msg(client_sock, msg)
            received = recv_msg(server_sock)
            assert received == msg
        finally:
            server_sock.close()
            client_sock.close()

    def test_send_recv_set(self):
        """Множество"""
        server_sock, client_sock = socket.socketpair()
        
        try:
            msg = {1, 2, 3}
            send_msg(client_sock, msg)
            received = recv_msg(server_sock)
            assert received == msg
        finally:
            server_sock.close()
            client_sock.close()

    def test_send_recv_float(self):
        """Число с плавающей точкой"""
        server_sock, client_sock = socket.socketpair()
        
        try:
            msg = 3.14159265359
            send_msg(client_sock, msg)
            received = recv_msg(server_sock)
            assert received == msg
        finally:
            server_sock.close()
            client_sock.close()

    def test_send_recv_boolean(self):
        """Булево значение"""
        server_sock, client_sock = socket.socketpair()
        
        try:
            for msg in [True, False]:
                send_msg(client_sock, msg)
                received = recv_msg(server_sock)
                assert received == msg
        finally:
            server_sock.close()
            client_sock.close()

    def test_bidirectional_communication(self):
        """Двунаправленная коммуникация"""
        server_sock, client_sock = socket.socketpair()
        
        try:
            # Клиент -> Сервер
            send_msg(client_sock, "hello from client")
            assert recv_msg(server_sock) == "hello from client"
            
            # Сервер -> Клиент
            send_msg(server_sock, "hello from server")
            assert recv_msg(client_sock) == "hello from server"
            
            # Еще раз в обе стороны
            send_msg(client_sock, "ping")
            send_msg(server_sock, "pong")
            
            assert recv_msg(server_sock) == "ping"
            assert recv_msg(client_sock) == "pong"
        finally:
            server_sock.close()
            client_sock.close()


class TestNetworkWithThreads:
    """Тесты с многопоточностью"""

    def test_concurrent_send_recv(self):
        """Параллельная отправка и получение"""
        server_sock, client_sock = socket.socketpair()
        received_messages = []
        
        try:
            def receiver():
                for _ in range(10):
                    msg = recv_msg(server_sock)
                    if msg is not None:
                        received_messages.append(msg)
            
            recv_thread = threading.Thread(target=receiver)
            recv_thread.start()
            
            for i in range(10):
                send_msg(client_sock, f"message_{i}")
                time.sleep(0.01)
            
            recv_thread.join(timeout=2)
            
            assert len(received_messages) == 10
            expected = [f"message_{i}" for i in range(10)]
            assert received_messages == expected
        finally:
            server_sock.close()
            client_sock.close()

    def test_interleaved_messages(self):
        """Чередующиеся сообщения"""
        server_sock, client_sock = socket.socketpair()
        
        try:
            for i in range(5):
                send_msg(client_sock, f"client_{i}")
                send_msg(server_sock, f"server_{i}")
            
            client_msgs = []
            server_msgs = []
            
            for _ in range(5):
                server_msgs.append(recv_msg(server_sock))
                client_msgs.append(recv_msg(client_sock))
            
            assert server_msgs == [f"client_{i}" for i in range(5)]
            assert client_msgs == [f"server_{i}" for i in range(5)]
        finally:
            server_sock.close()
            client_sock.close()
