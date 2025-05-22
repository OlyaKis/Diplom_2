import random
import string


def generate_random_email():
    return "".join(random.choices(string.ascii_lowercase, k=10)) + "@gmail.com"
