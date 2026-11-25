import pytest

from pr_portfolio import main, render_portfolio


def test_markdown_escapes_pr_title():
    pull_request = {
        "title": "[SQL] fix *client* <details>\nnext line",
        "number": 304,
        "url": "https://github.com/example/project/pull/304",
        "repository": {"nameWithOwner": "example/project"},
    }

    result = render_portfolio("DataLakeAI", [pull_request])

    assert "[example/project#304](https://github.com/example/project/pull/304)" in result
    assert r"\[SQL\] fix \*client\* &lt;details&gt; next line" in result


def test_empty_results():
    assert "没有找到公开、已合并的 PR。" in render_portfolio("DataLakeAI", [])


@pytest.mark.parametrize("arguments", [
    ["DataLakeAI", "--limit", "0"],
    ["DataLakeAI repo:example/project"],
])
def test_rejects_invalid_arguments(monkeypatch, arguments):
    monkeypatch.setattr("sys.argv", ["pr_portfolio.py", *arguments])

    with pytest.raises(SystemExit) as error:
        main()

    assert error.value.code == 2
