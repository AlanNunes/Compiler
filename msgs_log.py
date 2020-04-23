def print_title(title, col=80):
    title = "    " + title + "    "
    length = len(title)
    bounds = col - length
    bounds = bounds / 2
    bound_left = int(bounds)
    bound_right = int(bounds) + 1 if not bounds.is_integer() else int(bounds)
    print("="*col)
    print("="*bound_left + title + "="*bound_right)
    print("="*col)
    print("")

def print_welcome(*args, col=80):
    print("#"*col)
    for arg in args:
        print_welcome_body(arg, col)
    print("#"*col)
    print("")

def print_welcome_body(msg, col):
    msg_arg = msg
    msg = "    " + msg + "    "
    if len(msg) > 78:
        print_welcome_body(msg_arg[78:], col)
    msg = msg[:78]
    bounds = col - len(msg)
    bounds = bounds / 2
    bound_left = int(bounds)
    bound_right = int(bounds) + 1 if not bounds.is_integer() else int(bounds)
    print("#"*bound_left + msg + "#"*bound_right)