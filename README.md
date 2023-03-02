# stock-mail-notification

## 機能

- 楽天証券にログインし, 保有銘柄一覧をメール通知
- 定期実行(systemd-timer)

## 準備

- あらかじめ2段階認証を有効化してアプリパスワードを発行する
- `.env.json`を作成し各種設定値を記載する
- poetryの初期設定
  ```bash
  poetry install
  poetry run playwright install firefox
  ```


## 実行
```bash
poetry run python main.py
```