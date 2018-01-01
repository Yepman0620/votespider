#coding=utf-8

from selenium import webdriver
import sys
import time
import random

url = "https://www.cxrxoxwxdxaxi.org/challenges/ai-generated-music-challenge/dynamic_contents"
chrome_binary = "/Users/Yiwen/Downloads/chromedriver"

num_votes = 0
max_votes = 40
vote_id = "-d148"
us_votes = ["-d148", "-6d16", "-9387", "-1067"]

def isme(element):
    global us_votes
    ret = False
    for us_vote in us_votes:
        if us_vote in element.text:
            ret = True
    return ret

def _vote(page_wait_time):
    global num_votes, vote_id, max_votes
    options = webdriver.ChromeOptions()
    # 设置成中文
    options.add_argument('Accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8')
    options.add_argument('Accept-Language=zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6')
    # 添加头部
    options.add_argument('User-Agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36')
    driver = webdriver.Chrome(chrome_binary, chrome_options=options)

    try:
        driver.get(url)
        if page_wait_time > 0:
            print("page wait sleep %ds" % (page_wait_time))
            time.sleep(int(page_wait_time))
        elements = driver.find_elements_by_class_name("controlsWrapper_notactive")
        if len(elements) != 2:
            raise Exception("page load failed")
        isme_1 = isme(elements[0])
        isme_2 = isme(elements[1])
        if isme_1 and isme_2:
            raise Exception("all us music")
        else:
            chosed_element = None
            for element in elements:
                if vote_id in element.text:
                    chosed_element = element
            if not chosed_element:
                raise Exception("no us music")
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
                        raise Exception("vote timeout")
                    buttons = chosed_element.find_elements_by_css_selector("button")
                    for button in buttons:
                        try:
                            if "Vote for this song !" in button.get_attribute("data-rh"):
                                vote_button = button
                            else:
                                print("vote button disabled, wait vote sleep 2s")
                                time.sleep(2)
                                wait_vote_time += 2
                        except:
                            break
                vote_button.click()
                print("vote " + chosed_element.text + " successfully")
                time.sleep(1)
                num_votes += 1
                print("total finish %d votes" % (num_votes))
                if num_votes > max_votes:
                    print("finish vote 100 votes")
                    driver.quit()
                    exit(1)
            else:
                raise Exception("button load failed")
        driver.quit()
    except Exception as e:
        print(str(e))
    finally:
        driver.quit()
    driver.quit()

def vote(num_iter, iter_wait_time, page_wait_time):
    if num_iter > 0:
        for i in range(num_iter):
            random_wait_time = random.randint(1, iter_wait_time)
            _vote(page_wait_time)
            if iter_wait_time > 0:
                print("iter wait sleep %ds" % (random_wait_time))
                time.sleep(random_wait_time)
    else:
        while True:
            random_wait_time = random.randint(1, iter_wait_time)
            _vote(page_wait_time)
            if iter_wait_time > 0:
                print("iter wait sleep %ds" % (random_wait_time))
                time.sleep(random_wait_time)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage:" + sys.argv[0] + " <num_iter:int> <iter_wait_time:int> <page_wait_time:int>")
        exit(1)
    vote(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
