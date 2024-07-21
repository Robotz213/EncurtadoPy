import string
import random

def generate_id() -> str:
    
    while True:
        # Gerar 4 letras maiúsculas e 4 dígitos
        letters = random.sample(string.ascii_uppercase, 3)
        digits = random.sample(string.digits, 3)

        # Intercalar letras e dígitos
        id = ''.join([letters[i//2] if i % 2 == 0 else digits[i//2] for i in range(6)])

        # Verificar se a string gerada não contém sequências do tipo "AABB"
        if not any(id[i] == id[i + 1] for i in range(len(id) - 1)):
            return id