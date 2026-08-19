import httpx
import certifi
from config import settings




def fetch_repo(repo: str = settings.repo, timeout: float | None = None) -> dict:
    url = f"{settings.github_api_base}repos/{repo}"
    # httpx 在发起 HTTPS 请求时，找不到有效的根证书来验证 GitHub 的 SSL 证书。需要安装certifi库
    resp = httpx.get(url,timeout = timeout or settings.timeout,verify = certifi.where())
    resp.raise_for_status()
    return resp.json()

