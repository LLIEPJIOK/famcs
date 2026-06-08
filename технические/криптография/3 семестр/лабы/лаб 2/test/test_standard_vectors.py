"""
Тесты на соответствие стандарту СТБ 34.101.45 (Приложение Б)
Проверочные примеры из таблиц Б.1 и Б.2

Все значения в стандарте представлены в little-endian формате.
"""

import pytest
import sys
import os
from unittest.mock import patch, MagicMock
from dataclasses import dataclass

# Добавляем путь к app в PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from crypto.elliptic import EllipticCurve
from crypto.fmt import serialize_point, serialize_int, deserialize_point
from crypto.tzi_wrapper import belt_hash, bake_kdf, belt_mac
from crypto.bmqv import BMQVParticipant, BMQVMessage0, BMQVMessage1, BMQVMessage2, BMQVMessage3
from crypto.cert import RootCA, Certificate


def hex_to_bytes(hex_str: str) -> bytes:
    """Конвертирует hex строку в bytes (little-endian)"""
    hex_clean = hex_str.replace(" ", "").replace("_16", "")
    return bytes.fromhex(hex_clean)


def hex_to_int(hex_str: str) -> int:
    """Конвертирует hex строку в int (little-endian)"""
    return int.from_bytes(hex_to_bytes(hex_str), "little")


@dataclass
class SimplifiedCert:
    """Упрощённый сертификат из стандарта: cert = id || Q"""
    id_name: str
    pubkey: bytes
    
    def serialize(self) -> bytes:
        return self.id_name.encode('utf-8') + self.pubkey

class TestStandardVectorsFullProtocol:
    """
    Полный тест протокола BMQV с тестовыми векторами из стандарта СТБ 34.101.45
    Используем реальные функции BMQVParticipant с фиксированными значениями из стандарта.
    """

    ID_A = "416C6963 65"
    D_A_HEX = "1F66B5B8 4B733967 4533F032 9C74F218 34281FED 0732429E 0C79235F C273E269"
    Q_A_HEX = "BD1A5650 179D79E0 3FCEE49D 4C2BD5DD F54CE46D 0CF11E4F F87BF7A8 90857FD0 7AC6A603 61E8C817 3491686D 461B2826 190C2EDA 5909054A 9AB84D2A B9D99A90"

    ID_B = "426F62"
    D_B_HEX = "4C0E74B2 CD5811AD 21F23DE7 E0FA742C 3ED6EC48 3C461CE1 5C33A77A A308B7D2"
    Q_B_HEX = "CCEEF1A3 13A40664 9D15DA0A 851D486A 695B641B 20611776 252FFDCE 39C71060 7C9EA1F3 3C23D20D FCB8485A 88BE6523 A28ECC32 15B47FA2 89D6C9BE 1CE837C0"

    U_B_HEX = "0F51D913 47617C20 BD4AB07A EF4F26A1 AD1362A8 F9A3D42F BE1B8E6F 1C88AAD5"
    V_B_HEX = "9B4EA669 DABDF100 A7D4B6E6 EB76EE52 51912531 F426750A AC8A9DBB 51C54D8D 6AB7DBF1 5FCBD768 EE68A173 F7B236EF C15A01E2 AA6CD1FE 98B947DA 7B38A2A0"

    U_A_HEX = "0A4E8298 BE0839E4 6F19409F 637F4415 572251DD 0D39284F 0F0390D9 3BBCE9EC"
    V_A_HEX = "1D5A382B 962D4ED0 6193258C A6DE535D 8FD7FACB 853171E9 32EF93B5 EE800120 03DBB7B5 BD070363 80BAFA47 FCA7E6CA 3F179EDD D1AE5086 64790918 3628EDDC"

    T_HEX = "BD46F58A DE7C4DF9 826D32AB A9113428"
    S_A_HEX = "AB4EB3A6 D867C861 52E61B64 7F1A32D9 93A7768F 79361F75 0AE7C7A6 5CD9A233"

    K_HEX = "7FF3A0DA CDFECB3C D25F4D3C 334CCCB3 34C71FF7 1E2247DD 0688FA62 DF4C5920 728CB855 98DA04B4 8D85D32D 0CDCCD92 3D88E844 9BAA5065 B4E4D1CB EEE31D35"
    K0_HEX = "C6F86D0E 468D5EF1 A9955B2E E0CF0581 050C81D1 B4772709 2408E863 C7EEB48C"
    K1_HEX = "E95BA3F6 45C58288 E8A1B37C 10ADD336 DB8BD7F6 75F94963 139769F2 E260C6A9"

    T_A_HEX = "413B7E18 1BAFB337"

    S_B_HEX = "B6099633 2B62DDB1 354EC03D A949B528 99E6CA6D 08848C94 013B9CF6 FF42AEED"
    T_B_HEX = "B800A203 3AC7591B"

    @pytest.fixture
    def curve(self) -> EllipticCurve:
        return EllipticCurve.default_curve()

    @pytest.fixture
    def root_ca(self, curve: EllipticCurve) -> RootCA:
        """Создаем CA для выдачи сертификатов"""
        # Используем произвольный приватный ключ для CA
        ca_d = 0x1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF % curve.q
        if ca_d == 0:
            ca_d = 1
        return RootCA.from_privkey("TestCA", curve, ca_d)

    def test_full_protocol_with_simplified_certs(self, curve: EllipticCurve):
        """
        Полный тест протокола BMQV с упрощёнными сертификатами из стандарта.
        Сертификаты: cert = id || Q (без подписи CA).
        Мокаем verify_cert чтобы принимать упрощённые сертификаты.
        """
        # Загружаем ключи из стандарта
        d_a = hex_to_int(self.D_A_HEX)
        d_b = hex_to_int(self.D_B_HEX)
        Q_a_bytes = hex_to_bytes(self.Q_A_HEX)
        Q_b_bytes = hex_to_bytes(self.Q_B_HEX)
        Q_a = deserialize_point(Q_a_bytes, curve.l)
        Q_b = deserialize_point(Q_b_bytes, curve.l)

        u_a = hex_to_int(self.U_A_HEX)
        u_b = hex_to_int(self.U_B_HEX)

        # Упрощённые сертификаты как в стандарте
        cert_a = SimplifiedCert(id_name="Alice", pubkey=Q_a_bytes)
        cert_b = SimplifiedCert(id_name="Bob", pubkey=Q_b_bytes)

        # Мок для verify_cert - возвращает Certificate-подобный объект
        def mock_verify_cert(cert_bytes, root_pubkey, curve, expected_id_name=None):
            # Парсим упрощённый сертификат: первые байты - id, остальное - pubkey
            # Для Alice: "Alice" (5 байт) + Q_A (64 байт)
            # Для Bob: "Bob" (3 байта) + Q_B (64 байт)
            pubkey_len = 4 * curve.l // 8  # 64 байта для l=128
            id_bytes = cert_bytes[:-pubkey_len]
            pubkey = cert_bytes[-pubkey_len:]
            id_name = id_bytes.decode('utf-8')
            
            if expected_id_name is not None and id_name != expected_id_name:
                raise ValueError(f"ID mismatch: {id_name} != {expected_id_name}")
            
            # Возвращаем объект с полями id_name и pubkey
            return Certificate(id_name=id_name, pubkey=pubkey, sig=pubkey)  # sig не используется

        # Создаём мок RootCA
        mock_root_ca = MagicMock()
        mock_root_ca.pubkey = (1, 1)  # Не используется при моке verify_cert

        # Создаем участников с упрощёнными сертификатами
        with patch('crypto.bmqv.verify_cert', mock_verify_cert):
            alice = BMQVParticipant(
                id_name="Alice",
                curve=curve,
                hello=b"",
                cert=cert_a.serialize(),
                root_ca=mock_root_ca,
                d=d_a,
                Q=Q_a
            )

            bob = BMQVParticipant(
                id_name="Bob",
                curve=curve,
                hello=b"",
                cert=cert_b.serialize(),
                root_ca=mock_root_ca,
                d=d_b,
                Q=Q_b
            )

            # Мокаем генерацию случайных чисел
            random_values = iter([u_b, u_a])
            def mock_randbelow(n):
                return next(random_values)

            with patch('crypto.bmqv.secrets.randbelow', mock_randbelow):
                # Alice -> Bob: M0
                m0 = alice.process_init()

                # Bob -> Alice: M1
                m1 = bob.process_m0(
                    m0,
                    expected_v_b=hex_to_bytes(self.V_B_HEX),
                )

                # Alice -> Bob: M2
                # Примечание: T_A и T_B зависят от belt_mac, который в TZI
                # реализован иначе чем в стандарте. Проверяем K, K0, K1.
                m2 = alice.process_m1(
                    m1,
                    expected_v_a=hex_to_bytes(self.V_A_HEX),
                    expected_t=hex_to_bytes(self.T_HEX),
                    expected_s_a=hex_to_bytes(self.S_A_HEX),
                    expected_K=hex_to_bytes(self.K_HEX),
                    expected_K0=hex_to_bytes(self.K0_HEX),
                    expected_K1=hex_to_bytes(self.K1_HEX),
                    expected_T_a=hex_to_bytes(self.T_A_HEX)
                )

                # Bob -> Alice: M3
                m3 = bob.process_m2(
                    m2,
                    expected_K=hex_to_bytes(self.K_HEX),
                    expected_K0=hex_to_bytes(self.K0_HEX),
                    expected_K1=hex_to_bytes(self.K1_HEX),
                    expected_T_b=hex_to_bytes(self.T_B_HEX),
                )

                # Alice проверяет M3
                alice.process_m3(m3)

                # Проверяем K0 из стандарта
                K0_expected = hex_to_bytes(self.K0_HEX)
                assert alice.get_shared_key() == K0_expected, f"K0 Alice не совпадает: {alice.get_shared_key().hex()}"
                assert bob.get_shared_key() == K0_expected, f"K0 Bob не совпадает: {bob.get_shared_key().hex()}"
