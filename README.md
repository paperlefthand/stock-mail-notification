# stock-mail-notification

## 機能

楽天証券の保有銘柄一覧をスクショしてメール通知する

## 初期設定

- Googleアカウントで2段階認証を有効化
- Gmailのアプリパスワードを発行する [参考](https://support.google.com/mail/answer/185833?hl=ja)
- `.env.json`を作成し各種設定値を記載する
- poetryの初期設定

  ```bash
  poetry install
  poetry run playwright install chromium
  ```

## 実行

```bash
poetry run python main.py
```
