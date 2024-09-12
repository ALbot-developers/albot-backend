# albot-backend
albot-webからAPI部分を切り分けて、Restfulな設計を基本に再実装します。  
FastAPIを使用します。

# Table of Contents
- [仕様策定Todo](#仕様策定Todo)
- [実装Todo](#実装Todo)
- [Authentication](#Authentication)
  - [認証方法](#認証方法)
  - [認証エンドポイント `/api/v2/oauth2/url`](#認証エンドポイント-apiv2oauth2url)
- [Endpoints (`/api/v2`)](#Endpoints-apiv2)
  - [Shards `/api/v2/shards/`](#Shards-API-apiv2shards)
    - [Assign API `/api/v2/shards/assign`](#Assign-API-apiv2shardsassign)
    - [Release API `/api/v2/shards/release`](#Release-API-apiv2shardsrelease)
    - [Connection commands API `/api/v2/shards/{shard_id}/connection_commands`](#Connection-commands-API-apiv2shardsshard_idconnection_commands)
  - [Guilds data `/api/v2/guilds/{guild_id}/`](#Guilds-data-API-apiv2guildsguild_id)
    - [Dict API `/api/v2/guilds/{guild_id}/dict`](#Dict-API-apiv2guildsguild_iddict)
    - [Settings API `/api/v2/guilds/{guild_id}/settings`](#Settings-API-apiv2guildsguild_idsettings)
    - [Character usage API `/api/v2/guilds/{guild_id}/character_usage`](#Character-usage-API-apiv2guildsguild_idcharacter_usage)
    - [Trusted roles API `/api/v2/guilds/{guild_id}/trusted_roles`](#Trusted-roles-API-apiv2guildsguild_idtrusted_roles)
    - [Connection states API `/api/v2/guilds/{guild_id}/connection_states`](#Connection-states-API-apiv2guildsguild_idconnection_states)
    - [Message link expand preference API `/api/v2/guilds/{guild_id}/message_link_expand_preference`](#Message-link-expand-preference-API-apiv2guildsguild_idmessage_link_expand_preference)
    - [Connection command API `/api/v2/guilds/{guild_id}/connection_command`](#Connection-command-API-apiv2guildsguild_idconnection_command)
  - [Subscriptions `/api/v2/subscriptions/{subscription_id}/`](#Subscription-API-apiv2subscriptionssubscription_id)
    - [Activation API `/api/v2/subscriptions/{subscription_id}/activate`](#Activation-API-apiv2subscriptionssubscription_idactivate)
    - [Renew API `/api/v2/subscriptions/{subscription_id}/renew`](#Renew-API-apiv2subscriptionssubscription_idrenew)
    - [Cancel API `/api/v2/subscriptions/{subscription_id}/cancel`](#Cancel-API-apiv2subscriptionssubscription_idcancel)
  - [Metrics API `/api/v2/metrics`](#Metrics-API-apiv2metrics)
- [変数名の変更案](#変数名の変更案)

## 仕様策定Todo:
- [x] shard API
- [x] dict api
- [x] settings api
- [x] character usage api
- [x] trusted roles api
- [x] connection states api
- [x] metrics api
- [x] message link expand preference api
- [x] connection command api
- [x] subscription api (activate, renew, cancel)
- [ ] is guild subscribed api (should be moved to other endpoints)
- [ ] cached settings api (might replace connection command api)


## 実装Todo:
- [x] shard API
- [x] dict api
- [x] settings api
- [ ] character usage api
- [ ] trusted roles api
- [ ] connection states api
- [ ] metrics api
- [ ] message link expand preference api
- [ ] connection command api
- [ ] subscription api (activate, renew, cancel)

# Authentication
## 認証方法
* 各シャードからの認証には、Bearerトークンを使用します。
```http
Authorization
Bearer <token>
```
* WEBダッシュボードからの認証には、Cookieを使用したFastAPIのSessionを使用します。
## ユーザーの認証フロー
1. ユーザーが`/oauth2/login` にアクセスします。
2. サーバーがsessionにstateを保存して、Discord OAuth2の認証URLにリダイレクトします。
3. ユーザーがDiscordアカウントで認証します。
4. Discordがcallback URL`/oauth2/callback`にリダイレクトします。
5. サーバーがstateを検証し、アクセストークンを取得、sessionに保存します。

# Endpoints (`/api/v2`)
## Shards API `/api/v2/shards/`
### Assign API `/api/v2/shards/assign`
- `GET` : シャードの割当を行い、環境変数を配信します。

### Release API `/api/v2/shards/{shard_id}/release`
- `POST` : シャードの終了時に、割当を解除します。
```json
{
  "shard_id": 0
}
```

### Connection commands API `/api/v2/shards/{shard_id}/connection_commands`
- `GET` : シャードに接続するサーバーの接続コマンドを取得します。
```json
{
  "commands": {
    "123456789012345678": "t.con",
    "234567890123456789": "召喚"
  }
}
```

## Guilds data API `/api/v2/guilds/{guild_id}/`
### Dict API `/api/v2/guilds/{guild_id}/dict`
- `GET` : 辞書の一覧を取得します。
- `PUT` : 辞書をリクエストデータで置き換えます。
```json
{
  "key1": "value1",
  "key2": "value2"
}
```

- `DELETE` : 辞書を削除します。
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
### Message link expand preference API `/api/v2/guilds/{guild_id}/message_link_expand_preference`
- `GET`: サーバーのメッセージリンク展開設定を取得します。
```json
{
  "enabled": true
}
```
- `PUT`: サーバーのメッセージリンク展開設定を更新します。
```json
{
  "enabled": true
}
```
### Connection command API `/api/v2/guilds/{guild_id}/connection_command`
- `GET`: サーバーの接続コマンドを取得します。
```json
{
  "command": "召喚"
}
```
- `POST`: サーバーの接続コマンドを更新します。
```json
{
  "command": "召喚"
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
## Subscription API `/api/v2/subscriptions/{subscription_id}/`
### Activation API `/api/v2/subscriptions/{subscription_id}/activate`
- `POST`: サブスクリプションを有効化します。
```json
{
  "guild_id": "123456789012345678"
}
```
### Renew API `/api/v2/subscriptions/{subscription_id}/renew`
- `POST`: サブスクリプションを更新します。
```json
{
  "new_subscription_plan": "monthly1"
}
```
### Cancel API `/api/v2/subscriptions/{subscription_id}/cancel`
- `POST`: サブスクリプションをキャンセルします。

# 変数名の変更案
- `read_name` -> `read_sender_name`
