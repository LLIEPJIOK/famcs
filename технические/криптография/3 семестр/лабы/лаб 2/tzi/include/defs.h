#ifndef DEFS_H
#define DEFS_H

#include <stdint.h>
#include <stddef.h> 

////////////////////////////////////////////////////////////////////////////////////////////////////

enum err_type {
    ERR_OK = 0,                         // корректная работа
    ERR_OUT_OF_MEMORY  = 1,             // ошибки при работе с памятью
    ERR_BAD_PARAMS = 2,                 // неверные значения параметров
    ERR_BAD_INPUT = 3,                  // неверные входные параметры
    ERR_BAD_RANDOM = 4,                 // в функцию tzi_bign_genkeypair() передано недостаточно случайных данных
    ERR_BAD_PRIVKEY = 5,                // неверный личный ключ
    ERR_BAD_ONETIME_PRIVKEY = 6,        // неверный одноразовый личный ключ
    ERR_BAD_PUBKEY = 7,                 // ошибка при проверке открытого ключа
    ERR_BAD_MAC = 8,                    // ошибка при проверке имитовставки
    ERR_BAD_KEYTOKEN = 9,               // ошибка при расшифровании защищенного ключа или при разборе токена ключа
    ERR_BAD_SIG = 10,                   // ошибка при проверке подписи
    ERR_BAD_DATA_LENGTH = 11,           // ошибка при проверке размера входного блока данных
    ERR_BAD_OPERATION_TYPE = 12         // попытка использовать контекст для одного режима шифрования для другого режима
};

enum op_type {
    ENCRYPT = 1,        // зашифрование
    DECRYPT = 2         // расшифрование
};

enum cipher_mode {
    ECB = 1,            // шифрование в режиме простой замены
    CBC = 2,            // шифрование в режиме сцепления блоков
    CFB = 3,            // шифрование в режиме гаммирования с обратной связью
    CTR = 4,            // шифрование в режиме счетчика
    MAC = 5,            // имитозащита на основе шифрования
    DWP = 6,            // аутентифицированное шифрование данных (схема 1)
    CHE = 7,            // аутентифицированное шифрование данных (схема 2)
    KWP = 8             // аутентифицированное шифрование ключа
};

////////////////////////////////////////////////////////////////////////////////////////////////////

typedef enum err_type err_type;
typedef enum op_type op_type;
typedef enum cipher_mode cipher_mode;

////////////////////////////////////////////////////////////////////////////////////////////////////

typedef struct belt_ctx
{
    uint8_t k[32];
    uint8_t s[16];
    uint8_t r[16];
    uint8_t t[16];
    uint64_t i_size;
    uint64_t x_size;
    op_type ot;
    cipher_mode cm;
} belt_ctx;

////////////////////////////////////////////////////////////////////////////////////////////////////

typedef struct hash_ctx
{
    union
    {
        struct
        {
            uint8_t buf[32];
            uint8_t h[32];
            uint8_t r[16];
            uint8_t s[16];
            uint8_t t[16];
            size_t pos;
        } hbelt;
        struct
        {
            uint8_t s[192];
            uint16_t buf_len;
            size_t pos;
            uint16_t l;
        } bash;
    };
} hash_ctx;

typedef struct hashFunc
{
    enum err_type(*hash_start)(hash_ctx* ctx);
    enum err_type(*hash_step)(hash_ctx* ctx, const uint8_t* buf, size_t count);
    enum err_type(*hash_finish)(hash_ctx* ctx, uint8_t* hash);
    enum err_type(*hash)(const uint8_t*, const size_t, uint8_t*);
    uint16_t b;
    uint16_t l;
} hashFunc;

////////////////////////////////////////////////////////////////////////////////////////////////////

typedef struct hmac_ctx
{
    hash_ctx hctx;
    uint8_t t[128];
    hashFunc hF;
} hmac_ctx;

typedef struct brng_ctr_ctx
{
    uint8_t k[64];
    uint8_t s[64];
    uint8_t r[64];
    uint8_t x[64];
    hashFunc hF;
} brng_ctr_ctx ;

typedef struct brng_hmac_ctx
{
    uint8_t r[64];
    const uint8_t* k;
    size_t k_size;
    const uint8_t* s;
    size_t s_size;
    hashFunc hF;
} brng_hmac_ctx;

////////////////////////////////////////////////////////////////////////////////////////////////////

typedef struct bign_curve
{
    uint8_t p[64];
    uint8_t a[64];
    uint8_t b[64];
    uint8_t q[64];
    uint8_t yG[64];
    uint8_t f_size;
} bign_curve;

////////////////////////////////////////////////////////////////////////////////////////////////////

static const uint8_t OID_BELT_HASH[] = { 0x06, 0x09, 0x2A, 0x70, 0x00, 0x02, 0x00, 0x22, 0x65, 0x1F, 0x51 };
static const uint8_t OID_BASH256[] = {  0x06, 0x09, 0x2A, 0x70, 0x00, 0x02, 0x00, 0x22, 0x65, 0x4D, 0x0B };
static const uint8_t OID_BASH384[] = {  0x06, 0x09, 0x2A, 0x70, 0x00, 0x02, 0x00, 0x22, 0x65, 0x4D, 0x0C };
static const uint8_t OID_BASH512[] = {  0x06, 0x09, 0x2A, 0x70, 0x00, 0x02, 0x00, 0x22, 0x65, 0x4D, 0x0D };

////////////////////////////////////////////////////////////////////////////////////////////////////

#endif //DEFS_H
