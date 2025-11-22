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

### ワークフローの実行方法

ワークフローは以下の3つの方法で実行できます：

#### 1. Pull Requestで自動実行

Pull Requestを作成または更新すると、自動的にMCPサーバーのテストが実行されます。

```bash
git checkout -b test-branch
git add .
git commit -m "Test MCP server"
git push origin test-branch
# GitHubでPull Requestを作成
```

#### 2. PRコメントで実行

Pull Request内で `@claude` とメンションすると、ワークフローがトリガーされます。

```
@claude MCPサーバーをテストしてください
```

#### 3. 手動実行

1. Actions タブに移動
2. "Test MCP Server" ワークフローを選択
3. "Run workflow" ボタンをクリック

### ワークフローの動作

1. リポジトリをチェックアウト
2. Python環境のセットアップ
3. MCP設定ファイル（`.mcp/config.json`）を作成
4. MCPサーバーをバックグラウンドで起動
5. Claude Code Actionを使用してサーバーをテスト
   - 基本的なテキストのエコーテスト
   - 特殊文字を含むテキストのテスト
   - 日本語と絵文字のテスト
6. テスト完了後、サーバーをクリーンアップ

### 技術的な詳細

- MCPサーバーの設定は `--mcp-config` フラグで渡されます
- サーバーは `http://localhost:8000/sse` (SSEトランスポート) で起動します
- 健全性チェックにより、サーバーが起動するまで最大30秒待機します

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