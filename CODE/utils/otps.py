import random


def generate_otp() -> int:
    """
    Function to generate OTP
    :return: 6 digit OTP
    """
    return random.randint(100000, 999999)
