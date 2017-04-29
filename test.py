l = [1,2,3,4]

def next1(other):
    return next(other)

def me():
    i=0
    while(True):
        yield(l[i])
        i+=1

it = me()
print(next1(it))
print(next1(it))
print(next1(it))
print(next1(it))

