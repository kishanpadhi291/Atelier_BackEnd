import random

from otp_generator.otp import generate_otp

def generateotp():
    length = 6
    otp = ''.join(random.choice('0123456789') for _ in range(length))
    return otp

# def generatepassword():
#     length = random.randint(6, 25)
#     return generate_otp(length)
