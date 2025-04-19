from cryptography.fernet import Fernet  # Fernet ➝ Data ko encrypt aur decrypt karne ke liye use hota hai .
import hashlib  # hashlib ➝ Passkey ka hash banata hai, taake usay directly store na karna pade.


FERNET_KEY = Fernet.generate_key() #Ek random secure key generate karta hai (har bar nayi).
fernet = Fernet(FERNET_KEY) #  Is key ko use karke ek Fernet object banate hain jo encryption/decryption karega.

def encrypt_data(text):
    """    
    text.encode() ➝ Text ko bytes mein convert karta hai (Fernet ko bytes chahiye hoti hain).
    fernet.encrypt(...) ➝ Text ko encrypted format mein badal deta hai.
    .decode() ➝ Encrypted bytes ko wapas string bana deta hai (file mein store karne ke liye).
    """
    return fernet.encrypt(text.encode()).decode()

def decrypt_data(cipher_text):
    """
    cipher_text.encode() ➝ Encrypted string ko bytes banata hai.
    fernet.decrypt(...) ➝ Bytes ko decrypt karke original data return karta hai.
    .decode() ➝ Original text ko string bana deta hai.
    """
    return fernet.decrypt(cipher_text.encode()).decode()

def hash_passkey(passkey):
    """
    passkey.encode() ➝ Bytes mein convert karta hai.
    hashlib.sha256(...) ➝ SHA-256 hash object banata hai.
    .hexdigest() ➝ Final hash ko string format mein return karta hai.
   """
    return hashlib.sha256(passkey.encode()).hexdigest()