DEBUG = False


def debug_log(*args, **kwargs):
    pass


if DEBUG:
    def debug_log(*args, **kwargs):
        print(*args, **kwargs)
