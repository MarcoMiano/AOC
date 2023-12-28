def test():
    i = []

    def innertest():
        i = [1]

    innertest()
    print(i)


test()
