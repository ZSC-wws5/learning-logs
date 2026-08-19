import httpx
import certifi
# g = httpx.get('https://www.baidu.com',timeout = 10.0)
# print(g.text[:500])
# # p = httpx.post('https://www.baidu.com', data={'key': 'value'})
# # print(p)


def fetch_repo(repo:str, timeout:float = 30.0) -> dict:
    url = f"https://api.github.com/repos/{repo}"
    # httpx 在发起 HTTPS 请求时，找不到有效的根证书来验证 GitHub 的 SSL 证书。需要安装certifi库
    resp = httpx.get(url,timeout = timeout,verify = certifi.where())
    resp.raise_for_status()
    return resp.json()

