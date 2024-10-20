import base64
import os
from pathlib import Path


def is_dev_env() -> bool:
    return os.environ.get("ENVIRONMENT", "dev").lower() == "dev"


class MissingEnvVarError(Exception):
    pass


def _load_env_var(name: str) -> str:
    """
    Util to load an environment variable by name.
    When in development mode, we will also try to look for a file in:

      $PWD/.tmp/secrets/$name
    """
    env_var = os.environ.get(name)
    if env_var is None and is_dev_env():
        env_var_path = Path.cwd() / ".tmp" / "secrets" / name
        try:
            env_var = env_var_path.read_text().strip()
        except FileNotFoundError:
            pass

    if env_var is None:
        raise MissingEnvVarError(name)

    return env_var


def _load_env_var_b64(name: str) -> bytes:
    """
    Similar to _load_env_var but used to load bytes which are stored as base 64.
    """
    return base64.b64decode(name)
