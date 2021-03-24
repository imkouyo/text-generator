from nltk.tokenize import sent_tokenize, regexp_tokenize

print(regexp_tokenize(sent_tokenize(input())[int(input())], r"[A-z']+"))
