import unittest
from pathlib import Path
from dcm_schememo.vcs_parser import parse_vcs_file, Note
from datetime import datetime, timezone, timedelta
from dcm_schememo.vcs_parser import _to_bytes, _to_str, _decode_image, _parse_datetime, _parse_alarm, parse_vcs_file, Note

class TestVcsParser(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_to_bytes_none(self):
        """Noneをバイト列に変換できることを確認"""
        self.assertEqual(_to_bytes(None), b'')

    def test_to_bytes_unsupported(self):
        """未対応の型で例外が発生することを確認"""
        with self.assertRaises(TypeError):
            _to_bytes(123)

    def test_to_str_invalid_utf8(self):
        """不正なUTF-8データが空文字列で返されることを確認"""
        invalid_bytes = b'\xff\xfe\xfd'  # 不正なUTF-8シーケンス
        self.assertEqual(_to_str(invalid_bytes), "")  # 空文字列が返される

    def test_decode_image_error(self):
        """不正なBase64データでNoneが返ることを確認"""
        self.assertIsNone(_decode_image(b'invalid base64 data'))

    def test_parse_datetime_no_tz(self):
        """タイムゾーン指定なしでも日時が解析できることを確認"""
        dt = _parse_datetime('20250419T123456Z')
        self.assertEqual(dt.tzinfo, timezone.utc)

    def test_parse_datetime_invalid(self):
        """不正な日時文字列の処理を確認"""
        # None と空文字列の場合は None を返す
        self.assertIsNone(_parse_datetime(None))
        self.assertIsNone(_parse_datetime(""))

        # 不正なフォーマットの場合は ValueError が発生
        with self.assertRaises(ValueError):
            _parse_datetime("invalid")  # 不正なフォーマット
        with self.assertRaises(ValueError):
            _parse_datetime("2025-04-15")  # 別のフォーマット

    def test_parse_alarm_empty(self):
        """空のアラーム文字列でNoneが返ることを確認"""
        self.assertIsNone(_parse_alarm(''))
        self.assertIsNone(_parse_alarm(';RELATED=END'))

    def test_parse_vcs_file(self):
        test_data = """BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
SUMMARY;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:=E3=83=86=E3=82=B9=E3=83=88=E3=82=A4=E3=83=99=E3=83=B3=E3=83=88
DESCRIPTION;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:=E3=81=93=E3=82=8C=E3=81=AF=E3=83=86=E3=82=B9=E3=83=88=E3=82=A4=E3=83=99=E3=
=83=B3=E3=83=88=E3=81=A7=E3=81=99=E3=80=82=0A=E6=94=B9=E8=A1=8C=E3=83=86=E3=82=B9=E3=83=88=E3=80=82
X-DCM-TYPE:NOTE
X-DCM-PHOTO:iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVQI12NgYAAAAAMAASDVlMcAAAAASUVORK5CYII=
LAST-MODIFIED:20250415T120000Z
TZ:+09:00
X-DCM-DECOSUKE:R0lGODlhAQABAGAAACH5BAEKAP8ALAAAAAABAAEAAAgEAP8FBAA7
AALARM:20250415T090000Z;;;
LOCATION;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:=E6=9D=B1=E4=BA=AC=E9=83=BD=E5=8D=83=E4=BB=A3=E7=94=B0=E5=8C=BA=E5=8D=83=E4=
=BB=A3=E7=94=B0=EF=BC=91=E2=88=92=EF=BC=91
X-DCM-SHOW:ON
STATUS:COMPLETED
DUE:20250415T120000Z
END:VEVENT
END:VCALENDAR"""

        test_file = Path("/tmp/test_event_with_tz.vcs")
        test_file.write_text(test_data)

        events = parse_vcs_file(test_file)

        self.assertEqual(len(events), 1)
        event = events[0]
        self.assertEqual(event.last_modified, datetime(2025, 4, 15, 21, 0, tzinfo=timezone(timedelta(hours=9))))
        self.assertEqual(event.summary, "テストイベント")
        self.assertEqual(event.description, "これはテストイベントです。\n改行テスト。")
        self.assertEqual(event.photo, b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x04\x00\x00\x00\xb5\x1c\x0c\x02\x00\x00\x00\x0bIDAT\x08\xd7c``\x00\x00\x00\x03\x00\x01 \xd5\x94\xc7\x00\x00\x00\x00IEND\xaeB`\x82')
        self.assertEqual(event.tz, "+09:00")
        self.assertEqual(event.decosuke, b'GIF89a\x01\x00\x01\x00`\x00\x00!\xf9\x04\x01\n\x00\xff\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x08\x04\x00\xff\x05\x04\x00;')
        self.assertEqual(event.aalarm, datetime(2025, 4, 15, 18, 0, tzinfo=timezone(timedelta(hours=9))))
        self.assertEqual(event.location, "東京都千代田区千代田１−１")
        self.assertTrue(event.show)
        self.assertEqual(event.type, "NOTE")
        self.assertEqual(event.status, "COMPLETED")
        self.assertEqual(event.due, datetime(2025, 4, 15, 21, 0, tzinfo=timezone(timedelta(hours=9))))

        if test_file.exists():
            test_file.unlink()

    def test_parse_vcs_file_without_optional_fields(self):
        test_data = """BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
SUMMARY;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:=54=65=73=74=20=4E=6F=74=65
DESCRIPTION;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:=54=65=73=74=20=44=65=73=63=72=69=70=74=69=6F=6E
X-DCM-TYPE:NOTE
LAST-MODIFIED:20250415T120000Z
TZ:+09:00
X-DCM-DECOSUKE:
X-DCM-PHOTO:
AALARM:
LOCATION:
X-DCM-SHOW:
STATUS:
DUE:
END:VEVENT
END:VCALENDAR"""

        test_file = Path("/tmp/test_note_without_fields.vcs")
        test_file.write_text(test_data)

        events = parse_vcs_file(test_file)

        self.assertEqual(len(events), 1)
        event = events[0]
        self.assertEqual(event.type, "NOTE")
        self.assertIsNone(event.status)
        self.assertIsNone(event.due)
        self.assertIsNone(event.location)
        self.assertIsNone(event.show)
        self.assertIsNone(event.photo)
        self.assertIsNone(event.decosuke)
        self.assertIsNone(event.aalarm)

        if test_file.exists():
            test_file.unlink()

    def test_parse_vcs_invalid(self):
        """不正なVCSデータで例外が発生することを確認"""
        with self.assertRaises(Exception):
            parse_vcs_file('tests/invalid.vcs')

    def test_note_show_empty(self):
        """X-DCM-SHOWが空の場合にNoneが返ることを確認"""
        test_data = """BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
SUMMARY:Test Note
X-DCM-TYPE:NOTE
LAST-MODIFIED:20250415T120000Z
TZ:+09:00
X-DCM-SHOW:
END:VEVENT
END:VCALENDAR"""

        test_file = Path("/tmp/test_note_show_empty.vcs")
        test_file.write_text(test_data)

        try:
            notes = parse_vcs_file(test_file)
            self.assertEqual(len(notes), 1)
            self.assertIsNone(notes[0].show)
        finally:
            if test_file.exists():
                test_file.unlink()

    def test_event_type_skip(self):
        """EVENTタイプのイベントがスキップされることを確認"""
        test_data = """BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
SUMMARY:Test Event
X-DCM-TYPE:EVENT
LAST-MODIFIED:20250415T120000Z
END:VEVENT
END:VCALENDAR"""

        test_file = Path("/tmp/test_event_skip.vcs")
        test_file.write_text(test_data)

        try:
            events = parse_vcs_file(test_file)
            self.assertEqual(len(events), 0)
        finally:
            if test_file.exists():
                test_file.unlink()

    def test_note_repr(self):
        """Noteクラスの__repr__メソッドを確認"""
        note = Note(
            type="NOTE",
            last_modified=datetime(2025, 4, 15, 21, 0, tzinfo=timezone(timedelta(hours=9))),
            summary="Test Note",
            description="Test Description",
            photo=None,
            tz="+09:00",
            decosuke=None,
            aalarm=None,
            status=None,
            due=None,
            location=None,
            show=None,
            original_vevent=None
        )
        repr_str = repr(note)
        self.assertIn("type=NOTE", repr_str)
        self.assertIn("summary=Test Note", repr_str)
        self.assertIn("description=Test Description", repr_str)

    def test_file_not_found(self):
        """存在しないファイルで例外が発生することを確認"""
        with self.assertRaises(FileNotFoundError):
            parse_vcs_file("/nonexistent/file.vcs")

    def test_notes_sorting(self):
        """ノートが最終更新日時でソートされることを確認"""
        test_data = """BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
SUMMARY:Note 1
X-DCM-TYPE:NOTE
LAST-MODIFIED:20250415T120000Z
END:VEVENT
BEGIN:VEVENT
SUMMARY:Note 2
X-DCM-TYPE:NOTE
LAST-MODIFIED:20250414T120000Z
END:VEVENT
END:VCALENDAR"""

        test_file = Path("/tmp/test_notes_sorting.vcs")
        test_file.write_text(test_data)

        try:
            notes = parse_vcs_file(test_file)
            self.assertEqual(len(notes), 2)
            self.assertEqual(notes[0].summary, "Note 2")  # 古い方が先
            self.assertEqual(notes[1].summary, "Note 1")  # 新しい方が後
        finally:
            if test_file.exists():
                test_file.unlink()

    def test_parse_vcs_invalid_calendar(self):
        """不正なカレンダーデータの処理を確認"""
        test_data = """BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
SUMMARY:Test Note
X-DCM-TYPE:NOTE
INVALID_LINE
END:VCALENDAR"""

        from io import StringIO
        import sys

        test_file = Path("/tmp/test_invalid_calendar.vcs")
        test_file.write_text(test_data)

        # 標準エラー出力をキャプチャ
        stderr = StringIO()
        sys.stderr = stderr

        try:
            with self.assertRaises(Exception):
                parse_vcs_file(test_file)
            
            error_output = stderr.getvalue()
            self.assertIn("Error parsing iCal data:", error_output)
        finally:
            # 標準エラー出力を元に戻す
            sys.stderr = sys.__stderr__
            if test_file.exists():
                test_file.unlink()

    def test_parse_vcs_bytes_type(self):
        """X-DCM-TYPEがbytes型の場合の処理を確認"""
        test_data = """BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
SUMMARY:Test Note
X-DCM-TYPE;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:=4E=4F=54=45
LAST-MODIFIED:20250415T120000Z
TZ:+09:00
END:VEVENT
END:VCALENDAR"""

        test_file = Path("/tmp/test_bytes_type.vcs")
        test_file.write_text(test_data)

        try:
            events = parse_vcs_file(test_file)
            self.assertEqual(len(events), 1)
            self.assertEqual(events[0].type, "NOTE")  # bytesからデコードされたタイプ
        finally:
            if test_file.exists():
                test_file.unlink()

if __name__ == "__main__":
    unittest.main()