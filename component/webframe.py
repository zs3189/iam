# encoding: utf-8
'''
@author: zhushen
@contact: 810909753@q.com
@time: 2018/1/22 13:58
'''
from component.infopanel import InfoPanel
from component.staticmethod import *
from component.OperationFrame import OperationPanel
import wx.html2 as webview
from wx.lib.buttons import GenButton as wxButton
from component.imgcut import timeset, findfirstprice
from component.YanzhengmaFrame import YanzhengmaFrame, TipFrame
from component.imgcut import cut_pic, find_yan_confirm

from component.variable import init_pos, get_val, set_val, get_dick
import logging
logger = logging.getLogger()

class ButtonPanel(wx.Panel):
    def __init__(self, parent, webstatus_label, moni):
        size = get_val('buttonpanel_size')
        pos = get_val('buttonpanel_pos')
        wx.Panel.__init__(self, parent, size=size, pos=pos)
        self.parent = parent
        self.timefont = wx.Font(18, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False)
        self.statusfont = wx.Font(18, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False)
        ##时间同步功能
        if not moni:
            self.remotetime_button = wxButton(self, label='同步服务器时间', size=(90, 25), pos=(693, 2))
            self.remotetime_button.SetBackgroundColour("#ACD6ff")
            self.remotetime_button.Bind(wx.EVT_BUTTON, self.getremotetime)

        self.webtime_button = wxButton(self, label='同步网页时间', size=(90, 25), pos=(785, 2))
        self.webtime_button.SetBackgroundColour("#ACD6ff")
        self.SetBackgroundColour("#ACD6ff")
        self.webtime_button.Bind(wx.EVT_BUTTON, self.timeautoajust)

        self.smallbutton = wxButton(self, label='>', size=(16, 25), pos=(875, 2))
        self.smallbutton.SetBackgroundColour("#ACD6ff")
        self.SetBackgroundColour("#ACD6ff")
        self.smallbutton.Bind(wx.EVT_BUTTON, self.changewebsize)

        if not moni:
            guopai_dianxin = get_val('guopai_dianxin')
            if guopai_dianxin:
                urlchange_dianxin_label = get_val('urlchange_dianxin_label')
                self.urlchange_button = wxButton(self, label=urlchange_dianxin_label, pos=(600, 2), size=(90, 25))
                self.urlchange_button.Bind(wx.EVT_BUTTON, self.urlchange)
                self.urlchange_button.SetBackgroundColour("#ACD6ff")
            else:
                urlchange_nodianxin_label = get_val('urlchange_nodianxin_label')
                self.urlchange_button = wxButton(self, label=urlchange_nodianxin_label, pos=(600, 2), size=(90, 25))
                self.urlchange_button.Bind(wx.EVT_BUTTON, self.urlchange)
                self.urlchange_button.SetBackgroundColour("#ACD6ff")

        self.webstatus = wx.StaticText(self, label=webstatus_label, pos=(10, 2), size=(120, 30),)
        self.webstatus.SetFont(self.statusfont)
        # self.webstatus.SetBackgroundColour((0, 0, 150))
        self.webstatus.SetForegroundColour((255, 240, 240))

        # self.refresh_web = wxButton(self, label='刷新界面', size=(80, 25), pos=(25, 2), style=wx.BORDER_NONE)
        # self.refresh_web.SetBackgroundColour("#ACD6ff")

        self.autotime_timer = wx.Timer(self)  # 创建定时器
        self.Bind(wx.EVT_TIMER, self.autotime_set_timer, self.autotime_timer)  # 绑定一个定时器事件
        self.autotime_timer.Start(1000)  # 设定时间间隔

        # 没边框按钮
        # from wx.lib.buttons import GenButton as wxButton
        # tmpButton = wxButton(parent, id, u'删除学生', pos=(10, 10), size=(100, 30), style=wx.BORDER_NONE)
        # tmpButton.SetBackgroundColour("#ff0000")
        # tmpButton.SetForegroundColour("#ffffff")

    def changewebsize(self, event):
        x, y = self.parent.GetSize()
        if x >950:
            smallwebsize = get_val('smallwebsize')
            self.parent.SetSize(smallwebsize)
        else:
            websize = get_val('websize')
            self.parent.SetSize(websize)

    def Modify(self):  # 更新
        dc = wx.BufferedDC(wx.ClientDC(self))  # ClientDC客户区  ，BufferedDC双缓冲绘图设备
        moni_on = get_val('moni_on')
        true_time = get_val('true_time')
        time_local = time.localtime(true_time)
        st = time.strftime("%H:%M:%S", time_local)  # + '.' + str(b_time)
        # st="%s:%s:%s"%(b_time[0],b_time[1],b_time[2])
        set_val('true_time_str', st)
        st = '国拍时间：%s' % st
        w, h = self.GetClientSize()
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        dc.SetFont(self.timefont)
        tw, th = dc.GetTextExtent(st)
        dc.DrawText(st, (w - tw) / 2, (h) / 2 - th / 2)


    def autotime_set_timer(self, event):
        autotime_on = get_val('autotime_on')
        moni_on = get_val('moni_on')
        guopai_on = get_val('guopai_on')
        test = get_val('test')
        if not test and moni_on:
            self.timeautoajust()
        elif test and autotime_on:
            self.timeautoajust()
        ##判断是否完成第一次出价
        firstprice_done = get_val('firstprice_done')
        if not firstprice_done:
            if guopai_on:
                findfirstprice()
                firstprice_done = get_val('firstprice_done')


    ## 获取服务器时间
    def getremotetime(self, event):
        from component.app_thread import GetremotetimeThread
        getremotetimethread = GetremotetimeThread()
        wx.CallAfter(pub.sendMessage, 'update info', action='同步服务器时间')



    ## 同步本地时间
    def timeautoajust(self, event=None):
        imgpos_currenttime = get_val('imgpos_currenttime')
        timeset(imgpos_currenttime)  # 调用时间同步
        if event:
            wx.CallAfter(pub.sendMessage, 'update info', action='同步网页时间')

    def urlchange(self, event):
        guopai_dianxin = get_val('guopai_dianxin')
        urlchange_dianxin_label = get_val('urlchange_dianxin_label')
        urlchange_nodianxin_label = get_val('urlchange_nodianxin_label')
        if guopai_dianxin:
            self.urlchange_button.SetLabel(urlchange_dianxin_label)
            set_val('guopai_dianxin', False)
            url_nodianxin = get_val('url_nodianxin')
            print(url_nodianxin, 'url_nodianxin')
            self.parent.htmlpanel.webview.LoadURL(url_nodianxin)
            nodianxin_webstatus_label = get_val('nodianxin_webstatus_label')
            self.webstatus.SetLabel(nodianxin_webstatus_label)

        else:
            self.urlchange_button.SetLabel(urlchange_nodianxin_label)
            set_val('guopai_dianxin', True)
            url_dianxin = get_val('url_dianxin')
            print(url_dianxin)
            self.parent.htmlpanel.webview.LoadURL(url_dianxin)
            dianxin_webstatus_label = get_val('dianxin_webstatus_label')
            self.webstatus.SetLabel(dianxin_webstatus_label)

    #
    # def OnKeyDown(self, event):
    #     # 按键时相应代码
    #     # 	event.ControlDown
    #     kc = event.GetKeyCode()
    #     import win32gui
    #     if 32 <= kc <= 126:
    #         win32gui.MessageBox(0, "test,ok!", 'test', 0)
    #         print(kc)
    #     if event.AltDown():
    #         print('ff', kc)


class HtmlPanel(wx.Panel):
    def __init__(self, parent, moni):
        htmlpanel_size = get_val('htmlpanel_size')
        htmlpanel_pos = get_val('htmlpanel_pos')
        wx.Panel.__init__(self, parent, size=htmlpanel_size, pos=htmlpanel_pos, style=wx.BORDER_NONE)
        self.frame = self.GetTopLevelParent()
        self.titleBase = self.frame.GetTitle()
        htmlsize = get_val('htmlsize')
        webview_pos = get_val('webview_pos')
        self.webview = webview.WebView.New(self, size=htmlsize, pos=webview_pos,
                                           style=wx.BORDER_NONE)
        self.webview.EnableContextMenu(False)
        url_moni = get_val('url_moni')
        url_dianxin = get_val('url_dianxin')
        url_nodianxin = get_val('url_nodianxin')
        guopai_dianxin = get_val('guopai_dianxin')
        if moni:
            print("fsdfsfsfdsfsf")
            self.webview.LoadURL(url_moni)
        elif guopai_dianxin:
            self.webview.LoadURL(url_dianxin)
            print("352", url_dianxin)
        else:
            self.webview.LoadURL(url_nodianxin)
            print("Jfsd", url_nodianxin)



class BottomeStatusbarPanel(wx.Panel):
    def __init__(self, parent, moni):
        bottomestatusbarpanel_size = get_val('bottomestatusbarpanel_size')
        bottomestatusbarpanel_pos = get_val('bottomestatusbarpanel_pos')
        wx.Panel.__init__(self, parent, size=bottomestatusbarpanel_size, pos=bottomestatusbarpanel_pos,
                          style=wx.BORDER_NONE)

        self.textfont = wx.Font(12, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False)


        self.registered_bitmap = wx.Bitmap('icons/registered.png')
        self.unregistered_bitmap = wx.Bitmap('icons/unregistered.png')
        # self.slow_bitmap = wx.Bitmap('icons/slow.png')
        self.medium_bitmap = wx.Bitmap('icons/medium.png')
        self.quick_bitmap = wx.Bitmap('icons/quick.png')
        # self.veryquick_bitmap = wx.Bitmap('icons/veryquick.png')



    def Modify(self):  # 更新
        dc = wx.BufferedDC(wx.ClientDC(self))  # ClientDC客户区  ，BufferedDC双缓冲绘图设备
        w, h = self.GetClientSize()
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))  ##保存刷新不闪烁
        dc.Clear()
        register_label = get_val("register_label")
        dc.SetFont(self.textfont)
        tw, th = dc.GetTextExtent(register_label)
        dc.DrawText(register_label, 35, (h) / 2 - th / 2)

        ##更改激活状态
        activate_status = get_val('activate_status')
        if activate_status:
            dc.DrawBitmap(self.registered_bitmap, 2, 0, True)
        else:
            dc.DrawBitmap(self.unregistered_bitmap, 2, 0, True)

        netspeed_label = get_val("netspeed_label")
        dc.SetFont(self.textfont)
        tw, th = dc.GetTextExtent(netspeed_label)
        dc.DrawText(netspeed_label, 806, (h) / 2 - th / 2)
        dc.DrawBitmap(self.quick_bitmap, 850, -3, True)

        strategy_label = get_val('strategy_label')
        strategy_name = get_val('strategy_name')
        strategy_description = get_dick('strategy_description')
        text = "{0}  {1}         {2}".format(strategy_label, strategy_name, strategy_description)
        dc.SetFont(self.textfont)
        tw, th = dc.GetTextExtent(text)
        dc.DrawText(text, 270, (h) / 2 - th / 2)


class CurrentStatusFrame(wx.Frame):
    def __init__(self, parent):
        self.parent = parent
        x, y = parent.Position
        x0, y0 = get_val('CurrentStatusFramePos')
        CurrentStatusFrameSize = get_val('CurrentStatusFrameSize')
        super(CurrentStatusFrame, self).__init__(parent,  size=CurrentStatusFrameSize, pos=(x+x0, y+y0),
                                        style=wx.FRAME_TOOL_WINDOW | wx.FRAME_FLOAT_ON_PARENT | wx.BORDER_NONE)
        self.currentstatuspanel = CurrentStatusPanel(self)

        # self.Bind(wx.EVT_ACTIVATE, self.print)
        self.Disable()




class CurrentStatusPanel(wx.Panel):
    def __init__(self, parent):
        CurrentStatusFrameSize = get_val('CurrentStatusFrameSize')
        super(CurrentStatusPanel, self).__init__(parent, size=CurrentStatusFrameSize, style=wx.BORDER_NONE)
        self.SetBackgroundColour("#585858")
        self.timefont = wx.Font(12, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False)
        self.parent = parent


    def Modify(self):  # 更新
        self.SetForegroundColour('#FF8000')  ##设置文字颜色
        x1, y1 = get_val('status_time')
        x2, y2 = get_val('lowestprice_text')
        x3, y3 = get_val('pricelabeltext')
        x4, y4 = get_val('pricetext')
        x5, y5 = get_val('timestatustext')
        x6, y6 = get_val('pricestatustext')
        ##当前时间label
        currenttime_label = get_val("currenttime_label")
        dc = wx.BufferedDC(wx.ClientDC(self))  # ClientDC客户区  ，BufferedDC双缓冲绘图设备
        a_time = get_val('a_time')
        temp = int((a_time - int(a_time)) * 10)
        time_local = time.localtime(a_time)
        st = time.strftime("%H:%M:%S", time_local)  # + '.' + str(b_time)
        set_val('a_time_str', st)

        # st="%s:%s:%s"%(b_time[0],b_time[1],b_time[2])
        st = '{0}{1}.{2}'.format(currenttime_label, st, temp)
        w, h = self.GetClientSize()
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        dc.SetFont(self.timefont)
        tw, th = dc.GetTextExtent(st)
        dc.DrawText(st, x1, y1)

        ##显示最低成交价
        findpos_on = get_val('findpos_on')
        yanzhengma_view = get_val('yanzhengma_view')
        final_stage = get_val('final_stage')  ##判断是不是11点之后

        if findpos_on or yanzhengma_view or not final_stage: ##final_stage 是否处于修改出价阶段
            if self.parent.IsShown():
                self.parent.Show(False)
            # lowestpricelabel = get_val('lowestpricelabel')
            # lowestpricetext = "{0}: {1}".format(lowestpricelabel, '未识别')
            # dc.DrawText(lowestpricetext, x2, y2)
        else:
            if not self.parent.IsShown():
                self.parent.Show(True)
            lowest_price = get_val('lowest_price')
            lowestpricelabel = get_val('lowestpricelabel')
            lowestpricetext = "{0}: {1}".format(lowestpricelabel, lowest_price)
            dc.DrawText(lowestpricetext, x2, y2)

            ##第二行  出价情况
            userprice = get_val('userprice')
            tijiao_on = get_val('tijiao_on')
            usertime = get_val('usertime')
            smartprice_chujia = get_val('smartprice_chujia')
            strategy_type = get_dick('strategy_type')

            if userprice and tijiao_on:  ##提交状态
                current_pricestatus_label = get_val('current_pricestatus_label')
                current_pricestatus = get_val('current_pricestatus')
                pricelabeltext = "{0}".format(current_pricestatus_label)
                pricetext = "{0}".format(current_pricestatus)
                ##第三行  剩余状态
                # 显示截止时间与当前时间相差
                max_price = get_val('lowest_price') + 300
                diff_price = int(userprice) - max_price
                # 显示截止时间与当前时间相差
                currenttime = get_val('a_time')
                timediff = float(usertime) - float(currenttime)
                timestatustext = "提交倒计时{0:.1f}秒".format(timediff)
                pricestatustext = "差价{0}".format(diff_price)
                dc.DrawText(pricelabeltext, x3, y3)
                dc.DrawText(pricetext, x4, y4)
                dc.DrawText(timestatustext, x5, y5)
                dc.DrawText(pricestatustext, x6, y6)
            else:
                if smartprice_chujia:
                    current_pricestatus_label = get_val('current_pricestatus_label')
                    current_pricestatus = get_val('current_pricestatus')
                    pricelabeltext = "{0}".format(current_pricestatus_label)
                    pricetext = "{0}".format(current_pricestatus)
                    ##第三行  剩余状态
                    max_price = get_val('lowest_price') + 300
                    # diff_price = int(userprice) - max_price
                    diff_price = '-'
                    timediff = '-'
                    timestatustext = "提交倒计时{0}秒".format(timediff)
                    pricestatustext = "差价{0}".format(diff_price)
                    dc.DrawText(pricelabeltext, x3, y3)
                    dc.DrawText(pricetext, x4, y4)
                    dc.DrawText(timestatustext, x5, y5)
                    dc.DrawText(pricestatustext, x6, y6)
                else:
                    tijiao_num = get_val('tijiao_num')
                    # 显示截止时间与当前时间相差
                    currenttime = get_val('a_time')
                    if tijiao_num == 1:
                        one_time1 = get_val('one_real_time1')
                        timediff = float(one_time1) - float(currenttime)
                        ##修改状态
                        one_time1 = get_val('one_time1')
                        one_diff = get_val('one_diff')
                        current_pricestatus = '{0}秒加{1}'.format(one_time1, one_diff)
                        set_val('current_pricestatus', current_pricestatus)
                    elif tijiao_num == 2:
                        second_real_time1 = get_val('second_real_time1')
                        timediff = float(second_real_time1) - float(currenttime)
                        ##修改状态
                        second_time1 = get_val('second_time1')
                        second_diff = get_val('second_diff')
                        current_pricestatus = '{0}秒加{1}'.format(second_time1, second_diff)
                        set_val('current_pricestatus', current_pricestatus)
                    else:
                        timediff = '-'
                    current_pricestatus_label = get_val('current_pricestatus_label')
                    current_pricestatus = get_val('current_pricestatus')
                    pricelabeltext = "{0}".format(current_pricestatus_label)
                    pricetext = "{0}".format(current_pricestatus)
                    if timediff == '-':
                        timestatustext = "出价倒计时{0}秒".format(timediff)
                    else:
                        timestatustext = "出价倒计时{0:.1f}秒".format(timediff)

                # pricestatustext = "差价{0}".format('-')
                    pricestatustext = "请勿操作"
                    dc.DrawText(pricelabeltext, x3, y3)
                    dc.DrawText(pricetext, x4, y4)
                    dc.DrawText(timestatustext, x5, y5)
                    dc.DrawText(pricestatustext, x6, y6)



class WebFrame(wx.Frame):
    def __init__(self, px, py, id, name, tablabel, moni):  # name:窗口显示名称
        websize = get_val('websize')
        wx.Frame.__init__(self, None, id, name, size=(websize[0], websize[1]), pos=(px, py - 10),
                          style=wx.CAPTION | wx.CLOSE_BOX)
        ##LOGO
        mainicon = get_val('mainicon')
        self.icon = wx.Icon(mainicon, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)
        self.moni = moni
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.htmlpanel = HtmlPanel(self, moni)  ## moni: True
        if moni:
            webstatus_label = get_val('moni_webstatus_label')
            self.buttonpanel = ButtonPanel(self, webstatus_label, moni)  ##moni: True
        else:
            guopai_dianxin = get_val('guopai_dianxin')
            if guopai_dianxin:
                webstatus_label = get_val('dianxin_webstatus_label')
                self.buttonpanel = ButtonPanel(self, webstatus_label, moni)  ##moni: True
            else:
                webstatus_label = get_val('nodianxin_webstatus_label')
                self.buttonpanel = ButtonPanel(self, webstatus_label, moni)  ##moni: True
        self.operationpanel = OperationPanel(self, tablabel)
        self.infopanel = InfoPanel(self)
        self.bottomstatusbarpanel = BottomeStatusbarPanel(self, moni)

        self.currentstatusframe = CurrentStatusFrame(self)
        self.currentstatusframe.Show(False)
        Yanzhengmasize = get_val('Yanzhengmasize')
        self.yanzhengmaframe = YanzhengmaFrame(self, Yanzhengmasize)
        self.tipframe = TipFrame(self)

        self.Bind(wx.EVT_MOVE, self.childmove)

        self.timer1 = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.Price_view, self.timer1)  # 绑定一个定时器事件，主判断
        self.timer1.Start(40)  # 设定时间间隔

        # pub.subscribe(self.Price_view, 'price_view')  ##替换为CALL触发

        self.hotkey_open2()
        # self.Bind(wx.EVT_ACTIVATE , self.hotkey_open)
        if moni:
            pub.subscribe(self.refresh_web, 'moni refresh_web')
        else:
            pub.subscribe(self.refresh_web, 'guopai refresh_web')
            pub.subscribe(self.onekey_login, 'onekey_login')  # 登录


    ##移动跟随
    def childmove(self, event):
        #位置重新计算
        Px, Py = self.Position
        init_pos(Px, Py)
        set_val('Px', Px)
        set_val('Py', Py)
        x, y = self.Position
        x0, y0 = get_val('CurrentStatusFramePos')
        self.currentstatusframe.Move(x+x0, y+y0)
        x1, y1 = get_val('YanzhengmaFramePos')
        try:
            self.yanzhengmaframe.Move(x+x1, y+y1)  # 移动到新位置
        except:
            logger.exception('this is an exception message')
        x2, y2 = get_val('TipFramePos')
        try:
            self.tipframe.Move(x+x2, y+y2)  # 移动到新位置
        except:
            logger.exception('this is an exception message')
        wx.CallAfter(pub.sendMessage, 'dialog close')

    def refresh_web(self):
        self.htmlpanel.webview.Reload()
        strategy_type = get_dick("strategy_type")
        if strategy_type == 0:
            init_strategy()
        elif strategy_type == 1:
            init_strategy()

    def onekey_login(self):
        bidnumber_js = get_val('bidnumber_js')
        print(bidnumber_js)
        bidpassword_js = get_val('bidpassword_js')
        idcard_js = get_val('idcard_js')
        # self.htmlpanel.webview.RunScript(bidnumber_js)
        # self.htmlpanel.webview.RunScript(bidpassword_js)
        # self.htmlpanel.webview.RunScript("var a = document.getElementById('dtidcard')")
        # self.htmlpanel.webview.RunScript("a.setAttribute('style', 'display: block');")
        # self.htmlpanel.webview.RunScript(idcard_js)
        try:
            browser = self.htmlpanel.webview
            print(browser)
            print(bidnumber_js)
            browser.RunScript(bidnumber_js)
            browser.RunScript(bidpassword_js)
            browser.RunScript(idcard_js)
        except:
            logger.exception("error message")

    def Price_view(self, event=None):
        moni_on = get_val('moni_on')
        guopai_on = get_val('guopai_on')
        paishou = get_val('paishou')
        manage = get_val('manage')
        on1 = moni_on and self.moni
        on2 = guopai_on and not self.moni
        on = on1 or on2
        if on and self.IsShown() and not self.IsIconized():
            ###子面板刷新
            self.buttonpanel.Modify()
            self.bottomstatusbarpanel.Modify()
            self.currentstatusframe.currentstatuspanel.Modify()
            self.Yanzhengma_scale() #判定验证码放大
            self.hotkey_control()  #热键激活与否
            if not paishou and not manage:
                self.firstpirce_tip()
            ##自动验证码查看
            self.auto_yanzhengma()
        else:
            self.currentstatusframe.Show(False)
            self.yanzhengmaframe.Show(False)
            self.tipframe.Show(False)


    #打开验证码查看
    def auto_yanzhengma(self):
        ###自动验证码打开
        a_time = get_val('a_time')
        Position_frame = get_val('Position_frame')
        auto_yanzhengma_time = get_val('auto_yanzhengma_time')
        auto_query_on = get_dick('auto_query_on')
        auto_yanzhengma_on = get_val('auto_yanzhengma_on')
        yanzhengma_view = get_val('yanzhengma_view')
        if  not yanzhengma_view:
            if auto_query_on and not auto_yanzhengma_on and  auto_yanzhengma_time < a_time < auto_yanzhengma_time + 0.5:
                moni_on = get_val('moni_on')
                if not moni_on:
                    setText(str(100000))  # 出一定超出的价格
                    selfdelete()
                else:
                    Paste_moni(100000)
                Click(Position_frame[1][0], Position_frame[1][1])
                set_val('auto_yanzhengma_on', True)
                timer1 = threading.Timer(8, self.close_yanzhengma) ##8秒后关闭
                timer1.start()
                wx.CallAfter(pub.sendMessage, 'update info', action='触发验证码自动预览')
            elif a_time < auto_yanzhengma_time:
                set_val('auto_yanzhengma_on', False)  ##设置成查看状态

    #关闭验证码查看
    def close_yanzhengma(self):
        Position_frame = get_val('Position_frame')
        auto_yanzhengma_on = get_val('auto_yanzhengma_on')
        print(auto_yanzhengma_on)
        # if auto_yanzhengma_on:
        Click(Position_frame[7][0], Position_frame[7][1])
        print("fsdfsdsfs")
        self.tipframe.Show(False)
        set_val('auto_yanzhengma_on', False)  ##设置成查看状态

    def Yanzhengma_scale(self):
        ##------------------------------
        ###判定验证码放大框
        final_stage = get_val('final_stage')
        yanzhengma_view = get_val('yanzhengma_view')
        Yanzhengmasize = get_val('Yanzhengmasize')
        if final_stage:
            find_yan_confirm()
            yanzhengma_scale = get_dick('yanzhengma_scale')
            if yanzhengma_scale:
                yanzhengma_close = get_val("yanzhengma_close")
                if yanzhengma_close:
                    try:
                        if self.yanzhengmaframe.IsShown():
                            self.yanzhengmaframe.Show(False)
                            self.tipframe.Show(False)  ##关闭提交提示
                            set_val('auto_yanzhengma_on', False) ##关闭自动关闭验证码的触发
                            self.currentstatusframe.Show(True)
                            set_val('yanzhengma_view', False)  #开关与动作在一起
                    except:
                        logger.exception('this is an exception message')
                #验证码放大是否需要刷新
                if yanzhengma_view:
                    auto_yanzhengma_on = get_val("auto_yanzhengma_on")
                    set_val('yanzhengma_close', False)
                    path = get_val('path')
                    yanpath = path + "\\yanzhengma.png"
                    cut_pic(Yanzhengmasize, yanpath)  # 直接调用得到 png 保存图片
                    try:
                        yanpath = get_val('yanpath')
                        yan = self.yanzhengmaframe
                        yan.Show()
                        yan.ShowImage(yanpath)
                        self.currentstatusframe.Show(False)
                        ##打开提示
                        if not auto_yanzhengma_on:
                            self.tipframe.Show(True)
                            self.tipframe.ShowImage('icons/tip1.png')
                        else:
                            self.tipframe.Show(True)
                            self.tipframe.ShowImage('icons/tip2.png')
                    except:  # 找不到的情况下也要重新创建
                        logger.exception('this is an exception message')
                    finally:
                        pass
        else:
            set_val('yanzhengma_view', False)
            set_val('yanzhengma_close', True)
            if self.yanzhengmaframe.IsShown():
                self.yanzhengmaframe.Show(False)
                self.currentstatusframe.Show(True)

    def firstpirce_tip(self):
        first_stage = get_val('first_stage')
        final_stage = get_val('final_stage')
        firstprice_done = get_val('firstprice_done')
        yanzhengma_view = get_val('yanzhengma_view')
        ##处于第一次出价状态
        try:
            if first_stage and not firstprice_done:
                ##判断是否需要第一次出价提示
                self.tipframe.Show(True)
                self.tipframe.ShowImage('icons/firstprice.png')
            if not yanzhengma_view and firstprice_done:
                if self.tipframe.IsShown():
                    self.tipframe.Show(False)
            elif not first_stage and not final_stage:
                if self.tipframe.IsShown():
                    self.tipframe.Show(False)
        except:
            logger.exception('this is an exception message')



    def hotkey_control(self):
        # 根据当前句柄判断是否需要激活快捷键
        hwnd = win32gui.GetForegroundWindow()
        currenthwnd = self.Handle
        hotkey_on = get_val('hotkey_on')
        yanhwnd = self.yanzhengmaframe.Handle
        statushwnd = self.currentstatusframe.Handle
        if hwnd == currenthwnd or hwnd == yanhwnd or hwnd == statushwnd:
            if not hotkey_on:
                self.hotkey_open()
                try:
                    wx.CallAfter(pub.sendMessage, 'dialog close')
                    wx.CallAfter(pub.sendMessage, 'account close')
                except:
                    logger.exception("error message")

        elif hotkey_on and hwnd != currenthwnd or hwnd != yanhwnd or hwnd != statushwnd:
            self.hotkey_close()

    def hotkey_open2(self):
        ###热键控制
        hotkey_on = get_val('hotkey_on')
        if not hotkey_on:
            print("获得焦点")
            Hotkey_open()

    def hotkey_open(self):
        ###热键控制
        hotkey_on = get_val('hotkey_on')
        if not hotkey_on:
            print("获得焦点")
            Hotkey_open()

    def hotkey_close(self):
        hwnd = win32gui.GetForegroundWindow()
        currenthwnd = self.Handle
        hotkey_on = get_val('hotkey_on')
        if hotkey_on:
            print("失去焦点")
            Hotkey_close()


    def init_frame(self):
        self.operationpanel.init_ui()
        self.infopanel.init_info()


    def OnClose(self, event):
        set_val('web_on', False)
        set_val('view_time', False)
        set_val('moni_on', False)
        set_val('guopai_on', False)
        self.yanzhengmaframe.Show(False)
        self.tipframe.Show(False)
        self.currentstatusframe.Show(False)
        event.Skip()
        id = get_val('topframe')
        topframe = wx.FindWindowById(id)
        topframe.Show(True)

