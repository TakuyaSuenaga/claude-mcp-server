# claude-mcp-server

FastMCPを使用したシンプルなMCPサーバーのサンプルプロジェクト

## 機能

- **Echo Tool**: 入力されたテキストをそのまま返すシンプルなツール
- **S3 List Buckets Tool**: AWS S3のバケットリストを取得するツール（boto3を使用）

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

#### 1. GitHub Secretsの設定

GitHubリポジトリのSettings > Secrets and variables > Actions に移動し、以下のシークレットを追加：

- `ANTHROPIC_API_KEY`: Anthropic APIキー
- `AWS_ROLE_ARN`: GitHub Actions OIDC用のAWS IAMロールARN（例: `arn:aws:iam::123456789012:role/GitHubActionsRole`）

#### 2. AWS OIDC設定

AWS側でGitHub ActionsからのOIDC認証を設定する必要があります：

1. **IAMアイデンティティプロバイダーを作成**:
   - プロバイダータイプ: OpenID Connect
   - プロバイダーURL: `https://token.actions.githubusercontent.com`
   - オーディエンス: `sts.amazonaws.com`

2. **IAMロールを作成**:
   - 信頼されたエンティティタイプ: ウェブアイデンティティ
   - アイデンティティプロバイダー: 上記で作成したGitHub Actions用プロバイダー
   - オーディエンス: `sts.amazonaws.com`
   - 信頼ポリシーの例:
     ```json
     {
       "Version": "2012-10-17",
       "Statement": [
         {
           "Effect": "Allow",
           "Principal": {
             "Federated": "arn:aws:iam::123456789012:oidc-provider/token.actions.githubusercontent.com"
           },
           "Action": "sts:AssumeRoleWithWebIdentity",
           "Condition": {
             "StringEquals": {
               "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
             },
             "StringLike": {
               "token.actions.githubusercontent.com:sub": "repo:YOUR_GITHUB_USERNAME/claude-mcp-server:*"
             }
           }
         }
       ]
     }
     ```

3. **必要な権限をアタッチ**:
   - S3バケットリスト取得のため、最低限 `s3:ListAllMyBuckets` 権限が必要
   - ポリシー例:
     ```json
     {
       "Version": "2012-10-17",
       "Statement": [
         {
           "Effect": "Allow",
           "Action": "s3:ListAllMyBuckets",
           "Resource": "*"
         }
       ]
     }
     ```

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
2. **AWS OIDC認証を実行** - GitHub ActionsがAWS IAMロールを引き受け
3. Python環境のセットアップ
4. MCP設定ファイル（`.mcp/config.json`）を作成
5. MCPサーバーをバックグラウンドで起動（AWS認証情報を継承）
6. Claude Code Actionを使用してサーバーをテスト
   - 基本的なテキストのエコーテスト
   - 特殊文字を含むテキストのテスト
   - 日本語と絵文字のテスト
   - **AWS S3バケットリストの取得テスト**
7. テスト完了後、サーバーをクリーンアップ

### 技術的な詳細

- MCPサーバーの設定は `--mcp-config` フラグで渡されます
- サーバーは `http://localhost:8000/sse` (SSEトランスポート) で起動します
- 健全性チェックにより、サーバーが起動するまで最大30秒待機します
- AWS認証情報は環境変数として自動的にMCPサーバープロセスに渡されます
- boto3は環境変数（`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`）から自動的に認証情報を取得します

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