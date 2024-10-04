# func-cache

`func-cache` is a Python decorator that caches function results. The cache is stored on the local disk as a `.pkl` file.

## Installation

```sh
pip install git+https://github.com/kaiiy/func-cache
```

## Usage

```py
from func_cache import cache


@cache(caller_name=None, max_m_bytes=10, verbose=True)
def heavy_computation(x, y):
    # Expensive computation
    return x * y


first_result = heavy_computation(1, 2) # First call, the computation is executed and cached.
second_result = heavy_computation(1, 2) # Second call, the result is retrieved from the cache.
```

Since the cache is stored as a file, subsequent calls to the function will be faster across multiple runs of the program.

## Decorator Argument 

- `caller_name` (option) : The name of the caller's filename. If `None`, the name of the caller's file is retrieved using the Python inspect module. If you're using this in a Jupyter Notebook, it is recommended to set this argument to the name of the notebook file.
- `max_m_bytes` (option): The maximum size of the cache file in MB. If the cache file exceeds this size, the cache is not saved.
- `verbose` (option) : If `True`, prints messages to the console.

## LICENSE

MIT

