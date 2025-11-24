## 1. デプロイパイプライン概要

このパイプラインは、GitHub リポジトリへの push をトリガーとして、 サーバー上のアプリケーションを自動デプロイし、その結果を GitHub に
- Commit Status（Checks欄の deploy/production）	
- Deployments（右サイドバーの Environments/Deployments）

として反映します。

---

## 2. 全体構成

### コンポーネント
#### GitHub リポジトリ 
- push イベントを Webhook 経由で送信 
- Webhook Secret による HMAC-SHA256 署名 (X-Hub-Signature-256)

#### Nginx（us-1.albot.info）
- https://us-1.albot.info/hooks/... を受けて http://127.0.0.1:9000 にリバースプロキシ
- adnanh/webhook デーモン 
  - ポート9000 で待受
  - hooks.json.tmpl に基づき:
    - HMAC 署名検証（payload-hmac-sha256）
    - リポジトリ ID / フルネーム検証
    - デプロイコマンド + GitHubへの反映スクリプトを実行

#### シークレット・トークン	変数
- WEBHOOK_SECRET：GitHub Webhook と webhook の間の HMAC 用共通鍵	
- GITHUB_TOKEN：GitHub API 呼び出し用トークン（PAT など）	
- 権限：repo:status, repo_deployment（or repo）

---

## 3. セキュリティ
- 改ざん防止：ボディに対する HMAC-SHA256 を X-Hub-Signature-256 で検証。	
- リポジトリ制限：repository.id, repository.full_name で特定リポジトリ以外からの Webhook を拒否。
- 認証情報管理：
  - WEBHOOK_SECRET / GITHUB_TOKEN はファイルに平文で置かれるため、権限を 600 に制限。
  - GitHub 側には WEBHOOK_SECRET 以外のサーバ情報は流出しない。
