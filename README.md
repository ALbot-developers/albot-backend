# albot-backend

albot-webからAPI部分を切り分けて、Restfulに再実装します。  
FastAPIを使用します。

### [▶進捗](migration_progress.md)

# Table of Contents

- [Authentication](#Authentication)
  - [認証方法](#認証方法)
  - [ユーザーの認証フロー](#ユーザーの認証フロー)
- [Endpoints (`/api/v2`)](#Endpoints-apiv2)
  - [Shards](#Shards-API-apiv2shards)
    - [Assign API](#Assign-API-apiv2shardsassign)
    - [Release API](#Release-API-apiv2shardsshard_idrelease)
    - [Connection commands API](#Connection-commands-API-apiv2shardsshard_idconnection_commands)
    - [Metrics API](#Metrics-API-POST-apiv2shardsshard_idmetrics)
  - [Users](#Users-API-apiv2users)
    - [List subscriptions](#list-subscriptions-apiv2usersusersubscriptions)
    - [Activate subscription](#Activate-subscription-apiv2usersusersubscriptionssubscription_idactivate)
    - [Cancel subscription](#Cancel-subscription-apiv2usersusersubscriptionssubscription_idcancel)
    - [Renew subscription](#Renew-subscription-apiv2usersusersubscriptionssubscription_idrenew)
    - [List user's guilds](#List-users-guilds-apiv2usersmeguilds)
    - [Get user's guild info](#Get-users-guild-info-apiv2usersmeguildsguild_idinfo)
    - [Checkout](#Checkout-apiv2usersmecheckout-session)
  - [Guilds](#guilds-api-apiv2guildsguild_id)
    - [Create resource](#Create-a-resource-apiv2guildsguild_id)
    - [Delete resource](#Delete-a-resource-apiv2guildsguild_id)
    - [Dict API](#Dict-API-apiv2guildsguild_iddict)
    - [Settings API](#Settings-API-apiv2guildsguild_idsettings)
    - [Character usage API](#Character-usage-API-apiv2guildsguild_idcharacter_usage)
    - [Trusted roles API](#Trusted-roles-API-apiv2guildsguild_idtrusted_roles)
    - [Connection states API](#Connection-states-API-apiv2guildsguild_idconnection_states)
    - [Message link expand preference API](#Message-link-expand-preference-API-apiv2guildsguild_idmessage_link_expand_preference)
    - [Connection command API](#Connection-command-API-apiv2guildsguild_idconnection_command)
  - [Metrics API](#Metrics-API-GET-apiv2metrics)

# Authentication
## 認証方法
* 各シャードからの認証には、Bearerトークンを使用します。
```http
Authorization
Bearer <token>
```
## ユーザーの認証フロー

```mermaid
sequenceDiagram
    actor User as ユーザー
    participant Front as フロントエンド
    participant Back as バックエンド
    participant Discord as Discord

    User->>Front: /login にアクセス
    Front->>Back: 認証URLリクエスト
    Back-->>Front: 認証URL返却
    Front->>Discord: リダイレクト
    User->>Discord: Discordアカウントで認証
    Discord->>Front: /callback にリダイレクト
    Front->>Back: 認証リクエスト
    Note right of Back: 認証情報を<br/>sessionに保存
    Back-->>Front: 認証完了レスポンス
```

# Endpoints (`/api/v2`)
## Shards API `/api/v2/shards/`
### Assign API `/api/v2/shards/assign`
- `GET` : シャードの割当を行い、環境変数を配信します。

### Release API `/api/v2/shards/{shard_id}/release`
- `POST` : シャードの終了時に、割当を解除します。

### Connection commands API `/api/v2/shards/{shard_id}/connection_commands`

- `GET` : シャードに接続するサーバーの接続コマンドを取得します。  
  __Options__
  - changes_only (boolean): 前回fetch以降に更新されたコマンドのみ取得します。epoch秒で指定します。
```json
{
  "commands": {
    "123456789012345678": "t.con",
    "234567890123456789": "召喚"
  }
}
```

### Metrics API (POST) `/api/v2/shards/{shard_id}/metrics`

- `POST` : シャードのメトリクスを更新します。

```json
{
  "guilds": 10000,
  "connected": 100
}
```

## Users API `/api/v2/users/`

* **/me/**  
  ログイン中のユーザーにアクセス。セッションで認証されます。
* **/{user_id}/**  
  任意のユーザーの情報にアクセス。bearerトークンでの認証が必要です。

### List subscriptions `/api/v2/users/{user}/subscriptions`

- `GET`: ユーザーのサブスクリプションを取得します。

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

### Activate subscription `/api/v2/users/{user}/subscriptions/{subscription_id}/activate`

- `POST`: ユーザーのサブスクリプションを有効化します。

```json
{
  "guild_id": 123456789012345678
}
```

### Cancel subscription `/api/v2/users/{user}/subscriptions/{subscription_id}/cancel`

- `POST`: ユーザーのサブスクリプションをキャンセルします。

### Renew subscription `/api/v2/users/{user}/subscriptions/{subscription_id}/renew`

- `POST`: ユーザーのサブスクリプションを更新します。

```json
{
  "new_plan": "monthly1"
}
```

### List user's guilds `/api/v2/users/me/guilds`

- `GET`: ユーザーが所属するサーバーの一覧を取得します。

```json
{
  "guilds": [
    {
      "id": "123456789012345678",
      "name": "サーバー名"
    },
    {
      "id": "234567890123456789",
      "name": "サーバー名"
    }
  ]
}
```

### Get user's guild info `/api/v2/users/me/guilds/{guild_id}/info`

- `GET`: ユーザーが所属するサーバーの情報を取得します。

```json
{
  "info": {
    "id": "123456789012345678",
    "name": "サーバー名",
    "icon": "https://cdn.discordapp.com/icons/123456789012345678/abcdef1234567890.png",
    "owner": "123456789012345678",
    "members": 100,
    "channels": 10
  }
}
```

### Checkout `/api/v2/users/me/checkout-session`

- `GET`: ユーザーのチェックアウトセッションを取得します。  
  **Query params:** plan
```json
{
  "url": "https://example.com/"
}
```

## Guilds API `/api/v2/guilds/{guild_id}/`

### Create a resource `/api/v2/guilds/{guild_id}`

- `POST` : サーバーのリソースを作成します。

### Delete a resource `/api/v2/guilds/{guild_id}`

- `DELETE` : サーバーのリソースを削除します。

### Dict API `/api/v2/guilds/{guild_id}/dict`
- `GET` : 辞書の一覧を取得します。
- `PUT` : 辞書をリクエストデータで置き換えます。
```json
{
  "dict": {
    "key1": "value1",
    "key2": "value2"
  }
}
```

- `DELETE` : 辞書を削除します。
### Settings API `/api/v2/guilds/{guild_id}/settings`
- `GET` : サーバーの読み上げ設定を取得します。

```json
{
  "settings": {
    "guild_id": 731467468341510184,
    "lang": "ja-JP",
    "character_limit": 3000,
    "speech_speed": 1.75,
    "read_name": false,
    "custom_voice": null,
    "translate": false,
    "read_name_on_join": true,
    "read_name_on_leave": true,
    "read_guild": false,
    "read_not_joined_users": true,
    "audio_api": "gtts"
  }
}
```
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
  "role_ids": [
    123456789012345678,
    234567890123456789
  ]
}
```
- `PUT` : サーバーの設定を編集できるロールの一覧を更新します。
```json
{
  "enabled": true,
  "role_ids": [
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

### Subscriptions API `/api/v2/guilds/{guild_id}/subscriptions`

- `GET`: サーバーのサブスクリプションを取得します。

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

## Metrics API (GET) `/api/v2/metrics`
- `GET` : メトリクスを取得します。
```json
{
  "metrics": {
    "guilds": 10000,
    "connected": 100
  }
}
```
