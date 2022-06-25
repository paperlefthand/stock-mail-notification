import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formatdate
from selenium import webdriver
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.common.by import By
# from bs4 import BeautifulSoup
import os, sys
from dotenv import load_dotenv
load_dotenv()

CHROMEDRIVER_PATH = ".\chromedriver_v103.exe"

chrome_service = fs.Service(executable_path=CHROMEDRIVER_PATH)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
driver.implicitly_wait(60)

driver.get('https://www.rakuten-sec.co.jp/ITS/V_ACT_Login.html')

# login
try:
    driver.find_element(By.ID, "form-login-id").send_keys(os.getenv('RAKUTEN_SEC_ID'))
    driver.find_element(By.ID, "form-login-pass").send_keys(os.getenv('RAKUTEN_SEC_PASSWORD'))
    driver.find_element(By.ID, "login-btn").click()
except:
    pass

try:
    element = driver.find_element(By.LINK_TEXT, "保有資産を確認する")
    element.click()
except:
    pass

bodyText = ""
rows = driver.find_elements(By.CSS_SELECTOR, '#table_possess_data > span > table > tbody > tr')
for row in rows[1:]:
    tds = row.find_elements(By.TAG_NAME, 'td')
    text = f"{tds[0].text},{tds[1].text},{tds[2].text},{tds[3].text},{tds[4].text},{tds[5].text},{tds[6].text}\n"
    bodyText += text

filename = "result.png"

png = driver.find_element(By.ID, 'str-main-inner').screenshot_as_png
with open(filename, 'wb') as f:
    f.write(png)

driver.close()

body = f"""
<html>
    <body>
        <h1>保有銘柄一覧</h1>
        <p>{bodyText}</p>
    </body>
</html>"""

# メール作成
msg = MIMEMultipart()
msg['Subject'] = '保有商品'
msg['From'] = os.getenv('FROM_ADDRESS')
msg['To'] = os.getenv('TO_ADDRESS')
msg['Date'] = formatdate()
msg.attach(MIMEText(body, "html"))

with open(filename, "rb") as f:
    mb = MIMEApplication(f.read())

mb.add_header("Content-Disposition", "attachment", filename=filename)
msg.attach(mb)

# SMTPサーバに接続
smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
smtpobj.starttls()
smtpobj.login(os.getenv('GMAIL_ADDRESS'), os.getenv('GMAIL_PASSWORD'))
smtpobj.send_message(msg)
smtpobj.close()