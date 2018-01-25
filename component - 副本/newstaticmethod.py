'''
@author: zhushen
@contact: 810909753@q.com
@time: 2018/1/22 9:33
'''
import win32gui
import win32con
import win32api
import win32clipboard
import time
import cv2
import threading
from .imgcut import readpic
import pyautogui as pg
from .variable import set_val, get_val
def Click(x, y):  # 鼠标点击
    a = win32gui.GetCursorPos()
    x = int(x)
    y = int(y)
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
def Click2(x, y):  # 鼠标点击
    a = win32gui.GetCursorPos()
    x = int(x)
    y = int(y)
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    win32api.SetCursorPos(a)  # 模拟键盘输入
def Paste():  # ctrl + V
    win32api.keybd_event(17, 0, 0, 0)  # ctrl的键位码是17
    win32api.keybd_event(86, 0, 0, 0)  # v的键位码是86
    win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
def Paste_moni():
    win32api.keybd_event(17, 0, 0, 0)  # ctrl的键位码是17
    win32api.keybd_event(86, 0, 0, 0)  # v的键位码是86
    win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
def setText(aString):
    aString = aString.encode('utf-8')
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32con.CF_TEXT, aString)
    win32clipboard.CloseClipboard()
def Delete():
    a = time.clock()
    win32api.keybd_event(0x08, 0, 0, 0)
    win32api.keybd_event(0x08, 0, win32con.KEYEVENTF_KEYUP, 0)
    b = time.clock()
def OnClick_Tijiao(cls):
    global web_on, tijiao_on, one_delay, second_delay, tijiao_num
    global tijiao_on, chujia_on, confirm_one, confirm_need, twice
    set_val('confirm_need',True)
    if tijiao_num == 1:
        timer = threading.Timer(one_delay, Tijiao)
        timer.start()
        set_val('tijiao_on',False)
        if twice:
            set_val('tijiao_num',2)
    elif tijiao_num == 2:
        set_val('tijiao_num',0)
        timer = threading.Timer(second_delay, Tijiao)
        timer.start()
        set_val('tijiao_on',False)
    else:
        Tijiao()
def Tijiao():
    global tijiao_on, tijiao_OK, tijiao_num, chujia_on
    global Position
    Click(Position[2][0], Position[2][1])
    set_val('tijiao_OK',False)  #需要按E解锁，自动提交
    set_val('chujia_on',True)  #激活自动
    global confirm_one
    if not confirm_one:  # 激活确认
        pass
def SmartTijiao():
    global tijiao_on, tijiao_OK, tijiao_num, confirm_need, own_price1, own_price2
    global moni_on, moni_second, changetime, a_time ,lowest_price, twice
    set_val('confirm_need',True)
    if moni_on:
        interval = moni_second - changetime
    else:
        interval = a_time - changetime
    if tijiao_num == 2:  # 说明是第二次出价
        if lowest_price <= own_price2 - 600:
            print("触发延迟")
            set_val('tijiao_num',0)
            timer = threading.Timer(0.5, cls.Tijiao)
            timer.start()
            set_val('tijiao_on',False)
        elif lowest_price == own_price2 - 500 and interval < 0.95:
            set_val('tijiao_num',0)
            timesleep = (1 - interval) / 3 + 0.25
            timer = threading.Timer(timesleep, cls.Tijiao)
            timer.start()
            set_val('tijiao_on',False)
        else:
            set_val('tijiao_num',0)
            Tijiao()
            set_val('tijiao_on',False)
    elif tijiao_num == 1:
        if lowest_price <= own_price1 - 600:
            timer = threading.Timer(0.5, cls.Tijiao)
            timer.start()
            set_val('tijiao_on',False)
            if twice:
                set_val('tijiao_num',2)
        elif lowest_price == own_price1 - 500 and interval < 0.95:
            timesleep = (1 - interval) / 3 + 0.25
            timer = threading.Timer(timesleep, Tijiao)
            timer.start()
            set_val('tijiao_on',False)
            if twice:
                set_val('tijiao_num',2)
        else:
            Tijiao()
            set_val('tijiao_on',False)
            if twice:
                set_val('tijiao_num',2)
def OnClick_Shuaxin():
    global Position
    Click(Position[3][0], Position[3][1])
    Click(Position[5][0], Position[5][1])
    global yanzhengma_view, yanzhengma_close, yanzhengma_count
    set_val('yanzhengma_view',True)  #激活放大器
    set_val('yanzhengma_count',0)  #归零
def OnClick_confirm():
    global Position
    Click(Position[4][0], Position[4][1])
def OnClick_chujia():
    global web_on, lowest_price, yanzhengma_count,Position
    global tijiao_num, own_price1, own_price2, one_diff, second_diff
    global tijiao_on, chujia_on, twice
    global refresh_need, refresh_one, chujia_interval, yanzhengma_view
    set_val('yanzhengma_count',0)  #计数器，制造延迟
    set_val('yanzhengma_view',True)  #打开验证码放大器
    set_val('tijiao_on',True)  #激活自动出价
    set_val('refresh_need',True)  #激活刷新验证码
    if tijiao_num == 1:
        set_val('own_price1',lowest_price+one_diff)
        setText(str(own_price1))
        selfdelete()
        Click(Position[1][0], Position[1][1])
        Click(Position[5][0], Position[5][1])
        set_val('tijiao_on',True)
        set_val('chujia_on',False)
        set_val('chujia_interval',False)  #间隔结束
    elif tijiao_num == 2 and twice:
        set_val('own_price2',lowest_price+second_diff)
        setText(str(own_price2))
        selfdelete()
        Click(Position[1][0], Position[1][1])
        Click(Position[5][0], Position[5][1])
        set_val('tijiao_on',True)
        set_val('chujia_on',False)
        set_val('chujia_interval',False)  #间隔结束
def OnH_chujia():
    global yanzhengma_view, yanzhengma_count, Position, lowest_price, own_price1, one_diff
    set_val('yanzhengma_view',True)
    set_val('yanzhengma_count',0)
    set_val('own_price1',lowest_price+one_diff)
    setText(str(own_price1))
    selfdelete()
    Click(Position[1][0], Position[1][1])
    Click(Position[5][0], Position[5][1])
def selfdelete():
    global Position, moni_on
    Click2(Position[6][0], Position[6][1] - 5)
    Click2(Position[6][0], Position[6][1])
    Click2(Position[6][0], Position[6][1])
    Delete()
    Delete()
    if moni_on:
        Paste_moni()  # 粘贴
    else:
        Paste()  # 真粘贴
def selfChujia():
    global price_view, price_count, yanzhengma_count, yanzhengma_view, Position
    Click(Position[4][0], Position[4][1])
    Click(Position[0][0], Position[0][1])
    Click(Position[1][0], Position[1][1])
    Click(Position[5][0], Position[5][1])
    set_val('price_view',True)
    set_val('price_count',0)
    set_val('yanzhengma_count',0)
    set_val('yanzhengma_view',True)
def selfTijiao():
    global Position
    Click(Position[2][0], Position[2][1])
def OnClick_Backspace():
    pg.press('backspace')
