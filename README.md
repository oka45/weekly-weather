## 採用技術（技術選定）
- 言語：Python 3.11.6
- 画面（フレームワーク）：Streamlit 1.54.0
- 天気データ取得：Open-Meteo（Weather API）

### AI支援

- Codex（ChatGPT）
- 本プロジェクトは **Python学習目的** のため、AIは以下の用途のみに利用しています
  - Pythonの書き方の確認
  - ライブラリの使い方の調査
  - 自分で書いたコードのレビュー
  - エラー原因の調査

**実装は基本的に自分で行っています。**

## 起動方法
- uv run streamlit run main.py
  - 後で環境構築の項目を作る

## 静的解析
- `uv run ruff check .`
  - 問題を検出する
- `uv run ruff check . --fix`
  - 問題を検出しつつ、自動修正できるものは直す
- `uv run ruff format .`
  - コードの見た目を整える

## ドキュメント

- [仕様書](./docs/specification.md)
