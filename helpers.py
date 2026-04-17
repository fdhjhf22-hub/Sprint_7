import random
import string


def generate_random_string(length: int) -> str:
    """Генерирует строку из случайных букв нижнего регистра заданной длины."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))