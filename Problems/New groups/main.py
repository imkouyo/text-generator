# the list with classes; please, do not modify it
groups = ['1A', '1B', '1C', '2A', '2B', '2C', '3A', '3B', '3C']

# your code here
groups_key = groups[:int(input())]
groups_dic = dict.fromkeys(groups)

for key in groups_key:
    groups_dic[key] = int(input())

print(groups_dic)
