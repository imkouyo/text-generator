# put your python code here

some_iterable = input().lower().split()
count_dict = dict.fromkeys(some_iterable, 0)

for item in some_iterable:
    count_dict[item] += 1

for item in count_dict.items():
    print(f"{item[0]} {item[1]}")