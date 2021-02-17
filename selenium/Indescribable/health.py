from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import argparse

# 初始化：
parser = argparse.ArgumentParser(
    description='input the executable_path, uer_name and passwd to run!')
parser.add_argument('--executable_path', type=str, required=False, default='./linux_driver/chromedriver',
                    help='Path to browser driver')
parser.add_argument('--user_name', type=str, required=False, default=None,
                    help='User_name is your student number.')
parser.add_argument('--password', type=str, required=False, default=None,
                    help='Password of your Tsinghua account.')

# 调用：
global args
args = parser.parse_args()
executable_path = args.executable_path  # 默认 “--”后面的名字
user_name = args.user_name
password = args.password

chrome_options = Options()
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(
    executable_path=executable_path, chrome_options=chrome_options)
driver.maximize_window()
driver.get('https://thos.tsinghua.edu.cn/fp/view?m=fp#act=fp/formHome')
driver.find_element_by_id("i_user").send_keys(user_name)
driver.find_element_by_id("i_pass").send_keys(password)
login = driver.find_element_by_link_text("登录")
login.click()
print('--Successful login.')
print('---before jumpping---')
print('current url:'+driver.current_url)
driver.switch_to.window(driver.window_handles[-1])
time.sleep(3)
flag = 1
while flag:
    try:
        health = driver.find_element_by_xpath('//*[@title="学生健康及出行情况报告"]')
    except:
        print('So poor network! I will refresh and try again.')
        time.sleep(3)
    else:
        print('Page found.')
        flag = 0
print('---after jumpping---')
print('current url:'+driver.current_url)
health = driver.find_element_by_xpath('//*[@title="学生健康及出行情况报告"]')
health.click()
print('--commit page---')
print('current url:'+driver.current_url)
time.sleep(10)
flag = 1
while flag:
    try:
        commit = driver.find_element_by_xpath('//*[@id="commit"]')
    except:
        print('So poor network! I will refresh and try again.')
        time.sleep(3)
    else:
        print('Page found.')
        flag = 0
time.sleep(5)#贵校网页原因，不然提交不了
commit.click()
print("Successful commit.")
