"""
Тесты для модуля cert.py - сертификаты и ECDSA
"""

import pytest
import secrets
import sys
import os

# Добавляем путь к app в PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from crypto.cert import (
    Certificate,
    RootCA,
    verify_cert,
    _hash_to_scalar,
    _serialize_sig,
    _deserialize_sig,
    _ecdsa_sign,
    _ecdsa_verify,
    _CERT_MAGIC,
)
from crypto.elliptic import EllipticCurve
from crypto.fmt import serialize_point


class TestHashToScalar:
    """Тесты для функции _hash_to_scalar"""

    @pytest.fixture
    def curve(self) -> EllipticCurve:
        return EllipticCurve.default_curve()

    def test_hash_to_scalar_deterministic(self, curve: EllipticCurve):
        """Хеширование детерминировано"""
        data = b"test data"
        result1 = _hash_to_scalar(curve, data)
        result2 = _hash_to_scalar(curve, data)
        assert result1 == result2

    def test_hash_to_scalar_different_inputs(self, curve: EllipticCurve):
        """Разные входные данные дают разные скаляры"""
        result1 = _hash_to_scalar(curve, b"data1")
        result2 = _hash_to_scalar(curve, b"data2")
        assert result1 != result2

    def test_hash_to_scalar_in_range(self, curve: EllipticCurve):
        """Результат в диапазоне [0, q)"""
        for _ in range(10):
            data = secrets.token_bytes(32)
            result = _hash_to_scalar(curve, data)
            assert 0 <= result < curve.q

    def test_hash_to_scalar_empty_data(self, curve: EllipticCurve):
        """Хеширование пустых данных"""
        result = _hash_to_scalar(curve, b"")
        assert 0 <= result < curve.q


class TestSignatureSerialization:
    """Тесты для сериализации подписей"""

    @pytest.fixture
    def curve(self) -> EllipticCurve:
        return EllipticCurve.default_curve()

    def test_serialize_deserialize_signature(self, curve: EllipticCurve):
        """Сериализация и десериализация подписи"""
        r = secrets.randbelow(curve.q - 1) + 1
        s = secrets.randbelow(curve.q - 1) + 1
        
        serialized = _serialize_sig(curve, r, s)
        r2, s2 = _deserialize_sig(curve, serialized)
        
        assert r == r2
        assert s == s2

    def test_signature_length(self, curve: EllipticCurve):
        """Длина подписи корректна"""
        r = 1
        s = 1
        serialized = _serialize_sig(curve, r, s)
        expected_len = 2 * (2 * curve.l // 8)
        assert len(serialized) == expected_len

    def test_deserialize_invalid_length(self, curve: EllipticCurve):
        """Десериализация подписи неправильной длины"""
        with pytest.raises(ValueError, match="invalid signature length"):
            _deserialize_sig(curve, b'\x00' * 10)

    def test_deserialize_empty(self, curve: EllipticCurve):
        """Десериализация пустой подписи"""
        with pytest.raises(ValueError, match="invalid signature length"):
            _deserialize_sig(curve, b'')


class TestECDSA:
    """Тесты для ECDSA подписи и верификации"""

    @pytest.fixture
    def curve(self) -> EllipticCurve:
        return EllipticCurve.default_curve()

    @pytest.fixture
    def keypair(self, curve: EllipticCurve):
        """Генерация ключевой пары для тестов"""
        d, Q = curve._generate_keypair()
        return d, Q

    def test_ecdsa_sign_verify_valid(self, curve: EllipticCurve, keypair):
        """Подпись и верификация валидного сообщения"""
        d, Q = keypair
        msg = b"test message"
        
        sig = _ecdsa_sign(curve, d, msg)
        assert _ecdsa_verify(curve, Q, msg, sig)

    def test_ecdsa_verify_wrong_message(self, curve: EllipticCurve, keypair):
        """Верификация с неправильным сообщением должна провалиться"""
        d, Q = keypair
        msg = b"test message"
        wrong_msg = b"wrong message"
        
        sig = _ecdsa_sign(curve, d, msg)
        assert not _ecdsa_verify(curve, Q, wrong_msg, sig)

    def test_ecdsa_verify_wrong_key(self, curve: EllipticCurve, keypair):
        """Верификация с неправильным ключом должна провалиться"""
        d, Q = keypair
        _, wrong_Q = curve._generate_keypair()
        msg = b"test message"
        
        sig = _ecdsa_sign(curve, d, msg)
        assert not _ecdsa_verify(curve, wrong_Q, msg, sig)

    def test_ecdsa_verify_tampered_signature_r(self, curve: EllipticCurve, keypair):
        """Подделка r части подписи должна быть обнаружена"""
        d, Q = keypair
        msg = b"test message"
        
        sig = _ecdsa_sign(curve, d, msg)
        r, s = _deserialize_sig(curve, sig)
        
        # Изменяем r
        tampered_r = (r + 1) % curve.q
        tampered_sig = _serialize_sig(curve, tampered_r, s)
        
        assert not _ecdsa_verify(curve, Q, msg, tampered_sig)

    def test_ecdsa_verify_tampered_signature_s(self, curve: EllipticCurve, keypair):
        """Подделка s части подписи должна быть обнаружена"""
        d, Q = keypair
        msg = b"test message"
        
        sig = _ecdsa_sign(curve, d, msg)
        r, s = _deserialize_sig(curve, sig)
        
        # Изменяем s
        tampered_s = (s + 1) % curve.q
        tampered_sig = _serialize_sig(curve, r, tampered_s)
        
        assert not _ecdsa_verify(curve, Q, msg, tampered_sig)

    def test_ecdsa_sign_invalid_privkey_zero(self, curve: EllipticCurve):
        """Подпись с нулевым приватным ключом должна выбросить исключение"""
        with pytest.raises(ValueError, match="invalid CA private key"):
            _ecdsa_sign(curve, 0, b"test")

    def test_ecdsa_sign_invalid_privkey_too_large(self, curve: EllipticCurve):
        """Подпись с слишком большим приватным ключом должна выбросить исключение"""
        with pytest.raises(ValueError, match="invalid CA private key"):
            _ecdsa_sign(curve, curve.q, b"test")

    def test_ecdsa_verify_signature_r_zero(self, curve: EllipticCurve, keypair):
        """Подпись с r=0 должна быть отклонена"""
        d, Q = keypair
        sig = _serialize_sig(curve, 0, 1)
        assert not _ecdsa_verify(curve, Q, b"test", sig)

    def test_ecdsa_verify_signature_s_zero(self, curve: EllipticCurve, keypair):
        """Подпись с s=0 должна быть отклонена"""
        d, Q = keypair
        sig = _serialize_sig(curve, 1, 0)
        assert not _ecdsa_verify(curve, Q, b"test", sig)

    def test_ecdsa_verify_signature_r_too_large(self, curve: EllipticCurve, keypair):
        """Подпись с r >= q должна быть отклонена"""
        d, Q = keypair
        sig = _serialize_sig(curve, curve.q, 1)
        assert not _ecdsa_verify(curve, Q, b"test", sig)

    def test_ecdsa_verify_signature_s_too_large(self, curve: EllipticCurve, keypair):
        """Подпись с s >= q должна быть отклонена"""
        d, Q = keypair
        sig = _serialize_sig(curve, 1, curve.q)
        assert not _ecdsa_verify(curve, Q, b"test", sig)

    def test_ecdsa_verify_pubkey_infinity(self, curve: EllipticCurve, keypair):
        """Верификация с бесконечной точкой должна провалиться"""
        d, Q = keypair
        sig = _ecdsa_sign(curve, d, b"test")
        assert not _ecdsa_verify(curve, None, b"test", sig)

    def test_ecdsa_verify_pubkey_not_on_curve(self, curve: EllipticCurve, keypair):
        """Верификация с точкой не на кривой должна провалиться"""
        d, Q = keypair
        sig = _ecdsa_sign(curve, d, b"test")
        fake_point = (12345, 67890)  # Скорее всего не на кривой
        assert not _ecdsa_verify(curve, fake_point, b"test", sig)

    def test_ecdsa_different_messages(self, curve: EllipticCurve, keypair):
        """Подписи разных сообщений должны отличаться"""
        d, Q = keypair
        sig1 = _ecdsa_sign(curve, d, b"message1")
        sig2 = _ecdsa_sign(curve, d, b"message2")
        assert sig1 != sig2

    def test_ecdsa_empty_message(self, curve: EllipticCurve, keypair):
        """Подпись и верификация пустого сообщения"""
        d, Q = keypair
        sig = _ecdsa_sign(curve, d, b"")
        assert _ecdsa_verify(curve, Q, b"", sig)

    def test_ecdsa_large_message(self, curve: EllipticCurve, keypair):
        """Подпись и верификация большого сообщения"""
        d, Q = keypair
        msg = b"x" * 10000
        sig = _ecdsa_sign(curve, d, msg)
        assert _ecdsa_verify(curve, Q, msg, sig)


class TestCertificate:
    """Тесты для класса Certificate"""

    @pytest.fixture
    def curve(self) -> EllipticCurve:
        return EllipticCurve.default_curve()

    def test_certificate_serialize_deserialize(self, curve: EllipticCurve):
        """Сериализация и десериализация сертификата"""
        pubkey = serialize_point(curve.G, curve.l, 4 * curve.l)
        sig = b'\x00' * len(pubkey)  # Фиктивная подпись той же длины
        
        cert = Certificate(id_name="test_user", pubkey=pubkey, sig=sig)
        serialized = cert.serialize()
        deserialized = Certificate.deserialize(serialized)
        
        assert deserialized.id_name == cert.id_name
        assert deserialized.pubkey == cert.pubkey
        assert deserialized.sig == cert.sig

    def test_certificate_empty_id_name(self, curve: EllipticCurve):
        """Сертификат с пустым id_name"""
        pubkey = serialize_point(curve.G, curve.l, 4 * curve.l)
        sig = b'\x00' * len(pubkey)
        
        cert = Certificate(id_name="", pubkey=pubkey, sig=sig)
        serialized = cert.serialize()
        deserialized = Certificate.deserialize(serialized)
        
        assert deserialized.id_name == ""

    def test_certificate_unicode_id_name(self, curve: EllipticCurve):
        """Сертификат с unicode id_name"""
        pubkey = serialize_point(curve.G, curve.l, 4 * curve.l)
        sig = b'\x00' * len(pubkey)
        
        cert = Certificate(id_name="тест_пользователь_🔐", pubkey=pubkey, sig=sig)
        serialized = cert.serialize()
        deserialized = Certificate.deserialize(serialized)
        
        assert deserialized.id_name == "тест_пользователь_🔐"

    def test_certificate_deserialize_too_short(self):
        """Десериализация слишком короткого сертификата"""
        with pytest.raises(ValueError, match="certificate too short"):
            Certificate.deserialize(b'\x00' * 5)

    def test_certificate_deserialize_invalid_magic(self):
        """Десериализация с неправильным magic"""
        with pytest.raises(ValueError, match="invalid certificate magic"):
            Certificate.deserialize(b'WRONG' + b'\x00' * 20)

    def test_certificate_deserialize_truncated_id(self):
        """Десериализация с обрезанным id"""
        data = _CERT_MAGIC + b'\xff\xff'  # id_len = 65535
        with pytest.raises(ValueError, match="certificate too short|invalid certificate"):
            Certificate.deserialize(data)

    def test_certificate_serialize_empty_signature(self, curve: EllipticCurve):
        """Сериализация с пустой подписью должна выбросить исключение"""
        pubkey = serialize_point(curve.G, curve.l, 4 * curve.l)
        cert = Certificate(id_name="test", pubkey=pubkey, sig=b'')
        
        with pytest.raises(ValueError, match="invalid signature length"):
            cert.serialize()

    def test_certificate_serialize_mismatched_lengths(self, curve: EllipticCurve):
        """Сериализация с несовпадающими длинами pubkey и sig"""
        pubkey = serialize_point(curve.G, curve.l, 4 * curve.l)
        sig = b'\x00' * (len(pubkey) + 1)  # Неправильная длина
        cert = Certificate(id_name="test", pubkey=pubkey, sig=sig)
        
        with pytest.raises(ValueError, match="invalid signature length"):
            cert.serialize()


class TestRootCA:
    """Тесты для класса RootCA"""

    @pytest.fixture
    def curve(self) -> EllipticCurve:
        return EllipticCurve.default_curve()

    @pytest.fixture
    def root_ca(self, curve: EllipticCurve) -> RootCA:
        d, _ = curve._generate_keypair()
        return RootCA.from_privkey("TestCA", curve, d)

    def test_root_ca_creation(self, curve: EllipticCurve):
        """Создание RootCA"""
        d, _ = curve._generate_keypair()
        ca = RootCA.from_privkey("TestCA", curve, d)
        
        assert ca.id_name == "TestCA"
        assert ca.privkey == d
        assert ca.pubkey is not None

    def test_root_ca_invalid_privkey_zero(self, curve: EllipticCurve):
        """Создание RootCA с нулевым privkey"""
        with pytest.raises(ValueError, match="invalid CA private key"):
            RootCA.from_privkey("TestCA", curve, 0)

    def test_root_ca_invalid_privkey_too_large(self, curve: EllipticCurve):
        """Создание RootCA с слишком большим privkey"""
        with pytest.raises(ValueError, match="invalid CA private key"):
            RootCA.from_privkey("TestCA", curve, curve.q)

    def test_root_ca_issue_cert(self, curve: EllipticCurve, root_ca: RootCA):
        """Выдача сертификата"""
        user_d, user_Q = curve._generate_keypair()
        user_pubkey = serialize_point(user_Q, curve.l, 4 * curve.l)
        
        cert = root_ca.issue_cert("Alice", user_pubkey)
        
        assert cert.id_name == "Alice"
        assert cert.pubkey == user_pubkey
        assert len(cert.sig) > 0

    def test_root_ca_issue_cert_no_privkey(self, curve: EllipticCurve):
        """Попытка выдачи сертификата без privkey"""
        d, Q = curve._generate_keypair()
        pubkey = serialize_point(Q, curve.l, 4 * curve.l)
        
        # Создаем CA только с публичным ключом
        ca = RootCA(id_name="TestCA", curve=curve, pubkey=pubkey, privkey=None)
        
        user_pubkey = serialize_point(curve.G, curve.l, 4 * curve.l)
        with pytest.raises(ValueError, match="CA private key is not available"):
            ca.issue_cert("User", user_pubkey)


class TestVerifyCert:
    """Тесты для функции verify_cert"""

    @pytest.fixture
    def curve(self) -> EllipticCurve:
        return EllipticCurve.default_curve()

    @pytest.fixture
    def root_ca(self, curve: EllipticCurve) -> RootCA:
        d, _ = curve._generate_keypair()
        return RootCA.from_privkey("TestCA", curve, d)

    def test_verify_valid_cert(self, curve: EllipticCurve, root_ca: RootCA):
        """Верификация валидного сертификата"""
        user_d, user_Q = curve._generate_keypair()
        user_pubkey = serialize_point(user_Q, curve.l, 4 * curve.l)
        
        cert = root_ca.issue_cert("Alice", user_pubkey)
        cert_bytes = cert.serialize()
        
        verified = verify_cert(cert_bytes, root_pubkey=root_ca.pubkey, curve=curve)
        
        assert verified.id_name == "Alice"
        assert verified.pubkey == user_pubkey

    def test_verify_cert_wrong_ca_key(self, curve: EllipticCurve, root_ca: RootCA):
        """Верификация с неправильным ключом CA должна провалиться"""
        user_d, user_Q = curve._generate_keypair()
        user_pubkey = serialize_point(user_Q, curve.l, 4 * curve.l)
        
        cert = root_ca.issue_cert("Alice", user_pubkey)
        cert_bytes = cert.serialize()
        
        # Создаем другой CA
        fake_d, fake_Q = curve._generate_keypair()
        fake_pubkey = serialize_point(fake_Q, curve.l, 4 * curve.l)
        
        with pytest.raises(ValueError, match="certificate signature invalid"):
            verify_cert(cert_bytes, root_pubkey=fake_pubkey, curve=curve)

    def test_verify_cert_expected_id_name_match(self, curve: EllipticCurve, root_ca: RootCA):
        """Верификация с совпадающим expected_id_name"""
        user_d, user_Q = curve._generate_keypair()
        user_pubkey = serialize_point(user_Q, curve.l, 4 * curve.l)
        
        cert = root_ca.issue_cert("Alice", user_pubkey)
        cert_bytes = cert.serialize()
        
        verified = verify_cert(
            cert_bytes,
            root_pubkey=root_ca.pubkey,
            curve=curve,
            expected_id_name="Alice"
        )
        assert verified.id_name == "Alice"

    def test_verify_cert_expected_id_name_mismatch(self, curve: EllipticCurve, root_ca: RootCA):
        """Верификация с несовпадающим expected_id_name должна провалиться"""
        user_d, user_Q = curve._generate_keypair()
        user_pubkey = serialize_point(user_Q, curve.l, 4 * curve.l)
        
        cert = root_ca.issue_cert("Alice", user_pubkey)
        cert_bytes = cert.serialize()
        
        with pytest.raises(ValueError, match="certificate id binding invalid"):
            verify_cert(
                cert_bytes,
                root_pubkey=root_ca.pubkey,
                curve=curve,
                expected_id_name="Bob"
            )

    def test_verify_cert_tampered_id_name(self, curve: EllipticCurve, root_ca: RootCA):
        """Подмена id_name в сертификате должна быть обнаружена"""
        user_d, user_Q = curve._generate_keypair()
        user_pubkey = serialize_point(user_Q, curve.l, 4 * curve.l)
        
        cert = root_ca.issue_cert("Alice", user_pubkey)
        cert_bytes = cert.serialize()
        
        # Изменяем id_name в сериализованном сертификате
        tampered = cert_bytes.replace(b"Alice", b"Bob__")  # Сохраняем длину
        
        with pytest.raises(ValueError, match="certificate signature invalid"):
            verify_cert(tampered, root_pubkey=root_ca.pubkey, curve=curve)

    def test_verify_cert_tampered_pubkey(self, curve: EllipticCurve, root_ca: RootCA):
        """Подмена pubkey в сертификате должна быть обнаружена"""
        user_d, user_Q = curve._generate_keypair()
        user_pubkey = serialize_point(user_Q, curve.l, 4 * curve.l)
        
        cert = root_ca.issue_cert("Alice", user_pubkey)
        
        # Создаем новый публичный ключ
        _, fake_Q = curve._generate_keypair()
        fake_pubkey = serialize_point(fake_Q, curve.l, 4 * curve.l)
        
        # Подменяем pubkey
        tampered_cert = Certificate(
            id_name=cert.id_name,
            pubkey=fake_pubkey,  # Подмененный ключ
            sig=cert.sig  # Оригинальная подпись
        )
        tampered_bytes = tampered_cert.serialize()
        
        with pytest.raises(ValueError, match="certificate signature invalid"):
            verify_cert(tampered_bytes, root_pubkey=root_ca.pubkey, curve=curve)

    def test_verify_cert_tampered_signature(self, curve: EllipticCurve, root_ca: RootCA):
        """Подмена подписи в сертификате должна быть обнаружена"""
        user_d, user_Q = curve._generate_keypair()
        user_pubkey = serialize_point(user_Q, curve.l, 4 * curve.l)
        
        cert = root_ca.issue_cert("Alice", user_pubkey)
        
        # Изменяем подпись
        tampered_sig = bytes([b ^ 0xFF for b in cert.sig[:8]]) + cert.sig[8:]
        tampered_cert = Certificate(
            id_name=cert.id_name,
            pubkey=cert.pubkey,
            sig=tampered_sig
        )
        tampered_bytes = tampered_cert.serialize()
        
        with pytest.raises(ValueError, match="certificate signature invalid"):
            verify_cert(tampered_bytes, root_pubkey=root_ca.pubkey, curve=curve)

    def test_verify_cert_forged_by_attacker(self, curve: EllipticCurve, root_ca: RootCA):
        """Атакующий не может создать валидный сертификат без ключа CA"""
        # Атакующий создает свой CA
        attacker_d, attacker_Q = curve._generate_keypair()
        attacker_ca = RootCA.from_privkey("AttackerCA", curve, attacker_d)
        
        # Атакующий выдает сертификат от своего имени
        victim_d, victim_Q = curve._generate_keypair()
        victim_pubkey = serialize_point(victim_Q, curve.l, 4 * curve.l)
        
        forged_cert = attacker_ca.issue_cert("Victim", victim_pubkey)
        forged_bytes = forged_cert.serialize()
        
        # Этот сертификат не пройдет верификацию с ключом настоящего CA
        with pytest.raises(ValueError, match="certificate signature invalid"):
            verify_cert(forged_bytes, root_pubkey=root_ca.pubkey, curve=curve)


class TestCertificateForgeryResistance:
    """Тесты на устойчивость к подделке сертификатов"""

    @pytest.fixture
    def curve(self) -> EllipticCurve:
        return EllipticCurve.default_curve()

    @pytest.fixture
    def root_ca(self, curve: EllipticCurve) -> RootCA:
        d, _ = curve._generate_keypair()
        return RootCA.from_privkey("TestCA", curve, d)

    def test_cannot_reuse_signature_for_different_id(self, curve: EllipticCurve, root_ca: RootCA):
        """Нельзя переиспользовать подпись для другого id"""
        user_d, user_Q = curve._generate_keypair()
        user_pubkey = serialize_point(user_Q, curve.l, 4 * curve.l)
        
        cert = root_ca.issue_cert("Alice", user_pubkey)
        
        # Пытаемся использовать ту же подпись для "Bob"
        forged_cert = Certificate(
            id_name="Bob",
            pubkey=cert.pubkey,
            sig=cert.sig
        )
        forged_bytes = forged_cert.serialize()
        
        with pytest.raises(ValueError, match="certificate signature invalid"):
            verify_cert(forged_bytes, root_pubkey=root_ca.pubkey, curve=curve)

    def test_cannot_reuse_signature_for_different_pubkey(self, curve: EllipticCurve, root_ca: RootCA):
        """Нельзя переиспользовать подпись для другого pubkey"""
        user_d, user_Q = curve._generate_keypair()
        user_pubkey = serialize_point(user_Q, curve.l, 4 * curve.l)
        
        cert = root_ca.issue_cert("Alice", user_pubkey)
        
        # Генерируем другой публичный ключ
        _, other_Q = curve._generate_keypair()
        other_pubkey = serialize_point(other_Q, curve.l, 4 * curve.l)
        
        forged_cert = Certificate(
            id_name="Alice",
            pubkey=other_pubkey,
            sig=cert.sig
        )
        forged_bytes = forged_cert.serialize()
        
        with pytest.raises(ValueError, match="certificate signature invalid"):
            verify_cert(forged_bytes, root_pubkey=root_ca.pubkey, curve=curve)

    def test_bit_flip_in_signature_detected(self, curve: EllipticCurve, root_ca: RootCA):
        """Изменение одного бита в подписи должно быть обнаружено"""
        user_d, user_Q = curve._generate_keypair()
        user_pubkey = serialize_point(user_Q, curve.l, 4 * curve.l)
        
        cert = root_ca.issue_cert("Alice", user_pubkey)
        cert_bytes = cert.serialize()
        
        # Изменяем один бит в подписи (последние байты сертификата)
        flipped = bytearray(cert_bytes)
        flipped[-1] ^= 0x01
        
        with pytest.raises(ValueError):
            verify_cert(bytes(flipped), root_pubkey=root_ca.pubkey, curve=curve)

    def test_multiple_certificates_unique_signatures(self, curve: EllipticCurve, root_ca: RootCA):
        """Сертификаты для разных пользователей имеют разные подписи"""
        pubkey = serialize_point(curve.G, curve.l, 4 * curve.l)
        
        cert1 = root_ca.issue_cert("Alice", pubkey)
        cert2 = root_ca.issue_cert("Bob", pubkey)
        
        assert cert1.sig != cert2.sig
