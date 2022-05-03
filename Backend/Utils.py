import hashlib
from random import Random

# Attualmente non impiegato
DEFAULT_NONCE_LENGTH = 128

# attualmente non impiegato
random = Random()


# Al momento non usata (usata per comunicazione con scramp)
def generate_nonce(length=DEFAULT_NONCE_LENGTH):
    s = ""

    for a in range(length):
        i = random.randint(33, 126)  # Caratteri contemplati da UTF-8 che non sono caratteri speciali.
        charachter = chr(i)
        s = s + charachter

    return s


def hash_str(s: str):
    """
    Hasha la stringa con SHA-256.
    :param s: Stringa da hashare.
    :return: Stringa hashata in SHA-256.
    """
    return hashlib.sha256(s.encode()).hexdigest()
