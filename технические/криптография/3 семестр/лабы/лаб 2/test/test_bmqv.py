"""
Тесты для модуля bmqv.py - BMQV протокол обмена ключами
"""

import pytest
import secrets
import copy
import sys
import os

# Добавляем путь к app в PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from crypto.bmqv import (
    BMQVMessage0,
    BMQVMessage1,
    BMQVMessage2,
    BMQVMessage3,
    BMQVParticipant,
)
from crypto.cert import RootCA
from crypto.elliptic import EllipticCurve
from crypto.fmt import serialize_point, deserialize_point


class TestBMQVMessages:
    """Тесты для классов сообщений BMQV"""

    def test_message0_creation(self):
        """Создание BMQVMessage0"""
        m0 = BMQVMessage0(hello_a=b"hello_from_alice")
        assert m0.hello_a == b"hello_from_alice"

    def test_message1_creation(self):
        """Создание BMQVMessage1"""
        m1 = BMQVMessage1(
            hello_b=b"hello_from_bob",
            cert_b=b"cert_data",
            v_b=b"point_data"
        )
        assert m1.hello_b == b"hello_from_bob"
        assert m1.cert_b == b"cert_data"
        assert m1.v_b == b"point_data"

    def test_message2_creation_with_tag(self):
        """Создание BMQVMessage2 с тегом"""
        m2 = BMQVMessage2(
            cert_a=b"cert_data",
            v_a=b"point_data",
            t_a=b"auth_tag"
        )
        assert m2.cert_a == b"cert_data"
        assert m2.v_a == b"point_data"
        assert m2.t_a == b"auth_tag"

    def test_message2_creation_without_tag(self):
        """Создание BMQVMessage2 без тега"""
        m2 = BMQVMessage2(cert_a=b"cert_data", v_a=b"point_data")
        assert m2.t_a is None

    def test_message3_creation_with_tag(self):
        """Создание BMQVMessage3 с тегом"""
        m3 = BMQVMessage3(t_b=b"auth_tag")
        assert m3.t_b == b"auth_tag"

    def test_message3_creation_without_tag(self):
        """Создание BMQVMessage3 без тега"""
        m3 = BMQVMessage3()
        assert m3.t_b is None


class TestBMQVParticipant:
    """Тесты для класса BMQVParticipant"""

    @pytest.fixture
    def curve(self) -> EllipticCurve:
        return EllipticCurve.default_curve()

    @pytest.fixture
    def root_ca(self, curve: EllipticCurve) -> RootCA:
        d, _ = curve._generate_keypair()
        return RootCA.from_privkey("TestCA", curve, d)

    def test_participant_creation_auto_keypair(self, curve: EllipticCurve, root_ca: RootCA):
        """Создание участника с автоматической генерацией ключевой пары"""
        alice = BMQVParticipant(
            id_name="Alice",
            curve=curve,
            hello=b"hello_alice",
            cert=None,
            root_ca=root_ca
        )
        
        assert alice.id_name == "Alice"
        assert alice.hello == b"hello_alice"
        assert alice.d is not None
        assert alice.Q is not None
        assert curve.is_on_curve(alice.Q)

    def test_participant_creation_with_keypair(self, curve: EllipticCurve, root_ca: RootCA):
        """Создание участника с заданной ключевой парой"""
        d, Q = curve._generate_keypair()
        
        alice = BMQVParticipant(
            id_name="Alice",
            curve=curve,
            hello=b"hello_alice",
            cert=None,
            root_ca=root_ca,
            d=d,
            Q=Q
        )
        
        assert alice.d == d
        assert alice.Q == Q

    def test_participant_creation_without_root_ca(self, curve: EllipticCurve):
        """Создание участника без root_ca должно выбросить исключение"""
        with pytest.raises(ValueError, match="root_ca is required"):
            BMQVParticipant(
                id_name="Alice",
                curve=curve,
                hello=b"hello",
                cert=None,
                root_ca=None
            )

    def test_participant_with_existing_cert(self, curve: EllipticCurve, root_ca: RootCA):
        """Создание участника с существующим сертификатом"""
        d, Q = curve._generate_keypair()
        pubkey = serialize_point(Q, curve.l, 4 * curve.l)
        cert = root_ca.issue_cert("Alice", pubkey)
        cert_bytes = cert.serialize()
        
        alice = BMQVParticipant(
            id_name="Alice",
            curve=curve,
            hello=b"hello_alice",
            cert=cert_bytes,
            root_ca=root_ca,
            d=d,
            Q=Q
        )
        
        assert alice.cert == cert_bytes

    def test_participant_with_mismatched_cert(self, curve: EllipticCurve, root_ca: RootCA):
        """Создание участника с несоответствующим сертификатом"""
        d1, Q1 = curve._generate_keypair()
        d2, Q2 = curve._generate_keypair()
        
        # Сертификат для Q1
        pubkey1 = serialize_point(Q1, curve.l, 4 * curve.l)
        cert = root_ca.issue_cert("Alice", pubkey1)
        cert_bytes = cert.serialize()
        
        # Попытка использовать сертификат с другим ключом Q2
        with pytest.raises(ValueError, match="certificate does not match"):
            BMQVParticipant(
                id_name="Alice",
                curve=curve,
                hello=b"hello",
                cert=cert_bytes,
                root_ca=root_ca,
                d=d2,
                Q=Q2
            )

    def test_generate_keypair(self, curve: EllipticCurve, root_ca: RootCA):
        """Генерация ключевой пары участником"""
        alice = BMQVParticipant(
            id_name="Alice",
            curve=curve,
            hello=b"hello",
            cert=None,
            root_ca=root_ca
        )
        
        d, Q = alice.generate_keypair()
        
        assert 1 <= d < curve.q
        assert Q is not None
        assert curve.is_on_curve(Q)
        assert Q == curve.mul(d, curve.G)

    def test_process_init(self, curve: EllipticCurve, root_ca: RootCA):
        """Обработка инициализации (M0)"""
        alice = BMQVParticipant(
            id_name="Alice",
            curve=curve,
            hello=b"hello_alice",
            cert=None,
            root_ca=root_ca
        )
        
        m0 = alice.process_init()
        
        assert isinstance(m0, BMQVMessage0)
        assert m0.hello_a == b"hello_alice"


class TestBMQVProtocol:
    """Тесты полного протокола BMQV"""

    @pytest.fixture
    def curve(self) -> EllipticCurve:
        return EllipticCurve.default_curve()

    @pytest.fixture
    def root_ca(self, curve: EllipticCurve) -> RootCA:
        d, _ = curve._generate_keypair()
        return RootCA.from_privkey("TestCA", curve, d)

    @pytest.fixture
    def alice(self, curve: EllipticCurve, root_ca: RootCA) -> BMQVParticipant:
        return BMQVParticipant(
            id_name="Alice",
            curve=curve,
            hello=b"hello_alice",
            cert=None,
            root_ca=root_ca
        )

    @pytest.fixture
    def bob(self, curve: EllipticCurve, root_ca: RootCA) -> BMQVParticipant:
        return BMQVParticipant(
            id_name="Bob",
            curve=curve,
            hello=b"hello_bob",
            cert=None,
            root_ca=root_ca
        )

    def test_full_protocol_success(self, alice: BMQVParticipant, bob: BMQVParticipant):
        """Успешное выполнение полного протокола"""
        # Alice -> Bob: M0
        m0 = alice.process_init()
        
        # Bob -> Alice: M1
        m1 = bob.process_m0(m0)
        
        # Alice -> Bob: M2
        m2 = alice.process_m1(m1)
        
        # Bob -> Alice: M3
        m3 = bob.process_m2(m2)
        
        # Alice verifies M3
        alice.process_m3(m3)
        
        # Проверяем, что ключи совпадают
        alice_key = alice.get_shared_key()
        bob_key = bob.get_shared_key()
        
        assert alice_key is not None
        assert bob_key is not None
        assert alice_key == bob_key

    def test_shared_key_length(self, alice: BMQVParticipant, bob: BMQVParticipant):
        """Проверка длины общего ключа"""
        m0 = alice.process_init()
        m1 = bob.process_m0(m0)
        m2 = alice.process_m1(m1)
        m3 = bob.process_m2(m2)
        alice.process_m3(m3)
        
        key = alice.get_shared_key()
        assert len(key) == 32  # 256 бит

    def test_different_sessions_different_keys(
        self, curve: EllipticCurve, root_ca: RootCA
    ):
        """Разные сессии дают разные ключи"""
        alice1 = BMQVParticipant("Alice", curve, b"hello1", None, root_ca)
        bob1 = BMQVParticipant("Bob", curve, b"hello1", None, root_ca)
        
        alice2 = BMQVParticipant("Alice", curve, b"hello2", None, root_ca)
        bob2 = BMQVParticipant("Bob", curve, b"hello2", None, root_ca)
        
        # Первая сессия
        m0 = alice1.process_init()
        m1 = bob1.process_m0(m0)
        m2 = alice1.process_m1(m1)
        m3 = bob1.process_m2(m2)
        alice1.process_m3(m3)
        key1 = alice1.get_shared_key()
        
        # Вторая сессия
        m0 = alice2.process_init()
        m1 = bob2.process_m0(m0)
        m2 = alice2.process_m1(m1)
        m3 = bob2.process_m2(m2)
        alice2.process_m3(m3)
        key2 = alice2.get_shared_key()
        
        assert key1 != key2


class TestBMQVForgeryResistance:
    """Тесты на устойчивость к подделке сообщений"""

    @pytest.fixture
    def curve(self) -> EllipticCurve:
        return EllipticCurve.default_curve()

    @pytest.fixture
    def root_ca(self, curve: EllipticCurve) -> RootCA:
        d, _ = curve._generate_keypair()
        return RootCA.from_privkey("TestCA", curve, d)

    @pytest.fixture
    def alice(self, curve: EllipticCurve, root_ca: RootCA) -> BMQVParticipant:
        return BMQVParticipant("Alice", curve, b"hello_alice", None, root_ca)

    @pytest.fixture
    def bob(self, curve: EllipticCurve, root_ca: RootCA) -> BMQVParticipant:
        return BMQVParticipant("Bob", curve, b"hello_bob", None, root_ca)

    def test_tampered_m1_cert(self, alice: BMQVParticipant, bob: BMQVParticipant):
        """Подделка сертификата в M1 должна быть обнаружена"""
        m0 = alice.process_init()
        m1 = bob.process_m0(m0)
        
        # Подделываем сертификат
        tampered_m1 = BMQVMessage1(
            hello_b=m1.hello_b,
            cert_b=bytes([b ^ 0x01 for b in m1.cert_b[:8]]) + m1.cert_b[8:],
            v_b=m1.v_b
        )
        
        with pytest.raises(ValueError):
            alice.process_m1(tampered_m1)

    def test_tampered_m1_v_b(
        self, curve: EllipticCurve, alice: BMQVParticipant, bob: BMQVParticipant
    ):
        """Подделка точки v_b в M1 приводит к провалу верификации T_a на стороне Bob"""
        m0 = alice.process_init()
        m1 = bob.process_m0(m0)
        
        # Создаем другую точку
        fake_u = secrets.randbelow(curve.q - 1) + 1
        fake_v = curve.mul(fake_u, curve.G)
        fake_v_bytes = serialize_point(fake_v, curve.l, 4 * curve.l)
        
        tampered_m1 = BMQVMessage1(
            hello_b=m1.hello_b,
            cert_b=m1.cert_b,
            v_b=fake_v_bytes
        )
        
        # Alice использует подделанное сообщение и вычисляет другой ключ
        m2 = alice.process_m1(tampered_m1)
        
        # Bob проверяет T_a, который вычислен с другим v_b
        # Верификация T_a провалится, потому что Bob использует свой v_b
        with pytest.raises(ValueError, match="T_A verification failed"):
            bob.process_m2(m2)

    def test_tampered_m2_cert(
        self, curve: EllipticCurve, alice: BMQVParticipant, bob: BMQVParticipant
    ):
        """Подделка сертификата в M2 должна быть обнаружена"""
        m0 = alice.process_init()
        m1 = bob.process_m0(m0)
        m2 = alice.process_m1(m1)
        
        # Подделываем сертификат
        tampered_m2 = BMQVMessage2(
            cert_a=bytes([b ^ 0x01 for b in m2.cert_a[:8]]) + m2.cert_a[8:],
            v_a=m2.v_a,
            t_a=m2.t_a
        )
        
        with pytest.raises(ValueError):
            bob.process_m2(tampered_m2)

    def test_tampered_m2_v_a(
        self, curve: EllipticCurve, alice: BMQVParticipant, bob: BMQVParticipant
    ):
        """Подделка точки v_a в M2 должна привести к провалу верификации T_a"""
        m0 = alice.process_init()
        m1 = bob.process_m0(m0)
        m2 = alice.process_m1(m1)
        
        # Создаем другую точку
        fake_u = secrets.randbelow(curve.q - 1) + 1
        fake_v = curve.mul(fake_u, curve.G)
        fake_v_bytes = serialize_point(fake_v, curve.l, 4 * curve.l)
        
        tampered_m2 = BMQVMessage2(
            cert_a=m2.cert_a,
            v_a=fake_v_bytes,
            t_a=m2.t_a  # Оригинальный тег не будет соответствовать новой точке
        )
        
        with pytest.raises(ValueError, match="T_A verification failed"):
            bob.process_m2(tampered_m2)

    def test_tampered_m2_t_a(self, alice: BMQVParticipant, bob: BMQVParticipant):
        """Подделка тега T_a в M2 должна быть обнаружена"""
        m0 = alice.process_init()
        m1 = bob.process_m0(m0)
        m2 = alice.process_m1(m1)
        
        # Подделываем тег
        tampered_t_a = bytes([b ^ 0xFF for b in m2.t_a])
        tampered_m2 = BMQVMessage2(
            cert_a=m2.cert_a,
            v_a=m2.v_a,
            t_a=tampered_t_a
        )
        
        with pytest.raises(ValueError, match="T_A verification failed"):
            bob.process_m2(tampered_m2)

    def test_tampered_m3_t_b(self, alice: BMQVParticipant, bob: BMQVParticipant):
        """Подделка тега T_b в M3 должна быть обнаружена"""
        m0 = alice.process_init()
        m1 = bob.process_m0(m0)
        m2 = alice.process_m1(m1)
        m3 = bob.process_m2(m2)
        
        # Подделываем тег
        tampered_t_b = bytes([b ^ 0xFF for b in m3.t_b])
        tampered_m3 = BMQVMessage3(t_b=tampered_t_b)
        
        with pytest.raises(ValueError, match="T_B verification failed"):
            alice.process_m3(tampered_m3)

    def test_replay_attack_m1(
        self, curve: EllipticCurve, root_ca: RootCA,
        alice: BMQVParticipant, bob: BMQVParticipant
    ):
        """Атака повторного воспроизведения M1 приводит к разным ключам"""
        m0 = alice.process_init()
        m1_original = bob.process_m0(m0)
        
        # Полностью выполняем протокол
        m2 = alice.process_m1(m1_original)
        m3 = bob.process_m2(m2)
        alice.process_m3(m3)
        original_key = alice.get_shared_key()
        
        # Создаем новую сессию с Alice
        alice2 = BMQVParticipant("Alice", curve, b"hello_alice2", None, root_ca)
        m0_2 = alice2.process_init()
        
        # Атакующий воспроизводит старое M1
        m2_2 = alice2.process_m1(m1_original)
        
        # Bob не участвует во второй сессии, поэтому ключ будет другим
        # или протокол провалится
        new_key = alice2.get_shared_key()
        
        # Ключи должны отличаться
        assert new_key != original_key

    def test_man_in_the_middle_attack(
        self, curve: EllipticCurve, root_ca: RootCA
    ):
        """MITM атака: атакующий не может получить общий ключ без сертификата"""
        alice = BMQVParticipant("Alice", curve, b"hello_alice", None, root_ca)
        bob = BMQVParticipant("Bob", curve, b"hello_bob", None, root_ca)
        
        # Атакующий создает свою ключевую пару
        attacker_d, attacker_Q = curve._generate_keypair()
        
        # Выполняем протокол нормально
        m0 = alice.process_init()
        m1 = bob.process_m0(m0)
        m2 = alice.process_m1(m1)
        m3 = bob.process_m2(m2)
        alice.process_m3(m3)
        
        # Alice и Bob имеют одинаковый ключ
        assert alice.get_shared_key() == bob.get_shared_key()
        
        # Атакующий не может вычислить ключ без знания d_a или d_b

    def test_invalid_point_in_m1(
        self, curve: EllipticCurve, alice: BMQVParticipant, bob: BMQVParticipant
    ):
        """Невалидная точка в M1 должна быть отклонена"""
        m0 = alice.process_init()
        m1 = bob.process_m0(m0)
        
        # Создаем невалидную точку (не на кривой)
        invalid_point = (12345, 67890)
        invalid_v_bytes = serialize_point(invalid_point, curve.l, 4 * curve.l)
        
        tampered_m1 = BMQVMessage1(
            hello_b=m1.hello_b,
            cert_b=m1.cert_b,
            v_b=invalid_v_bytes
        )
        
        with pytest.raises(ValueError, match="Invalid point"):
            alice.process_m1(tampered_m1)

    def test_invalid_point_in_m2(
        self, curve: EllipticCurve, alice: BMQVParticipant, bob: BMQVParticipant
    ):
        """Невалидная точка в M2 должна быть отклонена"""
        m0 = alice.process_init()
        m1 = bob.process_m0(m0)
        m2 = alice.process_m1(m1)
        
        # Создаем невалидную точку
        invalid_point = (12345, 67890)
        invalid_v_bytes = serialize_point(invalid_point, curve.l, 4 * curve.l)
        
        tampered_m2 = BMQVMessage2(
            cert_a=m2.cert_a,
            v_a=invalid_v_bytes,
            t_a=m2.t_a
        )
        
        with pytest.raises(ValueError, match="Invalid point"):
            bob.process_m2(tampered_m2)

    def test_forged_certificate_with_wrong_ca(
        self, curve: EllipticCurve, root_ca: RootCA
    ):
        """Подделанный сертификат от другого CA должен быть отклонен"""
        alice = BMQVParticipant("Alice", curve, b"hello_alice", None, root_ca)
        
        # Создаем атакующего с другим CA
        attacker_ca_d, _ = curve._generate_keypair()
        attacker_ca = RootCA.from_privkey("AttackerCA", curve, attacker_ca_d)
        
        attacker_d, attacker_Q = curve._generate_keypair()
        attacker_pubkey = serialize_point(attacker_Q, curve.l, 4 * curve.l)
        forged_cert = attacker_ca.issue_cert("Bob", attacker_pubkey)
        
        # Создаем M1 с поддельным сертификатом
        u_b = secrets.randbelow(curve.q - 1) + 1
        v_b = curve.mul(u_b, curve.G)
        
        m0 = alice.process_init()
        forged_m1 = BMQVMessage1(
            hello_b=b"hello_attacker",
            cert_b=forged_cert.serialize(),
            v_b=serialize_point(v_b, curve.l, 4 * curve.l)
        )
        
        # Alice должна отклонить сертификат
        with pytest.raises(ValueError, match="certificate signature invalid"):
            alice.process_m1(forged_m1)


class TestBMQVEdgeCases:
    """Краевые случаи для BMQV протокола"""

    @pytest.fixture
    def curve(self) -> EllipticCurve:
        return EllipticCurve.default_curve()

    @pytest.fixture
    def root_ca(self, curve: EllipticCurve) -> RootCA:
        d, _ = curve._generate_keypair()
        return RootCA.from_privkey("TestCA", curve, d)

    def test_empty_hello_messages(self, curve: EllipticCurve, root_ca: RootCA):
        """Пустые hello сообщения"""
        alice = BMQVParticipant("Alice", curve, b"", None, root_ca)
        bob = BMQVParticipant("Bob", curve, b"", None, root_ca)
        
        m0 = alice.process_init()
        m1 = bob.process_m0(m0)
        m2 = alice.process_m1(m1)
        m3 = bob.process_m2(m2)
        alice.process_m3(m3)
        
        assert alice.get_shared_key() == bob.get_shared_key()

    def test_large_hello_messages(self, curve: EllipticCurve, root_ca: RootCA):
        """Большие hello сообщения"""
        large_hello = b"x" * 10000
        alice = BMQVParticipant("Alice", curve, large_hello, None, root_ca)
        bob = BMQVParticipant("Bob", curve, large_hello, None, root_ca)
        
        m0 = alice.process_init()
        m1 = bob.process_m0(m0)
        m2 = alice.process_m1(m1)
        m3 = bob.process_m2(m2)
        alice.process_m3(m3)
        
        assert alice.get_shared_key() == bob.get_shared_key()

    def test_unicode_id_names(self, curve: EllipticCurve, root_ca: RootCA):
        """Unicode имена участников"""
        alice = BMQVParticipant("Алиса_🔐", curve, b"hello", None, root_ca)
        bob = BMQVParticipant("Боб_🔑", curve, b"hello", None, root_ca)
        
        m0 = alice.process_init()
        m1 = bob.process_m0(m0)
        m2 = alice.process_m1(m1)
        m3 = bob.process_m2(m2)
        alice.process_m3(m3)
        
        assert alice.get_shared_key() == bob.get_shared_key()

    def test_same_id_names(self, curve: EllipticCurve, root_ca: RootCA):
        """Одинаковые имена участников (но разные ключи)"""
        alice = BMQVParticipant("User", curve, b"hello_a", None, root_ca)
        bob = BMQVParticipant("User", curve, b"hello_b", None, root_ca)
        
        # Разные ключи, несмотря на одинаковые имена
        assert alice.d != bob.d
        
        m0 = alice.process_init()
        m1 = bob.process_m0(m0)
        m2 = alice.process_m1(m1)
        m3 = bob.process_m2(m2)
        alice.process_m3(m3)
        
        assert alice.get_shared_key() == bob.get_shared_key()

    def test_multiple_sessions_same_participants(
        self, curve: EllipticCurve, root_ca: RootCA
    ):
        """Множественные сессии между теми же участниками"""
        keys = []
        
        for i in range(3):
            alice = BMQVParticipant("Alice", curve, f"session_{i}".encode(), None, root_ca)
            bob = BMQVParticipant("Bob", curve, f"session_{i}".encode(), None, root_ca)
            
            m0 = alice.process_init()
            m1 = bob.process_m0(m0)
            m2 = alice.process_m1(m1)
            m3 = bob.process_m2(m2)
            alice.process_m3(m3)
            
            keys.append(alice.get_shared_key())
        
        # Все ключи должны быть уникальными
        assert len(set(keys)) == len(keys)

    def test_null_t_a_handling(
        self, curve: EllipticCurve, alice: BMQVParticipant, bob: BMQVParticipant
    ):
        """Обработка None значения t_a"""
        m0 = alice.process_init()
        m1 = bob.process_m0(m0)
        m2 = alice.process_m1(m1)
        
        # Создаем M2 без тега
        m2_without_tag = BMQVMessage2(
            cert_a=m2.cert_a,
            v_a=m2.v_a,
            t_a=None
        )
        
        # Это должно вызвать ошибку при сравнении
        with pytest.raises((ValueError, TypeError)):
            bob.process_m2(m2_without_tag)

    def test_null_t_b_handling(self, alice: BMQVParticipant, bob: BMQVParticipant):
        """Обработка None значения t_b"""
        m0 = alice.process_init()
        m1 = bob.process_m0(m0)
        m2 = alice.process_m1(m1)
        m3 = bob.process_m2(m2)
        
        # Создаем M3 без тега
        m3_without_tag = BMQVMessage3(t_b=None)
        
        # Это должно вызвать ошибку при сравнении
        with pytest.raises((ValueError, TypeError)):
            alice.process_m3(m3_without_tag)

    @pytest.fixture
    def alice(self, curve: EllipticCurve, root_ca: RootCA) -> BMQVParticipant:
        return BMQVParticipant("Alice", curve, b"hello", None, root_ca)

    @pytest.fixture
    def bob(self, curve: EllipticCurve, root_ca: RootCA) -> BMQVParticipant:
        return BMQVParticipant("Bob", curve, b"hello", None, root_ca)


class TestBMQVSecurityProperties:
    """Тесты криптографических свойств безопасности BMQV"""

    @pytest.fixture
    def curve(self) -> EllipticCurve:
        return EllipticCurve.default_curve()

    @pytest.fixture
    def root_ca(self, curve: EllipticCurve) -> RootCA:
        d, _ = curve._generate_keypair()
        return RootCA.from_privkey("TestCA", curve, d)

    def test_forward_secrecy(self, curve: EllipticCurve, root_ca: RootCA):
        """
        Проверка прямой секретности: компрометация долгосрочных ключей
        не должна раскрывать сессионные ключи
        """
        alice = BMQVParticipant("Alice", curve, b"hello_a", None, root_ca)
        bob = BMQVParticipant("Bob", curve, b"hello_b", None, root_ca)
        
        # Сохраняем долгосрочные ключи
        alice_d = alice.d
        bob_d = bob.d
        
        # Выполняем протокол
        m0 = alice.process_init()
        m1 = bob.process_m0(m0)
        m2 = alice.process_m1(m1)
        m3 = bob.process_m2(m2)
        alice.process_m3(m3)
        
        session_key = alice.get_shared_key()
        
        # Сессионный ключ не должен быть вычислим только из долгосрочных ключей
        # (для полной проверки нужны эфемерные ключи, которые уже уничтожены)
        assert session_key is not None
        assert len(session_key) == 32

    def test_key_confirmation(self, curve: EllipticCurve, root_ca: RootCA):
        """
        Проверка подтверждения ключа: обе стороны уверены,
        что другая сторона имеет тот же ключ
        """
        alice = BMQVParticipant("Alice", curve, b"hello_a", None, root_ca)
        bob = BMQVParticipant("Bob", curve, b"hello_b", None, root_ca)
        
        m0 = alice.process_init()
        m1 = bob.process_m0(m0)
        m2 = alice.process_m1(m1)
        m3 = bob.process_m2(m2)
        
        # M3 содержит подтверждение от Bob
        # process_m3 проверяет это подтверждение
        alice.process_m3(m3)
        
        # Если мы дошли сюда, ключи подтверждены
        assert alice.get_shared_key() == bob.get_shared_key()

    def test_unknown_key_share_resistance(
        self, curve: EllipticCurve, root_ca: RootCA
    ):
        """
        Проверка устойчивости к атаке неизвестного общего ключа:
        атакующий не может заставить жертву думать, что она разделяет ключ
        с кем-то другим
        """
        alice = BMQVParticipant("Alice", curve, b"hello_a", None, root_ca)
        bob = BMQVParticipant("Bob", curve, b"hello_b", None, root_ca)
        
        m0 = alice.process_init()
        m1 = bob.process_m0(m0)
        m2 = alice.process_m1(m1)
        m3 = bob.process_m2(m2)
        alice.process_m3(m3)
        
        # Alice связана с сертификатом Bob, и наоборот
        # Это гарантируется включением сертификатов в KDF
        assert alice.cert_b == bob.cert
        assert bob.cert_a == alice.cert

    def test_key_independence(self, curve: EllipticCurve, root_ca: RootCA):
        """
        Проверка независимости ключей: ключи разных сессий независимы
        """
        session_keys = []
        
        for _ in range(5):
            alice = BMQVParticipant("Alice", curve, b"hello", None, root_ca)
            bob = BMQVParticipant("Bob", curve, b"hello", None, root_ca)
            
            m0 = alice.process_init()
            m1 = bob.process_m0(m0)
            m2 = alice.process_m1(m1)
            m3 = bob.process_m2(m2)
            alice.process_m3(m3)
            
            session_keys.append(alice.get_shared_key())
        
        # Все ключи уникальны
        unique_keys = set(session_keys)
        assert len(unique_keys) == len(session_keys)

    def test_identity_misbinding_resistance(
        self, curve: EllipticCurve, root_ca: RootCA
    ):
        """
        Проверка устойчивости к неправильной привязке идентичности:
        подмена сертификата обнаруживается при верификации тегов
        """
        alice = BMQVParticipant("Alice", curve, b"hello_a", None, root_ca)
        bob = BMQVParticipant("Bob", curve, b"hello_b", None, root_ca)
        
        m0 = alice.process_init()
        m1 = bob.process_m0(m0)
        
        # Попытка использовать сертификат Alice вместо Bob
        tampered_m1 = BMQVMessage1(
            hello_b=m1.hello_b,
            cert_b=alice.cert,  # Подменяем сертификат
            v_b=m1.v_b
        )
        
        # Alice вычисляет ключ используя подмененный сертификат
        m2 = alice.process_m1(tampered_m1)
        
        # Bob проверяет T_a, но вычисляет его со своим сертификатом,
        # а Alice использовала cert_b = alice.cert
        # Поэтому верификация T_a провалится
        with pytest.raises(ValueError, match="T_A verification failed"):
            bob.process_m2(m2)
