import pickle
import os
from functools import wraps
import hashlib
import base64
import inspect


def get_hash_filename(filename: str):
    hash_obj = hashlib.sha1()
    hash_obj.update(filename.encode())
    hash_bytes = hash_obj.digest()
    hash_base64 = base64.urlsafe_b64encode(hash_bytes).rstrip(b"=").decode()

    return f"{hash_base64}.pkl"


def get_caller_dirname():
    caller_frame = inspect.stack()[1]
    caller_dirname = os.path.dirname(os.path.abspath(caller_frame.filename))
    return caller_dirname


def get_caller_filename():
    caller_frame = inspect.stack()[1]
    caller_filename = caller_frame.filename
    return caller_filename


def cache(caller_name: str | None, max_m_bytes: int = 10, verbose: bool = False):
    def decorator(func):
        caller_filename = caller_name or get_caller_filename()
        cache_name = f"{caller_filename}_{func.__name__}"
        cache_filename = f"{cache_name}.pkl"

        if len(cache_filename) > 255:
            cache_filename = get_hash_filename(cache_name)

        script_dir = get_caller_dirname()

        cache_dir = os.path.join(script_dir, ".cache")
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        cache_filepath = os.path.join(cache_dir, cache_filename)

        if os.path.exists(cache_filepath):
            with open(cache_filepath, "rb") as f:
                cache_data = pickle.load(f)
        else:
            cache_data = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = (args, tuple(sorted(kwargs.items())))

            if cache_key in cache_data:
                if verbose:
                    print(f"\033[32mCache hit:\033[0m {func.__name__}{cache_key}")
                return cache_data[cache_key]

            result = func(*args, **kwargs)
            cache_data[cache_key] = result

            data_to_dump = pickle.dumps(cache_data)
            if len(data_to_dump) < max_m_bytes * 1024 * 1024:
                with open(cache_filepath, "wb") as f:
                    f.write(data_to_dump)

            return result

        return wrapper

    return decorator
