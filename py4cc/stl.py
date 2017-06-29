def show(x, pp=True):
    s = 'in Python --- ' + str(type(x)) + ': ' + str(x)
    if pp:
        print(s)
    else:
        return s


def length(x):
    return len(x)


def total(x):
    # grand total for sequence `x` whose elements have meaningful `+` operation.
    return sum(x)


def cumsum(x):
    # `cumsum` for sequence `x` whose elements have meaningful `+` operation.
    print('before `cumsum`,', show(x, False))
    for i in range(1, len(x)):
        x[i] = x[i-1] + x[i]
    print('after `cumsum`,', show(x, False))
    return x


def mapadd(x):
    # Add 1 to each value of a `dict`,
    # then insert a new lement 'total': total.
    print('before `mapadd`,', show(x, False))
    #total = sum(x.values())
    total = 0
    for k in x:
        v = x[k]
        total += v
        x[k] = v + 1
    x['total'] = total
    print('after `mappad`,', show(x, False))
    return x



