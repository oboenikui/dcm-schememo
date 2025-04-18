import unittest
from pathlib import Path
from dcm_schememo.vcs_parser import parse_vcs_file, Note
from datetime import datetime, timezone, timedelta

class TestVcsParser(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

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

if __name__ == "__main__":
    unittest.main()