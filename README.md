# GitHub PR 作品清单

输入 GitHub 用户名，生成由该账号提交且已经合并的公开 PR Markdown 清单。每条包含标题、仓库、PR 编号和链接，适合复制到个人主页或作品集。

## 使用

需要 Python 3.10+ 和已登录的 GitHub CLI。初次使用 GitHub CLI 时运行 `gh auth login`。

```sh
python3 pr_portfolio.py DataLakeAI
python3 pr_portfolio.py DataLakeAI --limit 10 > portfolio.md
```

工具通过 `gh search prs` 调用 GitHub 搜索 API，按最后更新时间倒序，默认显示 30 条。查询范围为公开仓库。请直接将查询结果中需要展示的 PR 粘贴到作品集中。
