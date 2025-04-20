import random

def generate_verification_code():
    return str(random.randint(1000, 9999))

def send_sms(phone_number, message):
    """
    SMS yuborishni simulatsiya qiladi.
    Konsolga xabar chiqariladi.
    """
    print(f"SMS {phone_number} raqamiga yuborildi: {message}")
    #Simulatsiya muvoffaqiyatli bo'ldi deb hisoblaymiz
    return True            