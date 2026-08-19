from func import top_word
from func import filter_even
from func import group_by_len
from func import flatten
from func import invert_mapping
from client import fetch_repo

dic = {
    "apple": 5,
    "banana": 10,
    "cherry": 5,
    "date": 20,
    "elderberry": 10
}
nums = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]
lis = [[1,2,3,4],5,6,7,[8,9],[10,11,12,13]]
text = "Hello,I am happy to share with you,and I really love you.You are mine"
# print(top_word(text))
# print(filter_even(nums))
# print(group_by_len(text))
# print(flatten(lis))
# print(invert_mapping(dic))

# 测试htppx
data = fetch_repo("pallets/flask")
# data = fetch_repo("pallets/flask", 0.00001)
# data = fetch_repo("pallets/not-exist-repo")
print(data["stargazers_count"])
print(data.get("description"))