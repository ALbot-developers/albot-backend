# albot-backend
albot-webからAPI部分を切り分けて、Restfulな設計を基本に再実装します。  
FastAPIを使用します。

# Table of Contents
- [仕様策定Todo](#仕様策定Todo)
- [実装Todo](#実装Todo)
  - [認証方法](#認証方法)
  - [ユーザーの認証フロー](#ユーザーの認証フロー)
- [Endpoints (`/api/v2`)](#Endpoints-apiv2)
  - [Shards](#Shards-API-apiv2shards)
    - [Assign API](#Assign-API-apiv2shardsassign)
    - [Release API](#Release-API-apiv2shardsshard_idrelease)
    - [Connection commands API](#Connection-commands-API-apiv2shardsshard_idconnection_commands)
  - [User(me) subscriptions](#Userme-Subscription-API-apiv2usersmesubscriptions)
    - [List subscriptions](#GET-apiv2usersmesubscriptions)
    - [Activation API](#Activation-API-apiv2usersmesubscriptionssubscription_idactivate)
    - [Cancel API](#Cancel-API-apiv2usersmesubscriptionssubscription_idcancel)
    - [Renew API](#Renew-API-apiv2usersmesubscriptionssubscription_idrenew)
  - [Guilds data](#Guilds-data-API-apiv2guildsguild_id)
    - [Dict API](#Dict-API-apiv2guildsguild_iddict)
    - [Settings API](#Settings-API-apiv2guildsguild_idsettings)
    - [Character usage API](#Character-usage-API-apiv2guildsguild_idcharacter_usage)
    - [Trusted roles API](#Trusted-roles-API-apiv2guildsguild_idtrusted_roles)
    - [Connection states API](#Connection-states-API-apiv2guildsguild_idconnection_states)
    - [Message link expand preference API](#Message-link-expand-preference-API-apiv2guildsguild_idmessage_link_expand_preference)
    - [Connection command API](#Connection-command-API-apiv2guildsguild_idconnection_command)
  - [Subscriptions](#Subscription-API-server-apiv2subscriptionssubscription_id)
    - [Activation API](#Activation-API-apiv2subscriptionssubscription_idactivate)
    - [Renew API](#Renew-API-apiv2subscriptionssubscription_idrenew)
    - [Cancel API](#Cancel-API-apiv2subscriptionssubscription_idcancel)
  - [Metrics API](#Metrics-API-apiv2metrics)
- [変数名の変更案](#変数名の変更案)

## 仕様策定Todo:
- [x] shard API
- [x] user (subscription) api
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
- [x] user (subscription) api
- [x] dict api
- [x] settings api
- [x] character usage api
- [x] trusted roles api
- [x] connection states api
- [ ] metrics api
- [x] message link expand preference api
- [x] connection command api
- [x] subscription api (activate, renew, cancel)

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

## User(me) Subscription API `/api/v2/users/me/subscriptions`

### GET `/api/v2/users/me/subscriptions`

- ユーザーのサブスクリプションを取得します。

```json
{
  "subscriptions": [
    {
      "sub_id": "sub_abcd1234",
      "guild_id": 123456789012345678,
      "plan": "monthly1",
      "sub_start": "2021-01-01T00:00:00",
      "last_updated": "2021-01-01T00:00:00"
    }
  ]
}
```

## Activation API `/api/v2/users/me/subscriptions/{subscription_id}/activate`

- `POST`: ユーザーのサブスクリプションを有効化します。

```json
{
  "guild_id": 123456789012345678
}
```

### Cancel API `/api/v2/users/me/subscriptions/{subscription_id}/cancel`

- `POST`: ユーザーのサブスクリプションをキャンセルします。

### Renew API `/api/v2/users/me/subscriptions/{subscription_id}/renew`

- `POST`: ユーザーのサブスクリプションを更新します。

```json
{
  "new_plan": "monthly1"
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
    "monthly_quota": 1000000,
    "used_characters": 250000
  },
  "standard": {
    "monthly_quota": 500000,
    "used_characters": 150000
  }
}
```
- `POST` : サーバーの文字数使用状況を更新します。文字数が増えた場合のみUPDATEします。
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

## Subscription API (server) `/api/v2/subscriptions/{subscription_id}/`
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
