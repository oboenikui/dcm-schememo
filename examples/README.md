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
python google_keep.py
```

`test_event.vcs` に保存されているメモがGoogle Keep上に作成されます。
