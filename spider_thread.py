#coding=utf-8

from selenium import webdriver
import sys
import time
import random

url = "https://www.crowdai.org/challenges/ai-generated-music-challenge/dynamic_contents"
chrome_binary = "/Users/dinghanyu/Downloads/chromedriver"

num_votes = 0
max_votes = 10000
defeat_id = "25b1"
vote_id = "-d148"
us_votes = ["-d148", "-6d16", "-9387", "-1067" , "4fa7", "8b39", "b6dd", "9291"]
options = webdriver.ChromeOptions()
# 设置成中文
options.add_argument('Accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8')
options.add_argument('Accept-Language=zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6')
# 添加头部
options.add_argument('User-Agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36')
driver = webdriver.Chrome(chrome_binary, chrome_options=options)
num_pages = 3


def isme(element):
    global us_votes
    ret = False
    for us_vote in us_votes:
        if us_vote in element.text:
            ret = True
    return ret

def _vote():
    global num_votes, vote_id, max_votes, driver, url, num_pages
    handles = driver.window_handles
    print(handles)
    time_out = 0
    while(len(handles) > 0):
        time_out += 1
        try:
            print("time out:%d" % (time_out))
            for handle in handles:
                driver.switch_to_window(handle)
                time.sleep(1)
                elements = driver.find_elements_by_class_name("controlsWrapper_notactive")
                if len(elements) != 2:
                    driver.close()
                    print("page load failed")
                    break
                isme_1 = isme(elements[0])
                isme_2 = isme(elements[1])
                if isme_1 and isme_2:
                    driver.refresh()
                    print("all us music")
                    continue
                if len(elements[0].find_elements_by_css_selector("button")) != 3 or \
                   len(elements[1].find_elements_by_css_selector("button")) != 3:
                    continue
                chosed_element = None
                if defeat_id in elements[0].text:
                    chosed_element = elements[1]
                elif defeat_id in elements[1].text:
                    chosed_element = elements[0]
                else:
                    for element in elements:
                        for us_id in us_votes:
                            if us_id in element.text:
                                chosed_element = element
                    if not chosed_element:
                        driver.refresh()
                        print("no us music")
                        continue
                buttons = chosed_element.find_elements_by_css_selector("button")
                print("the number of buttons", len(buttons))
                play_button = None
                for button in buttons:
                    try:
                        if "Play Song" in button.get_attribute("data-rh"):
                            play_button = button
                    except:
                        pass
                if play_button:
                    play_button.click()
                    vote_button = None
                    wait_vote_time = 0
                    while not vote_button:
                        if wait_vote_time >= 30:
                            driver.refresh()
                            print("vote timeout")
                        buttons = chosed_element.find_elements_by_css_selector("button")
                        for button in buttons:
                            try:
                                if "Vote for this song !" in button.get_attribute("data-rh"):
                                    vote_button = button
                                else:
                                    print("vote button disabled, wait vote sleep 2s")
                                    time.sleep(1)
                                    wait_vote_time += 1
                            except:
                                break
                    vote_button.click()
                    print("vote " + chosed_element.text + " successfully")
                    time.sleep(1)
                    num_votes += 1
                    print("total finish %d votes" % (num_votes))
                    driver.refresh()
                    if num_votes > max_votes:
                        print("finish vote %d votes" % (num_votes))
                        driver.quit()
                        exit(1)
                else:
                    driver.refresh()
                    print("button load failed")
                    continue
            handles = driver.window_handles
            if len(handles) < num_pages:
                new_page = 'window.open("%s")' % (url)
                driver.execute_script(new_page)
            if time_out > 10:
                for handle in handles:
                    driver.switch_to_window(handle)
                    driver.refresh()
                handles = driver.window_handles
                time_out = 0
        except Exception as e:
            print(str(e))
            driver.quit()
            exit(1)

def vote():
    global url, num_pages
    driver.get(url)
    new_page = 'window.open("%s")' % (url)
    for i in range(num_pages - 1):
        driver.execute_script(new_page)
    try:
        _vote()
    finally:
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) != 1:
        print("Usage:" + sys.argv[0])
        exit(1)
    vote()
