import tempfile
import unittest
from datetime import date
from pathlib import Path
from send_excel_email import build_message, find_latest_excel_files, parse_recipients, send_message

class FakeSMTP:
    instances = []
    def __init__(self, host, port, timeout):
        self.host, self.port, self.login_args, self.message = host, port, None, None
        self.__class__.instances.append(self)
    def __enter__(self): return self
    def __exit__(self, *_args): return False
    def login(self, sender, password): self.login_args = (sender, password)
    def send_message(self, message): self.message = message

class EmailTests(unittest.TestCase):
    def test_selects_latest_date_group(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name in ("old_20260713.xlsx", "a_20260714.xlsx", "b_20260714.XLSX",
                         "skip_20260715.xls", "bad_20261301.xlsx", "~$tmp_20260715.xlsx"):
                (root / name).write_bytes(b"data")
            report_date, files = find_latest_excel_files(root)
            self.assertEqual(report_date, date(2026, 7, 14))
            self.assertEqual([p.name for p in files], ["a_20260714.xlsx", "b_20260714.XLSX"])

    def test_missing_and_empty_directories_fail(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with self.assertRaises(RuntimeError): find_latest_excel_files(root)
            with self.assertRaises(RuntimeError): find_latest_excel_files(root / "missing")

    def test_message_attachments_and_smtp(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            files = [root / "a_20260714.xlsx", root / "b_20260714.xlsx"]
            for path in files: path.write_bytes(path.name.encode())
            recipients = parse_recipients("one@example.com, two@example.com, ")
            message = build_message("sender@gmail.com", recipients, date(2026, 7, 14), files)
            send_message(message, "sender@gmail.com", "abcd efgh ijkl mnop", FakeSMTP)
            smtp = FakeSMTP.instances[-1]
            self.assertEqual((smtp.host, smtp.port), ("smtp.gmail.com", 465))
            self.assertEqual(smtp.login_args, ("sender@gmail.com", "abcdefghijklmnop"))
            self.assertEqual([p.get_filename() for p in message.iter_attachments()], [p.name for p in files])

    def test_empty_recipient_list_fails(self):
        with self.assertRaises(RuntimeError):
            parse_recipients(" , ")

if __name__ == "__main__": unittest.main()
