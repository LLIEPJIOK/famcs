import socket
from binascii import hexlify

from crypto.bmqv import BMQVMessage1, BMQVMessage3, BMQVParticipant
from crypto.cert import RootCA
from crypto.elliptic import EllipticCurve
from crypto.network import recv_msg, send_msg


def _hx(b: bytes) -> str:
    return hexlify(b).decode("ascii")


def _print_kv(name: str, value: bytes):
    print(f"  {name} = { _hx(value) }")

def run_client(host='127.0.0.1', port=12345):
    cv = EllipticCurve.default_curve()

    root_sk_bytes = bytes.fromhex(
        "00112233445566778899aabbccddeeff"
        "00112233445566778899aabbccddeeff"
    )
    root_sk = int.from_bytes(root_sk_bytes, "little", signed=False) % cv.q
    if root_sk == 0:
        root_sk = 1

    root_ca = RootCA.from_privkey(id_name="Root", curve=cv, privkey=root_sk)

    alice = BMQVParticipant(
        "Alice",
        cv,
        hello=b"Hello from Alice",
        cert=None,
        root_ca=root_ca,
    )

    print("[CLIENT] Alice initialized")
    _print_kv("Alice.cert", alice.cert)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            print(f"[CLIENT] Connected to {host}:{port}")

            # 1. Send M0 (Alice -> Bob)
            m0 = alice.process_init()
            print("\n[CLIENT] Step M0: send")
            _print_kv("M0.hello_a", m0.hello_a)
            send_msg(s, m0)
            print("[CLIENT] M0 sent")

            # 2. Receive M1 (Bob -> Alice)
            m1 = recv_msg(s)
            if not isinstance(m1, BMQVMessage1):
                print("Expected M1")
                return
            print("\n[CLIENT] Step M1: recv")
            _print_kv("M1.hello_b", m1.hello_b)
            _print_kv("M1.cert_b", m1.cert_b)
            _print_kv("M1.v_b", m1.v_b)

            # 3. Process M1 and send M2 (Alice -> Bob)
            m2 = alice.process_m1(m1)
            print("\n[CLIENT] Step M2: send")
            _print_kv("M2.cert_a", m2.cert_a)
            _print_kv("M2.v_a", m2.v_a)
            if m2.t_a is not None:
                _print_kv("M2.t_a", m2.t_a)
            if alice.K0 is not None:
                _print_kv("K0", alice.K0)
            send_msg(s, m2)
            print("[CLIENT] M2 sent")

            # 4. Receive M3 (Bob -> Alice)
            m3 = recv_msg(s)
            if not isinstance(m3, BMQVMessage3):
                print("Expected M3")
                return
            print("\n[CLIENT] Step M3: recv")
            if m3.t_b is not None:
                _print_kv("M3.t_b", m3.t_b)

            alice.process_m3(m3)
            print("\n[CLIENT] Key agreement completed")
            _print_kv("K0", alice.get_shared_key())
    except KeyboardInterrupt:
        print("\n[CLIENT] Interrupted (Ctrl+C)")

if __name__ == "__main__":
    run_client()
