import requests
from lxml import etree
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
}
comiclist = [url1,url2,...]

def sendmail(con):
    msg_from = ''  # 发送方邮箱
    passwd = ''     # 授权码
    to = '' # 接受方邮箱
    #设置邮件内容
    msg = MIMEMultipart()
    content = con
    msg.attach(MIMEText(content,'plain','utf-8'))
    #设置邮件主题
    msg['Subject'] = "动漫更新提醒"
    #发送方信息
    msg['From'] = msg_from
    #通过SSL方式发送，服务器地址和端口
    s = smtplib.SMTP_SSL("smtp.qq.com", 465)
    s.login(msg_from, passwd)
    s.sendmail(msg_from,to,msg.as_string())

def getTitle(url,title):
    for i in url:
        url_ = i
        content = requests.get(url_,headers=headers).content 
        html = etree.HTML(content)
        title.append(''.join(html.xpath("/html/head/title/text()")))
    return title

def checklist(title):
    if not os.path.isfile("./updatelist.txt"):
        f = open("./updatelist.txt", "w+")
        f.writelines(t +'\n' for t in title)
        f.close()
    else:
        with open("./updatelist.txt", "r+") as f:
            old_title = f.readlines()
            for i in range(len(title)):
                if (old_title[i].strip('\n') != title[i]):
                    old_title[i] = title[i] + '\n'
                    f.seek(0)
                    f.truncate()
                    f.writelines(old_title)
                    sendmail(title[i]+" 已更新！")


if __name__ == "__main__":
    title = []
    checklist(getTitle(comiclist,title))