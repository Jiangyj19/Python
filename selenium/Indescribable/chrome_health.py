from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import argparse

# 参数初始化：
parser = argparse.ArgumentParser(
    description='input the executable_path, uer_name and passwd to run!')
parser.add_argument('--executable_path', type=str, required=False, default='./linux_driver/chromedriver',
                    help='Path to browser driver')
parser.add_argument('--user_name', type=str, required=False, default=None,
                    help='User_name is your student number.')
parser.add_argument('--password', type=str, required=False, default=None,
                    help='Password of your Tsinghua account.')

# 参数调用：
global args
args = parser.parse_args()
executable_path = args.executable_path
user_name = args.user_name
password = args.password

chrome_options = Options()  # 浏览器配置选项
chrome_options.add_argument("--headless")  # 无图形界面参数，注释掉后将开启图形界面
driver = webdriver.Chrome(
    executable_path=executable_path, chrome_options=chrome_options)
driver.maximize_window()
# 在线服务系统登录界面
driver.get('https://thos.tsinghua.edu.cn/fp/view?m=fp#act=fp/formHome')
driver.find_element_by_id("i_user").send_keys(user_name)  # 定位到输入框并输入信息
driver.find_element_by_id("i_pass").send_keys(password)
login = driver.find_element_by_link_text("登录")
login.click()  # 登录
print('--Successful login.')
print('---before jumpping---')
print('current url:'+driver.current_url)
# 登录成功后将自动跳转界面，但此时的url会停留在跳转的界面，所以需要切换句柄至最后一个窗口
driver.switch_to.window(driver.window_handles[-1])
time.sleep(3)  # 等待跳转
flag = 1
while flag:  # 一直刷新避免网络卡顿导致程序中断
    try:
        health = driver.find_element_by_xpath(
            '//*[@title="学生健康及出行情况报告"]')  # 定位到学生健康及出行情况报告栏
    except:
        print('So poor network! I will refresh and try again.')
        time.sleep(3)
    else:
        print('Page found.')
        flag = 0
print('---after jumpping---')
print('current url:'+driver.current_url)
health.click()
print('--commit page---')
print('current url:'+driver.current_url)  # 进入到提交界面
time.sleep(10)
flag = 1
while flag:
    try:
        commit = driver.find_element_by_xpath('//*[@id="commit"]')  # 定位提交按钮
    except:
        print('So poor network! I will refresh and try again.')
        time.sleep(3)
    else:
        print('Page found.')
        flag = 0
time.sleep(5)  # 可能是贵校网页原因，得多等一会儿不然提交不了
commit.click()
print("Successful commit.")
