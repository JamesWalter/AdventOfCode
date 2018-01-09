if __name__ == "__main__":
    a = 0
    b = 0
    c = 0
    d = 0
    e = 0
    f = 0
    g = 0
    h = 0

    mul = 0

    b = 84
    c = b
    if a != 0:
        b = b * 100
        b = b + 100000
        c = b + 17000
    while True:
        f = 1
        d = 2
        while True:
            e = 2
            while True:
                mul += 1
                if d * e == b:
                    f = 0
                e += 1
                if b == e:
                    break
            d += 1
            if b == d:
                break
        if f == 0:
            h += 1
        if b == c:
            print h
            print mul
            exit()
        b += 17