# dcm-schememo

[English](README.md)

[![PyPI version](https://badge.fury.io/py/dcm-schememo.svg)](https://badge.fury.io/py/dcm-schememo)
[![Tests](https://github.com/oboenikui/dcm-schememo/actions/workflows/test.yml/badge.svg)](https://github.com/oboenikui/dcm-schememo/actions/workflows/test.yml)

ドコモのスケジュール＆メモアプリからエクスポートしたVCSファイルのうち、メモデータを取得するPythonライブラリです。

## インストール方法

```bash
pip install dcm-schememo
```

## 使い方

### 基本的な使用方法

```python
from dcm_schememo import parse_vcs_file

# VCSファイルを解析
events = parse_vcs_file("path/to/your.vcs")

# イベントの内容を確認
for event in events:
    print(f"タイトル: {event.summary}")
    print(f"説明: {event.description}")
    print(f"タイプ: {event.type}")  # NOTE or TASK
    print(f"最終更新日時: {event.last_modified}")
```

### 利用可能なフィールド

`Note` クラスには以下のフィールドがあります：

- `type`: ノートのタイプ（'NOTE', 'SHOPPING', 'TODO', 'TODOEVENT' など）
- `summary`: タイトル
- `description`: 説明文
- `last_modified`: 最終更新日時（datetime型、タイムゾーン付き）
- `photo`: 画像データ（バイト列）
- `tz`: タイムゾーン（例: "+09:00"）
- `decosuke`: デコレーション絵文字データ（バイト列、通常GIF画像）
- `aalarm`: アラーム時刻（datetime型、タイムゾーン付き）
- `status`: タスクのステータス（例: "NEEDS-ACTION"）
- `due`: タスクの期限（datetime型、タイムゾーン付き）
- `location`: 場所
- `show`: 表示設定（True/False/None）

## 使用例

`examples` ディレクトリには以下のサンプルコードが含まれています：

### Google Keep連携サンプル（google_keep.py）

VCSファイルからメモを読み取り、Google Keepに保存するサンプルです。以下の機能を実装しています：

- Googleアカウントへのログイン処理
- VCSファイルからメモの読み取り
- メモのタイトルと本文をGoogle Keepに保存
- 画像の添付がある場合は一時ファイルとして保存

## ライセンス

MIT License
