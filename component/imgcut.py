'''
@author: zhushen
@contact: 810909753@q.com
@time: 2018/1/22 10:07
'''
import cv2
import win32gui
import win32ui
import win32con
import win32api
import numpy as np
import time

import wx
from wx.lib.pubsub import pub

from component.staticmethod import OnClick_Shuaxin, OnClick_confirm, Smart_chujia, calculate_usetime
from component.variable import set_val, get_val
import logging
from component.read_pic import readpic, grab_screen

logger = logging.getLogger()


def cut_pic(size, name):
    imgpos_yanzhengma = get_val('imgpos_yanzhengma')
    imgpos_question = get_val('imgpos_question')
    imgpos_yanzhengma = np.asarray(imgpos_yanzhengma)
    imgpos_question = np.asarray(imgpos_question)
    ##对空白裁剪
    # shape  (110, 210, 3)
    #(70, 210, 3)
    #(24, 251, 3)
    # (54, 180, 3)
    # (24, 253, 3)
    # (430, 220)

    i1 = imgpos_yanzhengma[:, :]
    i2 = imgpos_question[:, :]
    # i2 = cv2.resize(i2, (180, 62))

    # i1 = cv2.resize(i1, (360, 108), interpolation=cv2.INTER_LANCZOS4)
    # i2 = cv2.resize(i2, (360, 34), interpolation=cv2.INTER_LANCZOS4)

    # set_val('Pos_yanzhengma_relative', (-247, - 12, - 67, + 43))  # 验证码所在位置
    # set_val('Pos_question_relative', (-280, - 65, - 23, -41))  ##问题所在位置

    #(55, 180, 3)
# (24, 257, 3)

    i1 = cv2.resize(i1, (430, 131), interpolation=cv2.INTER_AREA)
    i2 = cv2.resize(i2, (430, 40), interpolation=cv2.INTER_AREA)


    im = np.concatenate([i2, i1])
    # im = cv2.resize(im, tuple(size))0
    cv2.imwrite(name, im)


# def new_screenshot(area):  # x,y  pos       w,h size
#     x, y = area[0], area[1]
#     w, h = area[2], area[3]
#     hwnd = win32gui.Fin`dWindow(None, "win32")
#     wDC = win32gui.GetWindowDC(hwnd)
#     dcObj = win32ui.CreateDCFromHandle(wDC)
#     cDC = dcObj.CreateCompatibleDC()
#     dataBitMap = win32ui.CreateBitmap()
#     dataBitMap.CreateCompatibleBitmap(dcObj, x, y)
#     cDC.SelectObject(dataBitMap)
#     cDC.BitBlt((0, 0), (x, y), dcObj, (0, 0), win32con.SRCCOPY)
#     im = dataBitMap.GetBitmapBits(True)  # Tried False also
#     bmpinfo = dataBitMap.GetInfo()
#     img = np.frombuffer(im, dtype='uint8')
#     img.shape = (bmpinfo['bmWidth'], bmpinfo['bmHeight'], 4)
#     dcObj.DeleteDC()
#     cDC.DeleteDC()
#     win32gui.ReleaseDC(hwnd, wDC)
#     win32gui.DeleteObject(dataBitMap.GetHandle())
#     img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
#     return img


# def new_screenshot_getimg(area, size, name):
#     x, y = area[0], area[1]
#     w, h = area[2], area[3]
#     hwnd = win32gui.FindWindow(None, "win32")
#     wDC = win32gui.GetWindowDC(hwnd)
#     dcObj = win32ui.CreateDCFromHandle(wDC)
#     cDC = dcObj.CreateCompatibleDC()
#     dataBitMap = win32ui.CreateBitmap()
#     dataBitMap.CreateCompatibleBitmap(dcObj, w - x, h - y)
#     cDC.SelectObject(dataBitMap)
#     cDC.BitBlt((-x, -y), (w, h), dcObj, (0, 0), win32con.SRCCOPY)
#     im = dataBitMap.GetBitmapBits(True)  # Tried False also
#     bmpinfo = dataBitMap.GetInfo()
#     img = Image.frombuffer(
#         'RGB',
#         (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
#         im, 'raw', 'RGBX', 0, 1)
#     img = np.array(img)
#     cut_pic(img, size, name)
#     dcObj.DeleteDC()
#     cDC.DeleteDC()
#     win32gui.ReleaseDC(hwnd, wDC)
#     win32gui.DeleteObject(dataBitMap.GetHandle())




def timeset( imgpos_currenttime):
    try:
        currenttime = cv2.cvtColor(imgpos_currenttime, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('time.png', currenttime)
        currenttime = readpic(currenttime)  # 识别出来的时间
        # print(currenttime)
        a_time = get_val('a_time')
        tem1 = time.time()
        a = time.strftime('%Y-%m-%d', time.localtime(tem1))
        b = a + ' ' + currenttime
        a_time_temp = time.mktime(time.strptime(b, '%Y-%m-%d %H:%M:%S')) + 0.6  # 转时间戳   补个平均时差

        if a_time_temp - 0.9 <= a_time <= a_time_temp + 0.9:
            pass
        else:
            set_val('a_time', a_time_temp)
    except:
        logger.exception('this is an exception message')



def findpos():
    Px = get_val('Px')
    Py = get_val('Py')
    region = (Px, Py, Px + 500, Py + 500)
    sc = grab_screen(region=region)
    img = np.asarray(sc)
    dick_target = get_val('dick_target')
    template = dick_target[2]
    time_template = dick_target[3]
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    px_relative = get_val('px_relative')
    py_relative = get_val('py_relative')
    px_timerelative = get_val('px_timerelative')
    py_timerelative = get_val('py_timerelative')
    Position_frame = get_val('Position_frame')
    P_relative2 = get_val('P_relative2')

    res2 = cv2.matchTemplate(img, time_template, cv2.TM_CCOEFF_NORMED)
    time_min_val, time_max_val, time_min_loc, time_max_loc = cv2.minMaxLoc(res2)

    if max_val > 0.75:  # 找不到不动作
        ##计算位置
        set_val('px_lowestprice', max_loc[0] + px_relative + Px)
        set_val('py_lowestprice', max_loc[1] + py_relative + Py)
        Px = get_val('Px')
        Py = get_val('Py')
        set_val('px_calculate_relative', max_loc[0] + px_relative) ##计算得到相差
        set_val('py_calculate_relative', max_loc[1] + py_relative)
        ##计算时间位置
        set_val('Px_currenttime', time_max_loc[0] + px_timerelative + Px)    #时间的位置
        set_val('Py_currenttime', time_max_loc[1] + py_timerelative + Py)

        px_lowestprice = get_val('px_lowestprice')
        py_lowestprice = get_val('py_lowestprice')
        set_val('Px_lowestprice', px_lowestprice)
        set_val('Py_lowestprice', py_lowestprice)
        Px_lowestprice = get_val('Px_lowestprice')
        Py_lowestprice = get_val('Py_lowestprice')

        print("找到的Px_lowestprice", Px_lowestprice)
        print("找到的Py_lowestprice", Py_lowestprice)


        for i in range(len(Position_frame)):
            Position_frame[i][0] = Px_lowestprice + P_relative2[i][0]
            Position_frame[i][1] = Py_lowestprice + P_relative2[i][1]
        set_val('Position_frame', Position_frame)
        ##几个截图位置, 通过服务器传来的相对位置 进行计算
        refresh_area_relative = get_val('refresh_area_relative')
        confirm_area_relative = get_val('confirm_area_relative')
        yan_confirm_area_relative = get_val('yan_confirm_area_relative')
        Pos_controlframe_relative = get_val('Pos_controlframe_relative')
        Pos_yanzhengma_relative = get_val('Pos_yanzhengma_relative')  # 验证码所在位置
        Pos_question_relative = get_val('Pos_question_relative')  # 问题所在位置
        Pos_yanzhengmaframe_relative = get_val('Pos_yanzhengmaframe_relative')  # 验证码框放置位置
        Pos_result_relative = get_val('Pos_result_relative')  # 出价结果
        Pos_login_relative = get_val('Pos_login_relative')  # 出价结果

        set_val('refresh_area', [refresh_area_relative[0] + Px_lowestprice, refresh_area_relative[1] + Py_lowestprice,
                                 refresh_area_relative[2] + Px_lowestprice, refresh_area_relative[3] + Py_lowestprice])
        set_val('confirm_area', [confirm_area_relative[0] + Px_lowestprice, confirm_area_relative[1] + Py_lowestprice,
                                 confirm_area_relative[2] + Px_lowestprice, confirm_area_relative[3] + Py_lowestprice])
        set_val('yan_confirm_area', [yan_confirm_area_relative[0] + Px_lowestprice,
                                     yan_confirm_area_relative[1] + Py_lowestprice,
                                     yan_confirm_area_relative[2] + Px_lowestprice,
                                     yan_confirm_area_relative[3] + Py_lowestprice])
        set_val('Pos_controlframe', [Pos_controlframe_relative[0] + Px_lowestprice,
                                     Pos_controlframe_relative[1] + Py_lowestprice])
        set_val('Pos_yanzhengma', [Position_frame[6][0] + Pos_yanzhengma_relative[0],
                                   Position_frame[6][1] + Pos_yanzhengma_relative[1],
                                   Position_frame[6][0] + Pos_yanzhengma_relative[2],
                                   Position_frame[6][1] + Pos_yanzhengma_relative[3]])  # 验证码所在位置
        set_val('Pos_question', [Position_frame[6][0] + Pos_question_relative[0],
                                   Position_frame[6][1] + Pos_question_relative[1],
                                   Position_frame[6][0] + Pos_question_relative[2],
                                   Position_frame[6][1] + Pos_question_relative[3]])  # 问题所在位置
        set_val('Pos_yanzhengmaframe', [Px_lowestprice + Pos_yanzhengmaframe_relative[0],
                                        Py_lowestprice + Pos_yanzhengmaframe_relative[1]])  # 验证码框放置位置
        set_val('Pos_timeframe', (245 - 344 + Px_lowestprice, 399 - 183 + Py_lowestprice))
        set_val('Pos_result', [Pos_result_relative[0] + Px_lowestprice, Pos_result_relative[1] + Py_lowestprice,
                                 Pos_result_relative[2] + Px_lowestprice, Pos_result_relative[3] + Py_lowestprice])

        set_val('Pos_login', [Pos_login_relative[0] + Px_lowestprice, Pos_login_relative[1] + Py_lowestprice,
                              Pos_login_relative[2] + Px_lowestprice, Pos_login_relative[3] + Py_lowestprice])

        lowestprice_sizex = get_val('lowestprice_sizex')
        lowestprice_sizey = get_val('lowestprice_sizey')
        currenttime_sizex = get_val('currenttime_sizex')
        currenttime_sizey = get_val('currenttime_sizey')
        set_val('lowest', [Px_lowestprice, Py_lowestprice, lowestprice_sizex + Px_lowestprice,
                           lowestprice_sizey + Py_lowestprice])
        Px_currenttime = get_val("Px_currenttime")
        Py_currenttime = get_val("Py_currenttime")
        set_val('currenttime', [Px_currenttime, Py_currenttime, Px_currenttime + currenttime_sizex,
                                Py_currenttime + currenttime_sizey])
        dis_x = 100
        dis_y = 150
        x1 = Px_lowestprice - dis_x  # 截图起始点
        y1 = Py_lowestprice - dis_y
        lowest = get_val('lowest')
        refresh_area = get_val('refresh_area')
        confirm_area = get_val('confirm_area')
        Pos_yanzhengma = get_val('Pos_yanzhengma')
        yan_confirm_area = get_val('yan_confirm_area')
        currenttime = get_val('currenttime')
        Pos_question = get_val('Pos_question')  ##验证码问题所在位置
        Pos_result = get_val('Pos_result') #拍牌结果位置
        cal_area = [lowest, refresh_area, confirm_area, Pos_yanzhengma,
                    yan_confirm_area, currenttime, Pos_question, Pos_result]  # 构建截图区域
        use_area = []
        set_val('sc_area', [Px_lowestprice - dis_x, Py_lowestprice - dis_y, Px_lowestprice + 600, Py_lowestprice + 120])
        for i in range(len(cal_area)):
            temp = [cal_area[i][0] - x1, cal_area[i][1] - y1, cal_area[i][2] - x1, cal_area[i][3] - y1]
            use_area.append(temp)
        set_val('use_area', use_area)



def new_screenshot(area):
    hwin = win32gui.GetDesktopWindow()
    width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)
    bmp.SaveBitmapFile(memdc, 'screenshot.bmp')



def only_screenshot(area):  # x,y  pos      w,h size
    a = time.time()
    x, y = int(area[0]), int(area[1])
    w, h = int(area[2]), int(area[3])
    hwnd = win32gui.FindWindow(None, "win32")
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w - x, h - y)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((-x, -y), (w, h), dcObj, (0, 0), win32con.SRCCOPY)
    im = dataBitMap.GetBitmapBits(True)  # Tried False also
    bmpinfo = dataBitMap.GetInfo()
    img = np.frombuffer(im, dtype='uint8')
    img.shape = (bmpinfo['bmHeight'], bmpinfo['bmWidth'], 4)
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    b = time.time()
    return img

# @calculate_usetime
def cut_img():  # 将所得的img 处理成  lowestprice_img   confirm_img  yanzhengma_confirm_img  refresh_img
    use_area = get_val('use_area')
    sc_area = get_val('sc_area')
    img = only_screenshot(sc_area)  # 获取得到的截图
    img = np.asarray(img)  # 转化为numpy数组
    try:
        set_val('imgpos_lowestprice', img[use_area[0][1]:use_area[0][3], use_area[0][0]:use_area[0][2]])  # ok
        set_val('imgpos_refresh', img[use_area[1][1]:use_area[1][3], use_area[1][0]:use_area[1][2]])  # ok
        set_val('imgpos_confirm', img[use_area[2][1]:use_area[2][3], use_area[2][0]:use_area[2][2]])
        set_val('imgpos_yanzhengma', img[use_area[3][1]:use_area[3][3], use_area[3][0]:use_area[3][2]])  # ok
        set_val('imgpos_yanzhengmaconfirm', img[use_area[4][1]:use_area[4][3], use_area[4][0]:use_area[4][2]])  # ok
        set_val('imgpos_currenttime', img[use_area[5][1]:use_area[5][3], use_area[5][0]:use_area[5][2]])
        set_val('imgpos_question', img[use_area[6][1]:use_area[6][3], use_area[6][0]:use_area[6][2]])
        set_val('imgpos_result', img[use_area[7][1]:use_area[7][3], use_area[7][0]:use_area[7][2]])
    except:
        logger.error("cut_img 这里出错")
        logger.exception('this is an exception message')


def findrefresh():
    dick_target = get_val('dick_target')
    template = dick_target[0]
    imgpos_refresh = get_val('imgpos_refresh')
    sc = imgpos_refresh
    img = cv2.cvtColor(sc, cv2.COLOR_BGR2GRAY)  # 转灰度图
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # print(max_val)

    if max_val >= 0.8:
        print("refresh")
        OnClick_Shuaxin()  # 刷新验证码
        set_val('yanzhengma_view', True)  # 激活放大器
        set_val('yanzhengma_find', False)  # 表示需要确认是否找到验证码
    else:
        set_val('yanzhengma_find', True)


def findconfirm():
    dick_target = get_val('dick_target')
    smartprice_chujia = get_val('smartprice_chujia')
    template = dick_target[1]
    imgpos_confirm = get_val('imgpos_confirm')
    sc = imgpos_confirm
    img = cv2.cvtColor(sc, cv2.COLOR_BGR2GRAY)  # 转灰度图
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val >= 0.7:
        # print(max_val, smartprice_chujia)
        if not smartprice_chujia:
            OnClick_confirm()  #点击确认
        else:
            print("找到确认")
            Smart_chujia()
        ##结果查找
        need_findresult = get_val('need_findresult')
        if need_findresult:
            print("查找结果")
            get_result()  ##确认结果
        #再判定是否需要点击确认


    else:
        set_val('need_findresult', True)

def get_result():
    result_dick =  get_val('result_dick')
    imgpos_result = get_val('imgpos_result')
    print(imgpos_result)
    imgpos_result = cv2.cvtColor(imgpos_result, cv2.COLOR_BGR2GRAY)
    for result, img in result_dick.items():
        print(result)
        res = cv2.matchTemplate(img, imgpos_result, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        print('max_val=', max_val)
        if max_val >= 0.7:
            set_val('need_findresult', False)  ##关闭
            wx.CallAfter(pub.sendMessage, 'update info', action=result)
            return result
    print('未知')
    return '未知结果'


def findfirstprice():
    try:
        print('findfirstprice')
        dick_target = get_val('dick_target')
        template = dick_target[4]
        template2 = dick_target[5]
        sc = grab_screen()
        img = np.asarray(sc)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        res2 = cv2.matchTemplate(img, template2, cv2.TM_CCOEFF_NORMED)
        min_val, max_val2, min_loc, max_loc = cv2.minMaxLoc(res2)
        if max_val >= 0.9 or max_val2 >= 0.9:
            set_val('firstprice_done', True)
        else:
            set_val('firstprice_done', False)
    except:
        pass

def find_yan_confirm():
    try:
        dick_target = get_val('dick_target')
        template = dick_target[1]
        imgpos_yanzhengmaconfirm = get_val('imgpos_yanzhengmaconfirm')
        sc = imgpos_yanzhengmaconfirm
        img = cv2.cvtColor(sc, cv2.COLOR_BGR2GRAY)  # 转灰度图
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        yanzhengma_control = get_val('yanzhengma_control')


        if max_val > 0.9 and yanzhengma_control:
            set_val('yanzhengma_view', True)
            # smartprice_chujia = get_val('smartprice_chujia')
            # if smartprice_chujia:
            #     set_val('smartprice_tijiao', True)  ##这代表出价成功
        elif max_val <= 0.9:
            set_val('yanzhengma_view', False)
            set_val('yanzhengma_close', True)
            set_val('yanzhengma_control', True)
            smartprice_tijiao = get_val('smartprice_tijiao')
            # if smartprice_tijiao:
            #     set_val('smartprice_tijiao', False)  ##这代表出价成功
            #     set_val('smartprice_chujia', False)
    except:
        logger.exception("error message")

# @calculate_usetime
def Price_read():
    imgpos_lowestprice = get_val('imgpos_lowestprice')

    # avt = get_val('avt')
    # avt += 1
    # if avt == 500 or avt == 501:
    #     avt = 0
    # set_val('avt', avt)
    # cv2.imwrite(r'./pic/%s.png' % avt, imgpos_lowestprice)

    lowest_price_img = cv2.cvtColor(imgpos_lowestprice, cv2.COLOR_BGR2GRAY)
    price = readpic(lowest_price_img)
    return price
