import re

w1 = input()
w2 = input()
if bool(re.match(w1, w2)):
    print(len(w2) * 2)
else:
    print('no matching')