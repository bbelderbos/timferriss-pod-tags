from functools import wraps, partial


def retry(func=None, *, times=3):
    if func is None:
        return partial(retry, times=times)
    @wraps(func)
    def wrapper(*args, **kwargs):
        attempt = 0
        while attempt < times:
            try:
                 return func(*args, **kwargs)
            except Exception as exc:
                attempt += 1
                print(f"Exception {func}: {exc} (attempt: {attempt})")
        return func(*args, **kwargs)
    return wrapper


