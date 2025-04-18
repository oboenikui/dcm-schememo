# サンプルコード集

このディレクトリには、dcm-schememoライブラリの使用例が含まれています。

## ファイル構成

- `test_event.vcs` - サンプルVCSファイル（買い物リスト）
- `google_keep.py` - Google Keepへのインポート例
- `pyproject.toml`, `poetry.lock` - Poetry依存関係ファイル

## サンプルVCSファイル（test_event.vcs）

買い物リストのサンプルVCSファイルです。以下の機能をテストできます：

- QUOTED-PRINTABLEエンコードされたテキスト（タイトル、説明文）
- Base64エンコードされた画像データ
- タイムゾーン付きの日時（最終更新日時、期限）
- 買い物メモタイプ（SHOPPING）
- ステータス（NEEDS-ACTION）
- 場所情報
- 表示設定（ON）

## Google Keep連携サンプル（google_keep.py）

VCSファイルのメモをGoogle Keepにインポートするサンプルです。

### 必要な依存関係

```
poetry install
```

### 使い方

```bash
python google_keep.py <vcs_file>
```

#### 引数

- `vcs_file`: インポートするVCSファイルのパス
- `email`: Googleアカウントのメールアドレス
- `app_password`: Googleアカウントのアプリパスワード

アプリパスワードは以下の手順で取得できます：
1. Googleアカウントの[セキュリティ設定](https://myaccount.google.com/security)を開く
2. 2段階認証を有効にする
3. アプリパスワードを生成する

#### 機能

- VCSファイルの解析
- メモのタイトルと本文をGoogle Keepに保存
- 画像の添付（手動での操作が必要）
- エラーハンドリング
- 進捗状況の表示

#### 注意事項

- 画像の添付は gkeepapi の制限により自動化できないため、手動での操作が必要です
- Google Keepの同期には若干の時間がかかる場合があります
- エラーが発生した場合でも、処理を継続して他のメモの保存を試みます

### サンプル実行例

```bash
python google_keep.py test_event.vcs example@gmail.com xxxx-xxxx-xxxx-xxxx
```

実行すると以下のような出力が表示されます：

```
VCSファイルを解析しました
メモ「買い物リスト」を作成しました
画像の添付が必要なメモを作成しました: 買い物リスト
Google Keepの最新メモに手動で画像を添付してください
続けるにはEnterを押してください...
すべてのメモを保存しました
```