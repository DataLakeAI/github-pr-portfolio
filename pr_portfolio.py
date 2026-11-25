"""Turn GitHub's public, merged pull requests into a Markdown portfolio."""

import argparse
import html
import json
import re
import subprocess


def render_portfolio(username: str, pull_requests: list[dict]) -> str:
    lines = [f"# {username} 的公开 GitHub PR", ""]
    for pr in pull_requests:
        title = html.escape(" ".join(pr["title"].split()), quote=False)
        title = re.sub(r"([\\`*_\[\]~])", r"\\\1", title)
        repo = pr["repository"]["nameWithOwner"]
        lines.append(f'- [{repo}#{pr["number"]}]({pr["url"]}) · {title}')
    if not pull_requests:
        lines.append("没有找到公开、已合并的 PR。")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="生成公开、已合并的 GitHub PR 清单。")
    parser.add_argument("username", help="GitHub 用户名，例如 DataLakeAI")
    parser.add_argument("--limit", type=int, default=30, help="最多返回几条（默认 30）")
    args = parser.parse_args()

    if not re.fullmatch(r"[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*", args.username) or len(args.username) > 39:
        parser.error("请输入有效的 GitHub 用户名。")
    if not 1 <= args.limit <= 1000:
        parser.error("--limit 必须在 1 到 1000 之间。")

    command = [
        "gh", "search", "prs", "--author", args.username, "--merged",
        "--visibility", "public", "--sort", "updated", "--order", "desc",
        "--limit", str(args.limit), "--json", "title,number,url,repository",
    ]
    try:
        result = subprocess.run(command, capture_output=True, check=True, text=True, timeout=120)
        portfolio = render_portfolio(args.username, json.loads(result.stdout))
    except FileNotFoundError:
        parser.exit(1, "找不到 GitHub CLI。请安装 gh 并运行 gh auth login。\n")
    except subprocess.CalledProcessError as error:
        parser.exit(1, f"GitHub 查询失败。{error.stderr.strip()}\n")
    except subprocess.TimeoutExpired:
        parser.exit(1, "GitHub 查询超时。\n")
    except (ValueError, TypeError, KeyError):
        parser.exit(1, "GitHub 返回了无法识别的数据。\n")

    print(portfolio)


if __name__ == "__main__":
    main()
