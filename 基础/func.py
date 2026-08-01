

# def func(a,b):
#     if (a > b):
#         return a-b
    
#     else:
#         return a+b
# a = int(input())
# b = int(input())
# print(func(a,b))


# 推导式
# list
arr = [i for i in range(30) if i % 2 == 0 or i % 3 == 0]
print("列表：\n{}".format(arr))
# 字典
test = ["abc", "hello", "test", "aaaaaaaa"]
l1 = {key:len(key) for key in test if len(key) < 8}
listdemo = {i:i**2 for i in range(10) if i % 2 == 0}
print("字典：\n{}\n{}".format(listdemo,l1))
# 集合

