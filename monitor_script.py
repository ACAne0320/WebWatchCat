import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import hashlib
import os
import ssl
import time

URL = 'https://jxjyxy.hunnu.edu.cn/xsxw/xwbk.htm'
hash_file_path = 'hash_file.txt'
TO_EMAIL = os.getenv('RECIPIENT_EMAIL','844670992@qq.com')

# 配置邮件发送
def send_email(subject, body, to_email):
    # 从环境变量中获取邮箱信息
    from_email = os.getenv('EMAIL_USER')
    from_password = os.getenv('EMAIL_PASSWORD')
    

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, from_password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()

# 获取网页内容并计算哈希值
def get_page_hash(url):
    response = requests.get(url)
    page_content = response.text
    return hashlib.md5(page_content.encode('utf-8')).hexdigest()

# 监控网页并检测更新
def monitor_website(url, hash_file_path, to_email):
    # 如果之前没有保存哈希值文件，则初始化
    if not os.path.exists(hash_file_path):
        with open(hash_file_path, 'w') as f:
            f.write(get_page_hash(url))

    # 读取之前的哈希值
    with open(hash_file_path, 'r') as f:
        old_hash = f.read()

    # 获取当前网页的哈希值
    current_hash = get_page_hash(url)

    # 如果哈希值不同，说明网页内容更新了
    if current_hash != old_hash:
        # 发送邮件通知
        send_email(
            subject='亲爱的cjy,网站更新啦~',
            body=f'''网站更新啦！
                     请前往查看：{url}''',
            to_email=to_email
        )
        print('发送成功!')
        # 更新保存的哈希值
        with open(hash_file_path, 'w') as f:
            f.write(current_hash)
    else:
        print('未检测到更新')

# 定时任务
def main():
    monitor_website(URL, hash_file_path, TO_EMAIL)
    

if __name__ == "__main__":
    main()
