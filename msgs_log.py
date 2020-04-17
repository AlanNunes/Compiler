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