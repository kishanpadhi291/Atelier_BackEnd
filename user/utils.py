import random

from otp_generator.otp import generate_otp

def generateotp():
    length = random.randint(3, 9)
    return generate_otp(length)

def generatepassword():
    length = random.randint(6, 25)
    return generate_otp(length)
