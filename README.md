# albot-backend
albot-webからAPI部分を切り分けて、Restfulな設計を基本に再実装します。  
FastAPIを使用します。

## 仕様策定Todo:
- [x] shard API
- [x] dict api
- [x] settings api
- [x] character usage api
- [x] trusted roles api
- [x] connection states api
- [x] metrics api
- [ ] message link expand preference api
- [ ] connection command api
- [ ] subscription api (activate, renew, cancel)
- [ ] is guild subscribed api (should be moved to other endpoints)
- [ ] cached settings api (might replace connection command api)

# Authentication
* 各シャードからの認証には、Bearerトークンを使用します。
```http
Authorization
Bearer <token>
```
* WEBダッシュボードからの認証には、httpOnly Cookieに保存したjwtトークンを使用します。
```http
Cookie
jwt=<token>
```

# Endpoints (/api)
## Shards API
- `GET /api/v2/shards/assign` : シャードの割当を行い、環境変数を配信します。
- `POST /api/v2/shards/release` : シャードの終了時に、割当を解除します。
```json
{
  "shard_id": 0
}
```
## Guilds data API
### Dict API `/api/v2/guilds/{guild_id}/dict`
- `GET` : 辞書の一覧を取得します。
- `POST` : 辞書のエントリーを追加します。
```json
{
  "key1": "value1",
  "key2": "value2"
}
```
- `PUT` : 辞書をリクエストデータで置き換えます。
```json
{
  "key1": "value1",
  "key2": "value2"
}
```
### Settings API `/api/v2/guilds/{guild_id}/settings`
- `GET` : サーバーの読み上げ設定を取得します。
- `DELETE` : サーバーの読み上げ設定を削除します。(初期化)
- `POST` : サーバーの読み上げ設定を編集します。
```json
{ 
  "speech_speed": 1.0,
  "read_name": true
}
```
### Character usage API `/api/v2/guilds/{guild_id}/character_usage`
- `GET` : サーバーの文字数使用状況を取得します。
```json
{
  "wavenet": {
    "monthly_quota": 1000000,        // Wavenet音声の月の使用可能文字数
    "used_characters": 250000,       // Wavenet音声の使用済み文字数
    "remaining_characters": 750000   // Wavenet音声の残り使用可能文字数
  },
  "standard": {
    "monthly_quota": 500000,         // Standard音声の月の使用可能文字数
    "used_characters": 150000,       // Standard音声の使用済み文字数
    "remaining_characters": 350000   // Standard音声の残り使用可能文字数
  }
}
```
- `POST` : サーバーの文字数使用状況を更新します。(increment)
```json
{
  "wavenet": {
    "used_characters": 25000
  },
  "standard": {
    "used_characters": 15000
  }
}
```
- `PUT`: サーバーの文字数使用状況をリクエストデータで上書きします。(replace)
```json
{
  "wavenet": {
    "used_characters": 50000
  },
  "standard": {
    "used_characters": 30000
  }
}
```
### Trusted roles API `/api/v2/guilds/{guild_id}/trusted_roles`
- `GET` : サーバーの設定を編集できるロールの一覧を取得します。
```json
{
  "enabled": true,
  "roles": [
    123456789012345678,
    234567890123456789
  ]
}
```
- `PUT` : サーバーの設定を編集できるロールの一覧を更新します。
```json
{
  "enabled": true,
  "roles": [
    123456789012345678,
    234567890123456789
  ]
}
```
### Connection states API `/api/v2/guilds/{guild_id}/connection_states`
- `POST`: サーバーのConnectionStateを生成して返却します。  
payloadとして、接続コマンドで指定されたオプションを受け取ります。  
BotクライアントのConnectionStateクラスに準拠したオブジェクトを返却します。
```json
{
  "options": {
    "read_guild": false,
    "speech_speed": 1,
    "lang": "jp",
    "read_name": true
  }
}
```
## Metrics API `/api/v2/metrics`
- `GET` : メトリクスを取得します。
```json
{
  "guilds": 100,
  "connected": 10
}
```
- `POST`: 特定シャードのメトリクスを更新します。
```json
{
  "shard_id": 0,
  "metrics": {
    "guilds": 10,
    "connected": 1
  }
}
```
# 変数名の変更案
- `read_name` -> `read_sender_name`