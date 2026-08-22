import logging

from .client import fetch_repo
from .config import Settings
from .func import top_word


def build_report(settings: Settings) -> str:
    data = fetch_repo(settings)
    desc = data.get("description") or "(无描述)"
    top = top_word(desc)
    lines = [
        f"#{settings.repo}报告",
        f"- stars: {data.get('stargazers_count', 0 )}",
        f"- 语言:{data.get('language') or 'unknown'}",
        f"- 描述:{desc}",
        f"- 高频词:{', '.join(f'{w}({c})' for w,c in top)}"
    ]
    return "\n".join(lines)

def main() -> None:
    logging.basicConfig(
        level = logging.INFO,
        format = "[%(levelname)s]-%(asctime)s-%(name)s:%(message)s",
        datefmt = "%Y-%m-%d %H:%M:%S"
    )
    settings = Settings()
    # print(build_report(settings))
    logger = logging.getLogger("test_log")
    logger.info(build_report(settings))

if __name__ == "__main__":
    main()