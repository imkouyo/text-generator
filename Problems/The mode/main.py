from collections import Counter

count_dict = Counter(input().split())
print(count_dict.most_common(1)[0][0])