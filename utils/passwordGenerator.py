import secrets
import string
def passwordGenerator(length):
    if length < 8:
        raise ValueError("Password length must be at least 8")
    password=[
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.digits),
        secrets.choice(string.punctuation)
    ]
    length=length-4

    passset=string.ascii_uppercase+string.ascii_lowercase+string.digits+string.punctuation
    password+=[secrets.choice(passset) for _ in range(length)]
    secrets.SystemRandom().shuffle(password)
    password="".join(password)
    return password