from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import rsa

app = FastAPI()


class PublicKey(BaseModel):
    e: str
    n: str


class PrivateKey(BaseModel):
    d: str
    n: str
    p: str
    q: str


class KeysResponse(BaseModel):
    public_key: PublicKey
    private_key: PrivateKey


class EncryptRequest(BaseModel):
    message: str
    e: str
    n: str


class DecryptRequest(BaseModel):
    cipher: str
    d: str
    n: str
    p: str
    q: str


@app.post("/generate_keys", response_model=KeysResponse)
def generate_keys_endpoint(bits: int = 2048):
    pubkey, privkey = rsa.generate_keys(bits)
    return {
        "public_key": {
            "e": str(pubkey[0]),
            "n": str(pubkey[1]),
        },
        "private_key": {
            "d": str(privkey[0]),
            "n": str(privkey[1]),
            "p": str(privkey[2]),
            "q": str(privkey[3]),
        },
    }

@app.post("/encrypt")
def encrypt_endpoint(req: EncryptRequest):
    pubkey = (int(req.e), int(req.n))
    encrypted = rsa.encrypt(req.message, pubkey)
    return {"cipher": encrypted}


@app.post("/decrypt")
def decrypt_endpoint(req: DecryptRequest):
    privkey = (int(req.d), int(req.n), int(req.p), int(req.q))
    decrypted = rsa.decrypt(req.cipher, privkey)
    return {"decrypted": decrypted}
