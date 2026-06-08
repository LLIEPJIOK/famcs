import socket
import pickle
from typing import Any

def send_msg(sock: socket.socket, msg: Any):
    """Sends a pickled message prefixed with its length."""
    data = pickle.dumps(msg)
    sock.sendall(len(data).to_bytes(4, byteorder='big'))
    sock.sendall(data)

def recv_msg(sock: socket.socket) -> Any:
    """Receives a pickled message prefixed with its length."""
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = int.from_bytes(raw_msglen, byteorder='big')
    data = recvall(sock, msglen) 
    if not data:
        return None
    return pickle.loads(data)

def recvall(sock: socket.socket, n: int) -> bytes:
    """Helper function to recv n bytes or return None if EOF is hit."""
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return bytes(data)
