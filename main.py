import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formatdate
from playwright.sync_api import sync_playwright
import os
from datetime import datetime as dt
from zoneinfo import ZoneInfo
import json

RAKUTEN_SEC_URL = "https://www.rakuten-sec.co.jp/ITS/V_ACT_Login.html"

with open('.env.json', 'r') as f:
    envs = json.load(f)
    GMAIL_ADDRESS = envs["gmail_address"]
    GMAIL_PASSWORD = envs["gmail_password"]
    RAKUTEN_SEC_ID = envs["rakuten_sec_id"]
    RAKUTEN_SEC_PASSWORD = envs["rakuten_sec_password"]
    FROM_ADDRESS = envs["from_address"]
    TO_ADDRESS = envs["to_address"]

with sync_playwright() as pw:
    browser = pw.chromium.launch(
        channel="chrome",
        headless=False,
    )
    context = browser.new_context(viewport={"width": 1920, "height": 1080})

    page = context.new_page()
    page.goto(RAKUTEN_SEC_URL)

    page.locator("#form-login-id").type(RAKUTEN_SEC_ID, delay=100)
    page.locator("#form-login-pass").type(RAKUTEN_SEC_PASSWORD, delay=100)
    page.locator("#login-btn").click()

    page.locator('a[data-ratid="mem_pc_top_purpose_all-possess-lst"]').click()
    page.wait_for_selector("#str-main-inner")

    now = dt.now(ZoneInfo("Asia/Tokyo"))
    FILENAME = os.path.join("results", f"保有資産_{now.year}年{now.month}月{now.day}日.png")

    # page.screenshot(path=FILENAME, full_page=True)
    page.locator("#str-main-inner").screenshot(path=FILENAME)

# メール本文作成
body = f"""
<html>
    <body>
        {now.hour}時{now.minute}分時点の情報です
    </body>
</html>"""

# メールヘッダ作成
msg = MIMEMultipart()
msg["Subject"] = f"{now.month}月{now.day}日 楽天証券 保有商品"
msg["From"] = FROM_ADDRESS
msg["To"] = TO_ADDRESS
msg["Date"] = formatdate()
msg.attach(MIMEText(body, "html"))

# ファイルの添付
with open(FILENAME, "rb") as f:
    mb = MIMEApplication(f.read())

mb.add_header("Content-Disposition", "attachment", filename=FILENAME)
msg.attach(mb)

# SMTPサーバに接続
smtpobj = smtplib.SMTP("smtp.gmail.com", 587)
smtpobj.starttls()
smtpobj.login(GMAIL_ADDRESS, GMAIL_PASSWORD)
smtpobj.send_message(msg)
smtpobj.close()
