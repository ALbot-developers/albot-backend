# 移行状況

このプロジェクトは、ALbot-webからRestfulベースに全機能を再実装し、完全に代替することを目的としています。  
これは移行状況を管理するためのファイルです。

#### ※追記

機械的に抽出したため、以下エンドポイント一覧にはWEBのものも含まれています。  
WEBのものはフロントで実装します。チェックが入っているものはalbot-frontendで実装済みです。

## `ALbot-web`のエンドポイント一覧

- [ ] **[WEB]** GET http://localhost:5000/
- [ ] **[WEB]** GET http://localhost:5000/.well-known/apple-developer-merchantid-domain-association
- [x] POST http://localhost:5000/api/activate-sub
- [x] **[廃止]** GET http://localhost:5000/api/cached-settings
- [x] **[廃止]** POST http://localhost:5000/api/cached-settings/{{guild_id}}
- [x] POST http://localhost:5000/api/change_connect_command
- [x] POST http://localhost:5000/api/create-connection-state
- [x] GET http://localhost:5000/api/dict/read
- [x] POST http://localhost:5000/api/dict/write
- [x] GET http://localhost:5000/api/envs/get
- [x] POST http://localhost:5000/api/envs/release
- [x] POST http://localhost:5000/api/fetch_changed_connect_commands
- [x] POST http://localhost:5000/api/fetch_connect_command
- [x] GET http://localhost:5000/api/get-word-limit
- [x] **[廃止]** GET http://localhost:5000/api/is-guild-registered
- [x] GET http://localhost:5000/api/is-message-link-expand-enabled
- [x] GET http://localhost:5000/api/metrics/get
- [x] POST http://localhost:5000/api/metrics/post
- [x] GET http://localhost:5000/api/metrics/record
- [x] GET http://localhost:5000/api/settings/delete
- [x] GET http://localhost:5000/api/settings/read
- [x] POST http://localhost:5000/api/settings/write
- [x] POST http://localhost:5000/api/trusted_roles
- [x] POST http://localhost:5000/api/update-subscription
- [x] POST http://localhost:5000/api/word_count/count
- [x] GET http://localhost:5000/api/word_count/read
- [x] POST http://localhost:5000/api/word_count/write
- [x] GET http://localhost:5000/cancel_subscription
- [x] **[WEB]** GET http://localhost:5000/checkout
- [ ] **[WEB]** GET http://localhost:5000/documents
- [ ] **[WEB]** POST http://localhost:5000/donate
- [ ] **[WEB]** GET http://localhost:5000/faq
- [ ] **[WEB]** GET http://localhost:5000/how-to-use
- [x] **[WEB]** GET http://localhost:5000/login
- [x] **[WEB]** GET http://localhost:5000/logout
- [x] **[廃止]** GET http://localhost:5000/metrics
- [x] **[WEB]** GET http://localhost:5000/my-page
- [x] **[WEB]** GET http://localhost:5000/my-page/select-guild
- [x] **[WEB]** GET http://localhost:5000/my-page/subscriptions
- [x] **[WEB]** GET http://localhost:5000/my-page/{{guild_id}}/{{page}}
- [ ] **[WEB]** GET http://localhost:5000/pricing
- [ ] **[WEB]** GET http://localhost:5000/privacy
- [ ] **[WEB]** GET http://localhost:5000/report/commands/{{category}}
- [ ] **[WEB]** GET http://localhost:5000/success
- [ ] **[WEB]** GET http://localhost:5000/term-of-sale
- [x] POST http://localhost:5000/webhook/stripe_event
