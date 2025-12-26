import os

def get_required_env(key: str) -> str:
    """
    Fetch a required environment variable.
    Fails fast if missing.
    """
    value = os.getenv(key)

    if not value:
        raise RuntimeError(
            f"Missing required environment variable: {key}"
        )

    return value






