def upstairs(n):
    if n > 0:
        print('steps:{0}\tposibilities:{1}'.format(n, step(n)))
    else:
        print('sorry! illegal input!')


def step(n):
    """step by step like the pace of the devil.

    Params:
        n:   total steps.

    Return:
        count of posibilities.
    """
    if n == 2:
        return 2
    elif n == 1:
        return 1
    elif n == 0:
        return 0
    elif n > 2:
        return step(n-1) + step(n-2)


if __name__ == '__main__':
    for i in range(10):
        upstairs(i)
