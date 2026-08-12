"""
===========================================================================
 04 — 文件读写 —— 入门基础版
===========================================================================
文件读写 = 让你的程序能"记住"东西。

你写代码时数据存在变量里，程序一关就没了。
用文件可以把数据长久保存下来。
===========================================================================
"""

import json  # 处理 JSON 格式（后面会用到）
from pathlib import Path  # 操作文件路径的现代方式

# ═══════════════════════════════════════════════════════════════════════════
# 第一部分：写文件
# ═══════════════════════════════════════════════════════════════════════════

# ─── 1. 写入文本文件 ───
# with open(...) as f: 是固定写法，记住就行
# "w" = write（写入模式），会覆盖已有内容

def demo_write():
    """
    写入文本文件。

    with open(...) as f:
        f.write(...)

    这个结构的意思是：
    1. 打开文件（open），得到一个文件对象 f
    2. 用 f 读写
    3. 退出 with 后自动关闭文件（不用自己关）
    """
    print("--- 写入文件 ---")

    # open() 的参数：
    #   第一个参数：文件名（不存在会自动创建）
    #   第二个参数："w" = 写入（覆盖）
    #   encoding 指定编码，用 "utf-8" 支持中文
    with open("my_note.txt", "w", encoding="utf-8") as f:
        f.write("这是我的第一条笔记。\n")  # \n 是换行
        f.write("这是第二条笔记。\n")
        f.write("文件读写很简单！\n")

    print("my_note.txt 已创建，内容已写入")

    # 验证：读取看看
    with open("my_note.txt", "r", encoding="utf-8") as f:
        content = f.read()
    print(f"文件内容：\n{content}")


# ─── 2. 追加写入（不覆盖） ───
# "a" = append（追加模式），在文件末尾添加

def demo_append():
    """
    追加写入：在已有文件后面加内容，不删原有内容。
    """
    print("--- 追加写入 ---")

    with open("my_note.txt", "a", encoding="utf-8") as f:
        f.write("这是追加的内容。\n")

    # 查看结果
    with open("my_note.txt", "r", encoding="utf-8") as f:
        print(f.read())


# ═══════════════════════════════════════════════════════════════════════════
# 第二部分：读文件
# ═══════════════════════════════════════════════════════════════════════════

# ─── 3. 读取整个文件 ───

def demo_read():
    """
    读取文本文件的几种方式。

    "r" = read（读取模式），默认值，不写也行。
    """
    print("--- 读取文件 ---")

    # 方式一：read() 一次性读取全部内容
    with open("my_note.txt", "r", encoding="utf-8") as f:
        content = f.read()  # 整个文件作为一个字符串
    print(f"方式一（read）：\n{content}")

    # 方式二：readlines() 按行读取，返回列表
    with open("my_note.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()  # 每一行是列表中的一个元素
    print(f"方式二（readlines）：共 {len(lines)} 行")
    for i, line in enumerate(lines, 1):
        print(f"  第 {i} 行：{line}", end="")

    # 方式三：直接遍历文件对象（推荐，大文件不占内存）
    print("\n方式三（逐行遍历）：")
    with open("my_note.txt", "r", encoding="utf-8") as f:
        for line in f:  # 每次只读一行到内存
            print(f"  -> {line}", end="")


# ═══════════════════════════════════════════════════════════════════════════
# 第三部分：JSON 文件（最常用的数据格式）
# ═══════════════════════════════════════════════════════════════════════════

# JSON = 一种通用的数据交换格式
# Python 的字典/列表和 JSON 几乎一模一样
# 所以存数据到文件，用 JSON 最方便

# Python 字典  ->  json.dump()  ->  文件里的 JSON 字符串
# 文件里的 JSON  ->  json.load()  ->  Python 字典

def demo_json():
    """
    JSON 文件读写：保存 Python 数据到文件。
    """
    print("\n--- JSON 文件读写 ---")

    # 一个 Python 字典（以后你会把 AI 返回的结果存下来）
    data = {
        "name": "小明",
        "age": 18,
        "hobbies": ["编程", "阅读", "篮球"],
        "scores": {"math": 95, "english": 88},
    }

    # ── 写入 JSON ──
    # json.dump(数据, 文件对象)
    # ensure_ascii=False 让中文正常显示
    # indent=2 让 JSON 格式化好看
    with open("my_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("my_data.json 已保存")

    # ── 读取 JSON ──
    # json.load(文件对象) 直接返回 Python 字典
    with open("my_data.json", "r", encoding="utf-8") as f:
        loaded = json.load(f)

    print(f"读取成功：{loaded['name']} 的爱好是 {loaded['hobbies']}")

    # ── 查看文件内容 ──
    with open("my_data.json", "r", encoding="utf-8") as f:
        print("文件内容：")
        print(f.read())


# ═══════════════════════════════════════════════════════════════════════════
# 第四部分：检查文件是否存在
# ═══════════════════════════════════════════════════════════════════════════

def demo_check_file():
    """
    操作文件前先检查它是否存在，避免 FileNotFoundError。
    用 pathlib 的 Path 来做。
    """
    print("\n--- 检查文件 ---")

    file_path = Path("my_note.txt")

    # exists() 返回 True/False
    if file_path.exists():
        print(f"文件存在，大小：{file_path.stat().st_size} 字节")
        print(f"文件名：{file_path.name}")
        print(f"后缀：{file_path.suffix}")
    else:
        print("文件不存在")

    # 检查不存在的文件
    fake_path = Path("不存在的文件.txt")
    if not fake_path.exists():
        print(f"'{fake_path.name}' 不存在，这是正常的")


# ═══════════════════════════════════════════════════════════════════════════
# 第五部分：给入门者的总结
# ═══════════════════════════════════════════════════════════════════════════

"""
文件读写你必须记住的 3 个模式：

"w" = write 写入（覆盖已有内容）
"a" = append 追加（在末尾加，不删已有的）
"r" = read 读取（默认，不写也行）

标准模板：

  # 写入
  with open("文件名", "w", encoding="utf-8") as f:
      f.write("内容")

  # 追加
  with open("文件名", "a", encoding="utf-8") as f:
      f.write("追加内容")

  # 读取
  with open("文件名", "r", encoding="utf-8") as f:
      content = f.read()

  # JSON 写入
  with open("文件名.json", "w", encoding="utf-8") as f:
      json.dump(字典, f, ensure_ascii=False, indent=2)

  # JSON 读取
  with open("文件名.json", "r", encoding="utf-8") as f:
      字典 = json.load(f)

记住：with 会自动关文件，别再手动写 f.close() 了。
"""


# ═══════════════════════════════════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 50)
    print("04 — 文件读写 入门基础")
    print("=" * 50)

    demo_write()
    demo_append()
    demo_read()
    demo_json()
    demo_check_file()

    # 清理演示文件
    import os
    for f in ["my_note.txt", "my_data.json"]:
        if os.path.exists(f):
            os.remove(f)
    print("\n===== 文件读写 基础演示结束 =====")
