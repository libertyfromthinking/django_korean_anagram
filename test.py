a = ['권민수','박민수','권민수','김민수']

def print_some(something):
        for i in range(len(something)):
                print(something[i])
        print('끝')

def remove_duplicates(li):
    my_set = set()
    res = []
    for i in li:
        if i not in my_set:
            res.append(i)
            my_set.add(i)
    return res

print(remove_duplicates(a))


