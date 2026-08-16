# def append_item(item):
#     lst = []
#     lst.append(item)
#     return lst


# print(append_item(1))
# print(append_item(2))
# print(append_item(3))
def numbers():
    print("A")
    yield 1
    print("B")
    yield 2
    print("C")
    yield 3

gen = numbers()
print(gen)
for x in gen:
    print(x)

for x in gen:
    print(x)
    