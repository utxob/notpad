from Crypto.PublicKey import RSA

# RSA কী জেনারেট করা
key = RSA.generate(2048)

# প্রাইভেট কী ফাইল হিসেবে সংরক্ষণ
private_key = key.export_key()
with open("private.pem", "wb") as priv_file:
    priv_file.write(private_key)

# পাবলিক কী ফাইল হিসেবে সংরক্ষণ
public_key = key.publickey().export_key()
with open("public.pem", "wb") as pub_file:
    pub_file.write(public_key)

print("Keys Generated: private.pem and public.pem")
