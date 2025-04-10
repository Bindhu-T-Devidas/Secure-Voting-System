from Crypto.PublicKey import RSA

key = RSA.generate(2048)

with open("private.pem", "wb") as f:
    f.write(key.export_key())

with open("public.pem", "wb") as f:
    f.write(key.publickey().export_key())

print("✅ RSA keys generated: private.pem (server), public.pem (client)")
