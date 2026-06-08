import socket
import threading
from binascii import hexlify
import signal
import secrets

from crypto.bmqv import (BMQVMessage0, BMQVMessage1, BMQVMessage2, BMQVMessage3, BMQVParticipant)
from crypto.cert import RootCA
from crypto.elliptic import EllipticCurve
from crypto.fmt import serialize_point
from crypto.network import recv_msg, send_msg


def generate_long_term_identity(id_name: str, cv: EllipticCurve, root_ca: RootCA):
    d = 0
    while d == 0:
        d = secrets.randbelow(cv.q)

    Q = cv.mul(d, cv.G)
    if not cv.is_on_curve(Q):
        raise ValueError("generated public key is not on the curve")

    cert = root_ca.issue_cert(id_name, serialize_point(Q, cv.l, 4 * cv.l)).serialize()
    return {"d": d, "Q": Q, "cert": cert}


def _hx(b: bytes) -> str:
    return hexlify(b).decode("ascii")


def _print_kv(prefix: str, name: str, value: bytes):
    print(f"{prefix}  {name} = { _hx(value) }")


def handle_client(conn, addr, cv, root_ca: RootCA, bob_static):
    with conn:
        prefix = f"[{addr}]"
        print(f"[NEW CONNECTION] {addr} connected.")
        try:
            bob = BMQVParticipant(
                "Bob",
                cv,
                hello=b"Hello from Bob",
                cert=bob_static["cert"],
                root_ca=root_ca,
                d=bob_static["d"],
                Q=bob_static["Q"],
            )

            print(f"{prefix} Bob initialized")
            _print_kv(prefix, "Bob.cert", bob.cert)

            # 1. Receive M0 (Alice -> Bob)
            m0 = recv_msg(conn)
            if not isinstance(m0, BMQVMessage0):
                print(f"{prefix} Expected M0")
                return
            print(f"\n{prefix} Step M0: recv")
            _print_kv(prefix, "M0.hello_a", m0.hello_a)

            # 2. Process M0 and send M1 (Bob -> Alice)
            m1 = bob.process_m0(m0)
            print(f"\n{prefix} Step M1: send")
            _print_kv(prefix, "M1.hello_b", m1.hello_b)
            _print_kv(prefix, "M1.cert_b", m1.cert_b)
            _print_kv(prefix, "M1.v_b", m1.v_b)
            send_msg(conn, m1)
            print(f"{prefix} M1 sent")

            # 3. Receive M2 (Alice -> Bob)
            m2 = recv_msg(conn)
            if not isinstance(m2, BMQVMessage2):
                print(f"{prefix} Expected M2")
                return
            print(f"\n{prefix} Step M2: recv")
            _print_kv(prefix, "M2.cert_a", m2.cert_a)
            _print_kv(prefix, "M2.v_a", m2.v_a)
            if m2.t_a is not None:
                _print_kv(prefix, "M2.t_a", m2.t_a)

            # 4. Process M2 and send M3 (Bob -> Alice)
            m3 = bob.process_m2(m2)
            print(f"\n{prefix} Step M3: send")
            if m3.t_b is not None:
                _print_kv(prefix, "M3.t_b", m3.t_b)
            if bob.K0 is not None:
                _print_kv(prefix, "K0", bob.K0)
            send_msg(conn, m3)
            print(f"{prefix} M3 sent")
            
            print(f"\n{prefix} Key agreement completed")
            _print_kv(prefix, "K0", bob.get_shared_key())

            print(f"{prefix} Session completed")
        except Exception as e:
            print(f"{prefix} Error: {e}")
        finally:
            print(f"[DISCONNECTED] {addr} disconnected.")

def run_server(host='127.0.0.1', port=12345):
    cv = EllipticCurve.default_curve()

    root_sk_bytes = bytes.fromhex(
        "00112233445566778899aabbccddeeff"
        "00112233445566778899aabbccddeeff"
    )
    root_sk = int.from_bytes(root_sk_bytes, "little", signed=False) % cv.q
    if root_sk == 0:
        root_sk = 1

    root_ca = RootCA.from_privkey(id_name="Root", curve=cv, privkey=root_sk)

    # Long-term server identity (static keypair + certificate) generated independently
    bob_static = generate_long_term_identity("Bob", cv, root_ca)

    running = True

    def _on_sigint(signum, frame):
        nonlocal running
        running = False

    signal.signal(signal.SIGINT, _on_sigint)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        s.settimeout(0.5)
        print(f"[LISTENING] Bob (Server) listening on {host}:{port}... (Ctrl+C to stop)")

        while running:
            try:
                conn, addr = s.accept()
            except socket.timeout:
                continue
            except OSError:
                break

            # Запускаем новый поток для каждого клиента
            thread = threading.Thread(
                target=handle_client,
                args=(conn, addr, cv, root_ca, bob_static),
                daemon=True,
            )
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

        print("[SHUTDOWN] Server stopping")

if __name__ == "__main__":
    run_server()