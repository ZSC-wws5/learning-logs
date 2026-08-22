import logging
import time

import certifi
import httpx

from .config import Settings

logger = logging.getLogger("HTTP Request")

# def fetch_repo(settings:Settings) -> dict:
#     url = f"{settings.github_api_base}repos/{settings.repo}"
#     # httpx 在发起 HTTPS 请求时，找不到有效的根证书来验证 GitHub 的 SSL 证书。需要安装certifi库
#     resp = httpx.get(url,timeout = settings.timeout,verify = certifi.where())
#     resp.raise_for_status()
#     return resp.json()

def fetch_repo(settings:Settings, repo: str | None = None,max_retries: int = 3) -> dict:
    repo = settings.repo or repo
    url = f"{settings.github_api_base}repos/{repo}"
    headers = {"User-Agent": "ZSC_wws"}
    for attempt in range(1,max_retries + 1):
        try:
            resp = httpx.get(url,headers=headers,timeout=settings.timeout,verify=certifi.where())
            resp.raise_for_status()
            return resp.json()
        except(httpx.HTTPStatusError,httpx.TimeoutException) as e:
            logger.warning(f"请求失败(第{attempt}次):{e}")
            if attempt == max_retries:
                raise # 重试次数达到后就向上抛出异常
            time.sleep(2 ** (attempt - 1)) # 指数退避 2**0s,2**1s,2**2s
    raise RuntimeError("unreachable")# 防御兜底