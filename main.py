from selenium.webdriver.common.by import By #用于指定 HTML 文件中 DOM 标签元素
from selenium.webdriver.support.ui import WebDriverWait #等待网页加载完成
from selenium.webdriver.support import expected_conditions as EC #指定等待网页加载结束条
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import pyautogui
import ddddocr
import time
import os


def login():
    # 打开 url
    driver = webdriver.Chrome()
    driver.get('https://h5.51credit.com/www/login/login.html?service=https%3A%2F%2Fbbs.51credit.com%2F')

    # 点击手机密码输入
    driver.find_element_by_xpath('/html/body/div[3]/div/div[1]/ul/li[2]').click()
    time.sleep(1)

    # 提交账号密码
    driver.find_element_by_xpath('//*[@id="userName"]').send_keys('your')
    driver.find_element_by_xpath('//*[@id="userPwd"]').send_keys('your')

    # 点击登录
    driver.find_element_by_xpath('//*[@id="userLoginBtn"]').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'captchaImgPwdLogin')))

    # 提交验证码
    while True:
        # 先判断之前运行的验证码还在吗，在删除
        if os.path.exists(r'C:\Users\DELL\Downloads\init.jfif'):
            os.remove(r'C:\Users\DELL\Downloads\init.jfif')
        else:
            pass
        # 获得验证码链接
        cap_url = driver.find_element_by_xpath('//*[@id="captchaImgPwdLogin"]').get_attribute('src')
        # 在同一窗口打开验证码链接
        driver.execute_script("window.open();")
        handles = driver.window_handles
        driver.switch_to.window(handles[-1])
        driver.get(cap_url)
        # 右键保存图片
        pic = driver.find_element_by_xpath('/html/body/img')  # 获取元素
        action = ActionChains(driver).move_to_element(pic)  # 移动到该元素
        action.context_click(pic)  # 右键点击该元素
        action.perform()  # 执行
        pyautogui.typewrite(['v'])  # 敲击V进行保存
        # 单击图片另存之后等1s敲回车，再等两秒等待图片下载
        time.sleep(1)
        pyautogui.typewrite(['enter'])
        time.sleep(2)
        # 识别图片，回到登录页提交
        code = OCR()
        driver.close()
        driver.switch_to.window(handles[0])
        driver.find_element_by_xpath('//*[@id="inputJcaptchaPwdLogin"]').send_keys(code)
        # 点击登录
        driver.find_element_by_xpath('//*[@id="userLoginBtn"]').click()
        try: # 识别错误
            WebDriverWait(driver,3).until(EC.presence_of_element_located((By.ID,'tab-社区首页')))
            input('登录成功！！！')
            break
        except:
            continue


def OCR():
    '''
    OCR 识别
    :return:
    '''
    ocr = ddddocr.DdddOcr()
    with open(r'C:\Users\DELL\Downloads\init.jfif', 'rb') as f:
        img_bytes = f.read()
    res = ocr.classification(img_bytes)
    #print(res)
    return res


if __name__ == '__main__':
    login()



