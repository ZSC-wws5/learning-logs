from collections import defaultdict
from collections import Counter
import re

# 1. 统计单词词频，取前 n 名
def top_word(text : str, n: int = 3) -> list[tuple[str, int]]:
    # 用正则匹配所有“单词”（字母数字+下划线，或字母+可选撇号），忽略标点
    a = re.findall(r"[a-z]+(?:'[a-z])?", text.lower())#findall()直接提取单词,避免字符转和多余分割
    # 利用Counter计数单词
    words = Counter(a)
    # 返回排名前n个单词的元组(单词，个数)
    return words.most_common(n)

# 2. 过滤出偶数（或所有满足条件的元素）—— 纯列表推导式，最简单的一发
def filter_even(nums: list[int]) -> list[int]:
    ans = []
    for i in nums:
        if not i % 2:
            ans.append(i)
    return ans

# 3. 按单词长度分组 —— dict + list 组合，key 是长度，value 是单词列表
def group_by_len(text: str) -> dict[int, list[str]]:
    s = re.findall(r"[a-z]+(?:'[a-z]+)?",text.lower())
    words = list(dict.fromkeys(s))# 单词去重
    groups = defaultdict(list)# 访问一个不存在的键时，defaultdict会自动创建空列表,而普通的dict
    """
    或者用:
    groups = {}
    for i in words:
        if len(i) not in groups: 
            # 确保键值存在,给当前位置创建一个空列表,不能用[].append(i),因为这个方法的返回值不是列表,而是None
            groups[len(i)] = []
        groups[len(i)].append(i)
    """
    for i in words:
        groups[len(i)].append(i)
    return dict(groups)

# 4. 扁平化嵌套列表 —— 两层列表推导式
def flatten(lis : list[list[int]]) -> list[int]:
    ans = []
    for i in lis:
        if isinstance(i,(list,tuple)):
            ans.extend(i)
        else:
            ans.append(i)
    return ans

# 5. 反转映射（dict 的 key/value 对调，value 可能重复，所以 value 是 list）
def invert_mapping(d:dict[str,int]) -> dict[int,list[str]]:
    ans = defaultdict(list)
    for s in d:
        ans[d[s]].append(s)
    return dict(ans)