# func-cache

## Usage

```py
from func_cache import cache


@cache(__file__)
def sleep_add(a, b):
    import time

    time.sleep(3)
    return a + b


def main():
    print(sleep_add(1, 2))
    print(sleep_add(1, 2)) # cache hit
    print(sleep_add(2, 3))
    print(sleep_add(2, 3)) # cache hit
    print(sleep_add(1, 2)) # cache hit


if __name__ == "__main__":
    main()
```

```sh
$ python main.py
3
Cache hit: sleep_add((1, 2), ())
3
5
Cache hit: sleep_add((2, 3), ())
5
Cache hit: sleep_add((1, 2), ())
3
```
