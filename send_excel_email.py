#!/usr/bin/env python3
"""將檔名日期最新一天的 Excel 檔案透過 Gmail SMTP 寄出。"""
import argparse
import os
import re
import smtplib
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path
from dotenv import load_dotenv

PATTERN = re.compile(r"_(\d{8})\.xlsx$", re.IGNORECASE)
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

def parse_args():
    parser = argparse.ArgumentParser(description="寄出檔名日期最新的所有 Excel")
    parser.add_argument("directory", nargs="?", type=Path, default=Path("."))
    parser.add_argument("--dry-run", action="store_true", help="顯示附件但不寄信")
    return parser.parse_args()

def extract_date(path):
    match = PATTERN.search(path.name)
    if not match:
        return None
    try:
        return datetime.strptime(match.group(1), "%Y%m%d").date()
    except ValueError:
        return None

def find_latest_excel_files(directory):
    if not directory.is_dir():
        raise RuntimeError(f"資料夾不存在：{directory}")
    dated = []
    for path in directory.iterdir():
        if path.is_file() and not path.name.startswith("~$"):
            file_date = extract_date(path)
            if file_date:
                dated.append((file_date, path.resolve()))
    if not dated:
        raise RuntimeError(f"找不到 *_YYYYMMDD.xlsx：{directory.resolve()}")
    latest = max(file_date for file_date, _ in dated)
    return latest, sorted(path for file_date, path in dated if file_date == latest)

def require_env(name):
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f".env 缺少必要設定：{name}")
    return value

def parse_recipients(value):
    recipients = [address.strip() for address in value.split(",") if address.strip()]
    if not recipients:
        raise RuntimeError("EMAIL_RECIPIENTS 至少需要一個收件地址")
    return recipients

def build_message(sender, recipients, report_date, files):
    message = EmailMessage()
    message["From"], message["To"] = sender, ", ".join(recipients)
    message["Subject"] = f"暢銷書排行榜 {report_date:%Y-%m-%d}"
    names = "\n".join(f"- {path.name}" for path in files)
    message.set_content(f"附件為 {report_date:%Y-%m-%d} 的暢銷書排行榜：\n\n{names}\n")
    for path in files:
        message.add_attachment(
            path.read_bytes(), maintype="application",
            subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=path.name,
        )
    return message

def send_message(message, sender, password, smtp_factory=smtplib.SMTP_SSL):
    with smtp_factory(SMTP_HOST, SMTP_PORT, timeout=30) as smtp:
        smtp.login(sender, password.replace(" ", ""))
        smtp.send_message(message)

def main():
    load_dotenv()
    args = parse_args()
    report_date, files = find_latest_excel_files(args.directory)
    print(f"排行榜日期：{report_date:%Y-%m-%d}")
    for path in files:
        print(f"- {path.name}")
    if args.dry_run:
        print("試跑完成，未寄出郵件。")
        return
    sender = require_env("GMAIL_ADDRESS")
    password = require_env("GMAIL_APP_PASSWORD")
    recipients = parse_recipients(require_env("EMAIL_RECIPIENTS"))
    send_message(build_message(sender, recipients, report_date, files), sender, password)
    print(f"已寄送 {len(files)} 個 Excel 附件給 {len(recipients)} 位收件者。")

if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError, smtplib.SMTPException) as error:
        raise SystemExit(f"錯誤：{error}") from error
