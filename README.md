# claude-mcp-server

FastMCPを使用したシンプルなMCPサーバーのサンプルプロジェクト

## 機能

- **Echo Tool**: 入力されたテキストをそのまま返すシンプルなツール

## ローカルでのテスト

### 1. サーバーの起動

```bash
uv run --with mcp .github/scripts/server.py
```

サーバーは `http://localhost:8000/sse` で起動します。

### 2. Claude Code CLIでの接続

```bash
# MCPサーバーを追加
claude mcp add --transport sse my-server http://localhost:8000/sse

# 接続を確認
claude mcp list

# Claude Code CLIで対話的にテスト
claude
```

Claude Code CLI内で以下のように実行できます：

```
> mcpのmy-serverをテストしてください
```

## GitHub Actionsでのテスト

このリポジトリには、GitHub ActionsでClaude Code Actionを使用してMCPサーバーを自動テストするワークフローが含まれています。

### セットアップ

1. GitHubリポジトリのSettings > Secrets and variables > Actions に移動
2. `ANTHROPIC_API_KEY` という名前でAnthropic APIキーを追加

### ワークフローの実行

ワークフローは以下の場合に自動実行されます：

- `main` ブランチへのpush
- `main` ブランチへのPull Request

手動で実行する場合：

1. Actions タブに移動
2. "Test MCP Server" ワークフローを選択
3. "Run workflow" ボタンをクリック

### ワークフローの動作

1. リポジトリをチェックアウト
2. Python環境のセットアップ
3. MCPサーバーをバックグラウンドで起動
4. Claude Code Actionを使用してサーバーをテスト
   - 基本的なテキストのエコーテスト
   - 特殊文字を含むテキストのテスト
   - 日本語と絵文字のテスト
5. テスト完了後、サーバーをクリーンアップ

## プロジェクト構成

```
.
├── .github/
│   ├── scripts/
│   │   └── server.py          # FastMCP Echo Server
│   └── workflows/
│       └── test-mcp.yml        # GitHub Actions workflow
├── pyproject.toml              # プロジェクト設定
└── .python-version             # Python バージョン指定
```