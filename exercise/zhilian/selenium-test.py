from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import numpy as np
import pylab

from mouse_track_parser import mouseTrackParser

chromepath = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
driver = webdriver.Chrome(chromepath)

# url='https://jobs.zhaopin.com/CC867377750J00136574514.htm'
url = 'https://127.0.0.1:9008'

driver.get(url)
driver.maximize_window()
driver.implicitly_wait(1)

timeData = [0, 7, 23, 32, 39, 43, 56, 63, 71, 80, 88, 96, 103, 111, 119, 128, 136, 147, 151, 159, 167, 171, 180, 187, 196, 203, 211, 219, 227, 235, 243, 251, 263, 271, 279, 287,
            295, 299, 308, 320, 327, 335, 343, 351, 360, 368, 375, 383, 391, 400, 407, 415, 424, 428, 435, 444, 451, 460, 467, 475, 483, 492, 499, 510, 516, 524, 533, 638, 646, 732]
trackData = [0, 1, 3, 4, 5, 8, 8, 10, 11, 13, 16, 17, 20, 23, 27, 30, 32, 34, 36, 38, 40, 41, 44, 47, 49, 52, 54, 57, 59, 63, 66, 69, 72, 76, 78, 82, 88, 93, 99,
             103, 104, 108, 112, 117, 123, 128, 133, 136, 140, 145, 152, 158, 165, 173, 181, 189, 196, 204, 211, 217, 224, 231, 237, 243, 248, 254, 258, 264, 265, 265]


# 构造滑动轨迹
def get_trace(distance):
    '''
    :param distance: (Int)缺口离滑块的距离
    :return: (List)移动轨迹
    '''

    # 创建存放轨迹信息的列表
    trace = []
    # 设置加速的距离
    faster_distance = distance*(4/5)
    # 设置初始位置、初始速度、时间间隔
    start, v0, t = 0, 0, 0.2
    # 当尚未移动到终点时
    while start < distance:
        # 如果处于加速阶段
        if start < faster_distance:
            # 设置加速度为2
            a = 1.5
        # 如果处于减速阶段
        else:
            # 设置加速度为-3
            a = -3
        # 移动的距离公式
        move = v0 * t + 1 / 2 * a * t * t
        # 此刻速度
        v = v0 + a * t
        # 重置初速度
        v0 = v
        # 重置起点
        start += move
        # 将移动的距离加入轨迹列表
        trace.append(round(move))
    # 返回轨迹信息
    return trace


def get_trace(offset, time):
    trackRatio = offset/trackData[-1]
    timeRatio = time*1000/timeData[-1]

    msTime = np.array(timeData)*timeRatio
    msTrack = np.array(trackData)*trackRatio
    xx = np.arange(0, time*1000)*timeRatio
    yy, fits = mouseTrackParser(
        msTime, msTrack).myPolyfit(xx, 3)
    yy = np.round(offset/np.max(yy)*yy)

    # pylab.plot(timeData, trackData, '.')
    # pylab.plot(msTime, msTrack, '-')
    # pylab.plot(xx, yy, '*')
    # pylab.show()

    return xx, yy


def drag_and_drop(driver, ele, offset, time):
    xx, yy = get_trace(offset, time)
    ActionChains(driver).click_and_hold(ele).perform()
    for i in range(0, len(yy), 50):
        print(yy[i])
        ActionChains(driver).move_by_offset(yy[i], 0).perform()
        # ActionChains(driver).drag_and_drop_by_offset(ele, y, 0).perform()
    ActionChains(driver).pause(0.3).release().perform()
    print(yy[-1])


try:
    # 滑块
    slide = driver.find_element_by_css_selector(
        '#nocaptcha .nc_iconfont.btn_slide')
    # 滑块包裹
    nc_scale = driver.find_element_by_css_selector('.nc-container .nc_scale')
except:
    print('无元素')

slide_width = int(slide.value_of_css_property('width')[0:-2])
nc_scale_width = int(nc_scale.value_of_css_property('width')[0:-2])
print(slide_width, nc_scale_width)
drag_and_drop(driver, slide, nc_scale_width-slide_width, 1)
