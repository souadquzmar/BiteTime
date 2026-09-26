from pathlib import Path
from uuid import uuid4


def generate_object_key(file_name: str) -> str:
    extension = Path(file_name).suffix
    return f"uploads/{uuid4()}{extension}"
