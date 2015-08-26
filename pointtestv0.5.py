#! /usr/bin/env python
# coding: utf8
# version:v0.5
# code by: xiong.mingjun
"""
Change log:
v0.4 使用telnetlib来判断服务器是否正常
v.05 添加四种新的api：
    1 音频信息查询
    2 音频信息更新
    3 音频信息删除
    4 音频详情查询
"""
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from Tkinter import *
from tkMessageBox import *
import time
import urllib
import types
import hmac,hashlib
import httplib
import telnetlib

class MyFrame():
    """Test for MyFrame"""

    # 定义错误代码
    dict_error_msg = {

        402:'appid错误',
        403:'签名错误',
        404:'没有数据',
        405:'参数错误（缺少必要的参数，或参数格式错误）',
        500:'服务器繁忙',
        501:'规则引擎配置错误',
        601:'注册时该积分用户已存在',
        602:'未找到积分用户',
        603:'积分余额不足',
        604:'未找到对应的交易（out_trade_no）',
        605:'积分已过期',
        606:'订单已经被处理',
        711:'tonginfo访问的音频ID记录不存在',
        712:'数据记录不存在，或是之前已经被删除'

    }

    # 定义请求类型
    dict_api_type = {

        1 : '/api/v1/points/reg',
        2 : '/api/v1/points/unreg',
        3 : '/api/v1/points/add',
        4 : '/api/v1/points/calc',
        5 : '/api/v1/points/resume',
        6 : '/api/v1/points/redeem',
        7 : '/api/v1/points/query',
        8 : '/api/v1/points/detail',
        9 : '/api/v1/mit/query',
        10: '/api/v1/mit/update',
        11: '/api/v1/mit/delete',
        12: '/api/v1/mit/tonginfo'

    }

    # 初始化所有的字段
    str_appid = ''
    str_user_id = ''
    str_sign = ''
    str_trade_no = ''
    str_exp_date = ''
    str_cause = ''
    str_before_date = ''
    str_end_date = ''
    str_inc_trade_no = ''
    str_busi_type = ''
    str_total_fee = ''
    str_ex_points = ''
    str_page_no = ''
    str_page_size = ''
    str_timestamp = str(int(time.time()))
    str_user_level = ''
    str_user_ponits = ''
    str_add_points = ''
    str_secretkey = ''
    str_host_ip = '192.168.0.125'
    str_host_port = '8443'
    str_toneid = ''
    str_content = ''
    str_contenttype = '100'  # 目前只支持100，代之链接
    str_userid = ''

    # 定义包含所有字段的字典表
    dict_fields_defined = {

        "appid" : str_appid,                   # sring(11), not null
        "out_user_id" : str_user_id,           # string(32), not null
        "sign" : str_sign,                     # str(64), not null
        "out_trade_no" : str_trade_no,         # str(64), not null
        "business_type" : str_busi_type,       # int(3), not null
        "total_fee" : str_total_fee,           # int(11), not null, by cent
        "exchange_points" : str_ex_points,     # int(11), not bull
        "page_no" : str_page_no,               # int(11), not null
        "page_size" : str_page_size,           # int(2), not null, <=99
        "ts" : str_timestamp,                  # int(11), not null, UTC timestamp
        "user_level" : str_user_level,         # int(2), 1~8, default 1
        "user_points" : str_user_ponits,       # int(11), default 0
        "exp_date" : str_exp_date,             # str(8), yyyyMMdd, default is gloable time
        "cause" : str_cause,                   # string, not null
        "before_date" : str_before_date,       # str(8), yyyyMMdd
        "end_date" : str_end_date,             # str(8), yyyyMMdd
        "inc_trade_no" : str_inc_trade_no,     # str(64)
        "add_user_points" : str_add_points,    # int(11), not null
        "toneid" : str_toneid,                 # string
        "content" : str_content,               # string
        "contenttype" : str_contenttype,       # string
        "userid" : str_userid                  # string        

    }

    # 定义主窗口和两个框架
    master = Tk()
    frame1 = Frame(master)
    frame2 = Frame(master)

    # 定义控件的值
    vUsername = StringVar()
    vAppid = StringVar()
    vTradeNo = StringVar()
    vExPoint = StringVar()
    vCause = StringVar()
    vInitPoint = StringVar()
    vInitLevel = StringVar()
    vAddPoint = StringVar()
    vTradeType = StringVar()
    vExpTime = StringVar()
    vAmount = StringVar()
    vStartTime = StringVar()
    vEndTime = StringVar()
    vPage = StringVar()
    vNumbers = StringVar()
    vHost = StringVar()
    vPort = StringVar()
    vSecretKey = StringVar()
    vinTradeno = StringVar()
    vtoneId = StringVar()
    vcontent = StringVar()
    vcontenttype = StringVar()
    vusername = StringVar()


    # 定义菜单选项对应的变量
    vChoose = StringVar()

    # 定义窗口的所有控件，label为提示语，text为输入控件
    # 其中空行也使用了label
    label1 = Label(frame1,text='注册用户名：')
    text1 = Entry(frame1,textvariable=vUsername)
    label2 = Label(frame1,text='appid：')
    text2 = Entry(frame1,textvariable=vAppid)
    label3 = Label(frame1,text='交易号：')
    text3 = Entry(frame1,textvariable=vTradeNo)
    label4 = Label(frame1,text='兑换积分：')
    text4 = Entry(frame1,textvariable=vExPoint)
    label5 = Label(frame1,text='原因：')
    text5 = Entry(frame1,textvariable=vCause)
    label6 = Label(frame1,text='初始等级：')
    text6 = Entry(frame1,textvariable=vInitLevel)
    label7 = Label(frame1,text='初始积分：')
    text7 = Entry(frame1,textvariable=vInitPoint)
    label8 = Label(frame1,text='添加积分：')
    text8 = Entry(frame1,textvariable=vAddPoint)
    label9 = Label(frame1,text='交易类型：')
    text9 = Entry(frame1,textvariable=vTradeType)
    label10 = Label(frame1,text='过期时间：')
    text10 = Entry(frame1,textvariable=vExpTime)
    label11 = Label(frame1,text='交易金额：')
    text11 = Entry(frame1,textvariable=vAmount)
    label12 = Label(frame1,text='起始时间：')
    text12 = Entry(frame1,textvariable=vStartTime)
    label13 = Label(frame1,text='结束时间：')
    text13 = Entry(frame1,textvariable=vEndTime)
    label14 = Label(frame1,text='查询页数：')
    text14 = Entry(frame1,textvariable=vPage)
    label15 = Label(frame1,text='每页条数：')
    text15 = Entry(frame1,textvariable=vNumbers)
    label16 = Label(frame1,text='IP：')
    text16 = Entry(frame1,textvariable=vHost)
    label17 = Label(frame1,text='端口：')
    text17 = Entry(frame1,textvariable=vPort)
    label18 = Label(frame1,text='')
    label19 = Label(frame1,text='密钥：')
    text19 = Entry(frame1,textvariable=vSecretKey)
    button1 = Button(frame1,text='提交')
    button2 = Button(frame1,text='清空')
    text20 = Text(frame2)
    label20 = Label(frame1,text='')
    label21 = Label(frame1,text='内部交易号：')
    text21 = Entry(frame1,textvariable=vinTradeno)
    label22 = Label(frame1,text='积分回退',fg='blue')
    label23 = Label(frame1,text='积分兑换',fg='blue')
    label24 = Label(frame1,text='积分查询',fg='blue')
    label25 = Label(frame1,text='积分用户注册',fg='blue')
    label26 = Label(frame1,text='积分用户注销',fg='blue')
    label27 = Label(frame1,text='积分直接累加',fg='blue')
    label28 = Label(frame1,text='积分规则累加',fg='blue')
    label29 = Label(frame1,text='积分明细查询',fg='blue')
    label30 = Label(frame1,text='*',fg='red')
    label31 = Label(frame1,text='*',fg='red')
    label32 = Label(frame1,text='*',fg='red')
    label33 = Label(frame1,text='*',fg='red')
    label34 = Label(frame1,text='*',fg='red')
    label35 = Label(frame1,text='音频ID')
    text22 = Entry(frame1,textvariable=vtoneId)
    label36 = Label(frame1,text='更新内容')
    text23 = Entry(frame1,textvariable=vcontent)
    label37 = Label(frame1,text='类型')
    text24 = Entry(frame1,textvariable=vcontenttype)
    label38 = Label(frame1,text='音频信息查询',fg='blue')
    label39 = Label(frame1,text='音频信息更新',fg='blue')
    label40 = Label(frame1,text='音频信息删除',fg='blue')
    label42 = Label(frame1,text='音频详情查询',fg='blue')
    label41 = Label(frame1,text='用户名')
    text25 = Entry(frame1,textvariable=vusername)


    # 定义构造函数
    def __init__(self):
    
        # 新建菜单
        menubar = Menu(self.master)
        # 定义菜单选项栏
        tradetype = Menu(menubar)
        config = Menu(menubar)
        # 添加单选按钮到菜单选项
        tradetype.add_radiobutton(label='积分回退',command=self.returnPoint,variable=self.vChoose)
        tradetype.add_radiobutton(label='积分兑换',command=self.exchangePoint,variable=self.vChoose)
        tradetype.add_radiobutton(label='积分查询',command=self.queryPoint,variable=self.vChoose)
        tradetype.add_radiobutton(label='积分用户注册',command=self.regCust,variable=self.vChoose)
        tradetype.add_radiobutton(label='积分用户注销',command=self.unregCust,variable=self.vChoose)
        tradetype.add_radiobutton(label='积分直接累加',command=self.addPoint,variable=self.vChoose)
        tradetype.add_radiobutton(label='积分规则累加',command=self.addByRule,variable=self.vChoose)
        tradetype.add_radiobutton(label='积分明细查询',command=self.queryDetail,variable=self.vChoose)
        tradetype.add_radiobutton(label='音频信息查询',command=self.queryToneInfo,variable=self.vChoose)
        tradetype.add_radiobutton(label='音频信息更新',command=self.updateToneInfo,variable=self.vChoose)
        tradetype.add_radiobutton(label='音频信息删除',command=self.deleteToneInfo,variable=self.vChoose)
        tradetype.add_radiobutton(label='音频详情查询',command=self.queryTonedetail,variable=self.vChoose)
        config.add_radiobutton(label='设置',command=self.setconfig,variable=self.vChoose)
        menubar.add_cascade(label='选择交易类型', menu=tradetype)
        menubar.add_cascade(label='服务器配置',menu=config)
        self.frame1.pack(fill=BOTH)
        self.frame2.pack(fill=BOTH)
        # 设置主窗口标题
        self.master.wm_title('积分接口测试v0.5')
        # 设置窗口大小
        self.master.geometry('300x400')
        # 限制改变窗口大小
        self.master.resizable(width=False,height=False)
        # 显示菜单条
        self.master.config(menu=menubar)

    # 用于设置服务器IP和端口，以及appid和secretkey
    def setconfig(self):
        self.forgetAll()
        self.label16.grid(row=0,sticky=E)
        self.text16.grid(row=0,column=1)
        self.label17.grid(row=1,sticky=E)
        self.text17.grid(row=1,column=1)
        self.label2.grid(row=2,sticky=E)
        self.text2.grid(row=2,column=1)
        self.label19.grid(row=3,sticky=E)
        self.text19.grid(row=3,column=1)
        self.label18.grid(row=4)
        # 显示初始IP和端口，以便更改
        if '' == self.vHost.get() and '' == self.vPort.get():
            self.vHost.set(self.str_host_ip)
            self.vPort.set(self.str_host_port)
            self.vAppid.set(self.str_appid)
            self.vSecretKey.set(self.str_secretkey)
        self.button1 = Button(self.frame1,text='提交',width=6,command=self.submit)
        self.button2 = Button(self.frame1,text='清空',width=6,command=self.clearAll)
        self.button1.grid(row=5,padx=10)
        self.button2.grid(row=5,column=1)
        self.label20.grid(row=6)

    def donothing(self):
        showinfo(title='测试菜单选项',message='选择的交易类型是：' + self.vChoose.get())

    def returnPoint(self):

        self.forgetAll()
        self.label22.grid(row=0)
        self.label1.grid(row=1,sticky=E)
        self.text1.grid(row=1,column=1)
        self.label30.grid(row=1,column=2)
        self.label3.grid(row=2,sticky=E)
        self.text3.grid(row=2,column=1)
        self.label31.grid(row=2,column=2)
        self.label18.grid(row=3)
        self.button1 = Button(self.frame1,text='提交',width=6,command=self.submit)
        self.button2 = Button(self.frame1,text='清空',width=6,command=self.clearAll)
        self.button1.grid(row=4)
        self.button2.grid(row=4,column=1)
        self.label20.grid(row=5)

    def exchangePoint(self):
        self.forgetAll()
        self.label23.grid(row=0)
        self.label1.grid(row=1,sticky=E)
        self.text1.grid(row=1,column=1)
        self.label30.grid(row=1,column=2)
        self.label3.grid(row=2,sticky=E)
        self.text3.grid(row=2,column=1)
        self.label31.grid(row=2,column=2)
        self.label4.grid(row=3,sticky=E)
        self.text4.grid(row=3,column=1)
        self.label32.grid(row=3,column=2)
        self.label5.grid(row=4,sticky=E)
        self.text5.grid(row=4,column=1)
        self.label18.grid(row=5)
        self.button1 = Button(self.frame1,text='提交',width=6,command=self.submit)
        self.button2 = Button(self.frame1,text='清空',width=6,command=self.clearAll)
        self.button1.grid(row=6)
        self.button2.grid(row=6,column=1)
        self.label20.grid(row=7)

    def queryPoint(self):
        self.forgetAll()
        self.label24.grid(row=0)
        self.label1.grid(row=1,sticky=E)
        self.text1.grid(row=1,column=1)
        self.label30.grid(row=1,column=2)
        self.label12.grid(row=2,sticky=E)
        self.text12.grid(row=2,column=1)
        self.label13.grid(row=3,sticky=E)
        self.text13.grid(row=3,column=1)
        self.label18.grid(row=4)
        self.button1 = Button(self.frame1,text='提交',width=6,command=self.submit)
        self.button2 = Button(self.frame1,text='清空',width=6,command=self.clearAll)
        self.button1.grid(row=5)
        self.button2.grid(row=5,column=1)
        self.label20.grid(row=6)

    def regCust(self):
        self.forgetAll()
        self.label25.grid(row=0)
        self.label1.grid(row=1,sticky=E)
        self.text1.grid(row=1,column=1)
        self.label30.grid(row=1,column=2)
        self.label6.grid(row=2,sticky=E)
        self.text6.grid(row=2,column=1)
        self.label7.grid(row=3,sticky=E)
        self.text7.grid(row=3,column=1)
        self.label18.grid(row=4)
        self.button1 = Button(self.frame1,text='提交',width=6,command=self.submit)
        self.button2 = Button(self.frame1,text='清空',width=6,command=self.clearAll)
        self.button1.grid(row=5)
        self.button2.grid(row=5,column=1)
        self.label20.grid(row=6)

    def unregCust(self):
        self.forgetAll()
        self.label26.grid(row=0)
        self.label1.grid(row=1,sticky=E)
        self.text1.grid(row=1,column=1)
        self.label30.grid(row=1,column=2)
        self.label18.grid(row=2,sticky=E)
        self.button1 = Button(self.frame1,text='提交',width=6,command=self.submit)
        self.button2 = Button(self.frame1,text='清空',width=6,command=self.clearAll)
        self.button1.grid(row=3)
        self.button2.grid(row=3,column=1)
        self.label20.grid(row=4)

    def addPoint(self):
        self.forgetAll()
        self.label27.grid(row=0)
        self.label1.grid(row=1,sticky=E)
        self.text1.grid(row=1,column=1)
        self.label30.grid(row=1,column=2)
        self.label3.grid(row=2,sticky=E)
        self.text3.grid(row=2,column=1)
        self.label31.grid(row=2,column=2)
        self.label8.grid(row=3,sticky=E)
        self.text8.grid(row=3,column=1)
        self.label32.grid(row=3,column=2)
        self.label9.grid(row=4,sticky=E)
        self.text9.grid(row=4,column=1)
        self.label33.grid(row=4,column=2)
        self.label10.grid(row=5,sticky=E)
        self.text10.grid(row=5,column=1)
        self.label5.grid(row=6,sticky=E)
        self.text5.grid(row=6,column=1)
        self.label34.grid(row=6,column=2)
        self.label18.grid(row=7)
        self.button1 = Button(self.frame1,text='提交',width=6,command=self.submit)
        self.button2 = Button(self.frame1,text='清空',width=6,command=self.clearAll)
        self.button1.grid(row=8)
        self.button2.grid(row=8,column=1)
        self.label20.grid(row=9)

    def addByRule(self):
        self.forgetAll()
        self.label28.grid(row=0)
        self.label1.grid(row=1,sticky=E)
        self.text1.grid(row=1,column=1)
        self.label30.grid(row=1,column=2)
        self.label3.grid(row=2,sticky=E)
        self.text3.grid(row=2,column=1)
        self.label31.grid(row=2,column=2)
        self.label11.grid(row=3,sticky=E)
        self.text11.grid(row=3,column=1)
        self.label32.grid(row=3,column=2)
        self.label10.grid(row=4,sticky=E)
        self.text10.grid(row=4,column=1)
        self.label9.grid(row=5,sticky=E)
        self.text9.grid(row=5,column=1)
        self.label33.grid(row=5,column=2)
        self.label18.grid(row=6)
        self.button1 = Button(self.frame1,text='提交',width=6,command=self.submit)
        self.button2 = Button(self.frame1,text='清空',width=6,command=self.clearAll)
        self.button1.grid(row=7)
        self.button2.grid(row=7,column=1)
        self.label20.grid(row=8)

    def queryDetail(self):
        self.forgetAll()
        self.label29.grid(row=0)
        self.label1.grid(row=1,sticky=E)
        self.text1.grid(row=1,column=1)
        self.label30.grid(row=1,column=2)
        self.label21.grid(row=2,sticky=E)
        self.text21.grid(row=2,column=1)
        self.label12.grid(row=3,sticky=E)
        self.text12.grid(row=3,column=1)
        self.label13.grid(row=4,sticky=E)
        self.text13.grid(row=4,column=1)
        self.label14.grid(row=5,sticky=E)
        self.text14.grid(row=5,column=1)
        self.label31.grid(row=5,column=2)
        self.label15.grid(row=6,sticky=E)
        self.text15.grid(row=6,column=1)
        self.label32.grid(row=6,column=2)
        self.label18.grid(row=7)
        self.button1 = Button(self.frame1,text='提交',width=6,command=self.submit)
        self.button2 = Button(self.frame1,text='清空',width=6,command=self.clearAll)
        self.button1.grid(row=8)
        self.button2.grid(row=8,column=1)
        self.label20.grid(row=9)

    def queryToneInfo(self):
        self.forgetAll()
        self.label38.grid(row=0)
        self.label35.grid(row=1,sticky=E)
        self.text22.grid(row=1,column=1)
        self.label14.grid(row=2,sticky=E)
        self.text14.grid(row=2,column=1)
        self.label30.grid(row=2,column=2)
        self.label15.grid(row=3,sticky=E)
        self.text15.grid(row=3,column=1)
        self.label31.grid(row=3,column=2)
        self.label18.grid(row=4)
        self.button1 = Button(self.frame1,text='提交',width=6,command=self.submit)
        self.button2 = Button(self.frame1,text='清空',width=6,command=self.clearAll)
        self.button1.grid(row=5)
        self.button2.grid(row=5,column=1)
        self.label20.grid(row=6)

    def updateToneInfo(self):
        self.forgetAll()
        self.label39.grid(row=0)
        self.label35.grid(row=1,sticky=E)
        self.text22.grid(row=1,column=1)
        self.label30.grid(row=1,column=2)
        self.label36.grid(row=2,sticky=E)
        self.text23.grid(row=2,column=1)
        self.label18.grid(row=3)
        self.button1 = Button(self.frame1,text='提交',width=6,command=self.submit)
        self.button2 = Button(self.frame1,text='清空',width=6,command=self.clearAll)
        self.button1.grid(row=4)
        self.button2.grid(row=4,column=1)
        self.label20.grid(row=5)

    def deleteToneInfo(self):
        self.forgetAll()
        self.label40.grid(row=0)
        self.label35.grid(row=1,sticky=E)
        self.text22.grid(row=1,column=1)
        self.label30.grid(row=1,column=2)
        self.label18.grid(row=2)
        self.button1 = Button(self.frame1,text='提交',width=6,command=self.submit)
        self.button2 = Button(self.frame1,text='清空',width=6,command=self.clearAll)
        self.button1.grid(row=3)
        self.button2.grid(row=3,column=1)
        self.label20.grid(row=4)

    def queryTonedetail(self):
        self.forgetAll()
        self.label42.grid(row=0)
        self.label35.grid(row=1,sticky=E)
        self.text22.grid(row=1,column=1)
        self.label30.grid(row=1,column=2)
        self.label41.grid(row=2,sticky=E)
        self.text25.grid(row=2,column=1)
        self.label31.grid(row=2,column=2)
        self.label18.grid(row=3)
        self.button1 = Button(self.frame1,text='提交',width=6,command=self.submit)
        self.button2 = Button(self.frame1,text='清空',width=6,command=self.clearAll)
        self.button1.grid(row=4)
        self.button2.grid(row=4,column=1)
        self.label20.grid(row=5)



    # 用于提交操作或是保存配置信息
    def submit(self):
        self.text20.pack_forget()
        if '设置' == self.vChoose.get():
            if '' != self.vHost.get() and '' != self.vPort.get() and '' != self.vAppid.get() and '' != self.vSecretKey.get():
                try:
                    telnetlib.Telnet(self.vHost.get(),self.vPort.get(),timeout=2)
                except:
                    showerror(message='无法和服务器建立连接，\n请重新确认服务器IP和端口！')
                    return
                self.str_host_port = self.vPort.get()
                self.str_host_ip = self.vHost.get()
                self.str_appid = self.vAppid.get()
                self.str_secretkey = self.vSecretKey.get()
                self.vHost.set(self.str_host_ip)
                self.vPort.set(self.str_host_port)
                self.vAppid.set(self.str_appid)
                self.vSecretKey.set(self.str_secretkey)
                showinfo(message='保存成功！')
            else:
                showwarning(message='服务器IP和端口均不能为空！')
        # 用于求情积分回退
        if '积分回退' == self.vChoose.get():
            if '' != self.vUsername.get() and '' != self.vTradeNo.get() and self.str_appid != '':
                dict_msg = {'appid':self.str_appid,'out_user_id':self.vUsername.get(),'out_trade_no':self.vTradeNo.get(),'ts':self.str_timestamp}
                str_uri = self.fill_ApiMsg(dict_msg,self.str_secretkey,5)
                res,interval,body = self.sendmsg_http(str_uri,self.str_host_ip,self.str_host_port)
                self.showResult(body[14:17],interval,body,'积分回退')
            else:
                showwarning(message='用户名、交易号和appid均不能为空！')
        # 用于请求积分兑换
        if '积分兑换' == self.vChoose.get():
            if '' != self.vUsername.get() and '' != self.vTradeNo.get() and self.str_appid != '' and '' != self.vExPoint.get():
                dict_msg = {'appid':self.str_appid,'out_user_id':self.vUsername.get(),'out_trade_no':self.vTradeNo.get(),'exchange_points':self.vExPoint.get(),'cause':self.vCause.get(),'ts':self.str_timestamp}
                # 删除空字段
                dict_msg = self.removeBlank(dict_msg)
                str_uri = self.fill_ApiMsg(dict_msg,self.str_secretkey,6)
                res,interval,body = self.sendmsg_http(str_uri,self.str_host_ip,self.str_host_port)
                self.showResult(body[14:17],interval,body,'积分兑换')
            else:
                showwarning(message='用户名、交易号、兑换积分和appid均不能为空！')
        # 用于请求积分查询
        if '积分查询' == self.vChoose.get():
            if '' != self.vUsername.get() and self.str_appid != '':
                dict_msg = {'appid':self.str_appid,'out_user_id':self.vUsername.get(),'before_date':self.vStartTime.get(),'end_date':self.vEndTime.get(),'ts':self.str_timestamp}
                # 删除空字段
                dict_msg = self.removeBlank(dict_msg)
                str_uri = self.fill_ApiMsg(dict_msg,self.str_secretkey,7)
                res,interval,body = self.sendmsg_http(str_uri,self.str_host_ip,self.str_host_port)
                self.showResult(body[14:17],interval,body,'积分查询')
            else:
                showwarning(message='用户名和appid均不能为空！')
        # 用于请求积分用户注册
        if '积分用户注册' == self.vChoose.get():
            if '' != self.vUsername.get() and self.str_appid != '':
                dict_msg = {'appid':self.str_appid,'out_user_id':self.vUsername.get(),'user_level':self.vInitLevel.get(),'user_points':self.vInitPoint.get(),'ts':self.str_timestamp}
                # 删除空字段
                dict_msg = self.removeBlank(dict_msg)
                str_uri = self.fill_ApiMsg(dict_msg,self.str_secretkey,1)
                res,interval,body = self.sendmsg_http(str_uri,self.str_host_ip,self.str_host_port)
                self.showResult(body[14:17],interval,body,'积分用户注册')
            else:
                showwarning(message='用户名和appid均不能为空！')
        # 用于请求积分用户注销
        if '积分用户注销' == self.vChoose.get():
            if '' != self.vUsername.get() and self.str_appid != '':
                dict_msg = {'appid':self.str_appid,'out_user_id':self.vUsername.get(),'ts':self.str_timestamp}
                str_uri = self.fill_ApiMsg(dict_msg,self.str_secretkey,2)
                res,interval,body = self.sendmsg_http(str_uri,self.str_host_ip,self.str_host_port)
                self.showResult(body[14:17],interval,body,'积分用户注销')
            else:
                showwarning(message='用户名和appid均不能为空！')
        # 用于请求积分直接累加
        if '积分直接累加' == self.vChoose.get():
            if '' != self.vUsername.get() and '' != self.vTradeNo.get() and self.str_appid != '' and '' != self.vAddPoint.get() and '' != self.vTradeType and '' != self.vCause.get():
                dict_msg = {'appid':self.str_appid,'out_user_id':self.vUsername.get(),'out_trade_no':self.vTradeNo.get(),'add_user_points':self.vAddPoint.get(),'business_type':self.vTradeType.get(),'exp_date':self.vExpTime.get(),'cause':self.vCause.get(),'ts':self.str_timestamp}
                # 删除空字段
                dict_msg = self.removeBlank(dict_msg)
                str_uri = self.fill_ApiMsg(dict_msg,self.str_secretkey,3)
                res,interval,body = self.sendmsg_http(str_uri,self.str_host_ip,self.str_host_port)
                self.showResult(body[14:17],interval,body,'积分直接累加')
            else:
                showwarning(message='用户名、交易号、添加积分、交易类型、积分原因和appid均不能为空！')
        # 用于请求积分规则累加
        if '积分规则累加' == self.vChoose.get():
            if '' != self.vUsername.get() and '' != self.vTradeNo.get() and self.str_appid != '' and '' != self.vAmount.get() and '' != self.vTradeType:
                dict_msg = {'appid':self.str_appid,'out_user_id':self.vUsername.get(),'out_trade_no':self.vTradeNo.get(),'total_fee':self.vAmount.get(),'business_type':self.vTradeType.get(),'exp_date':self.vExpTime.get(),'ts':self.str_timestamp}
                # 删除空字段
                dict_msg = self.removeBlank(dict_msg)
                str_uri = self.fill_ApiMsg(dict_msg,self.str_secretkey,4)
                res,interval,body = self.sendmsg_http(str_uri,self.str_host_ip,self.str_host_port)
                self.showResult(body[14:17],interval,body,'积分规则累加')
            else:
                showwarning(message='用户名、交易号、交易金额、交易类型、和appid均不能为空！')
        # 用于请求积分明细查询
        if '积分明细查询' == self.vChoose.get():
            if '' != self.vUsername.get() and self.str_appid != '' and '' != self.vPage.get() and '' != self.vNumbers.get():
                dict_msg = {'appid':self.str_appid,'out_user_id':self.vUsername.get(),'inc_trade_no':self.vinTradeno.get(),'before_date':self.vStartTime.get(),'end_date':self.vEndTime.get(),'page_size':self.vNumbers.get(),'page_no':self.vPage.get(),'ts':self.str_timestamp}
                # 删除空字段
                dict_msg = self.removeBlank(dict_msg)
                str_uri = self.fill_ApiMsg(dict_msg,self.str_secretkey,8)
                res,interval,body = self.sendmsg_http(str_uri,self.str_host_ip,self.str_host_port)
                self.showResult(body[14:17],interval,body,'积分明细查询')
            else:
                showwarning(message='用户名,页数、查询条数和appid均不能为空！')
        # 用于查询音频信息
        if '音频信息查询' == self.vChoose.get():
            if self.str_appid != '' and '' != self.vPage.get() and '' != self.vNumbers.get():
                dict_msg = {'appid':self.str_appid,'toneid':self.vtoneId.get(),'page_size':self.vNumbers.get(),'page_no':self.vPage.get(),'ts':self.str_timestamp}
                # 删除空字段
                dict_msg = self.removeBlank(dict_msg)
                str_uri = self.fill_ApiMsg(dict_msg,self.str_secretkey,9)
                res,interval,body = self.sendmsg_http(str_uri,self.str_host_ip,self.str_host_port)
                self.showResult(body[14:17],interval,body,'音频信息查询')
            else:
                showwarning(message='页数、查询条数和appid均不能为空！')
        # 用于音频信息更新
        if '音频信息更新' == self.vChoose.get():
            if self.str_appid != '' and self.vtoneId.get() != '':
                dict_msg = {'appid':self.str_appid,'toneid':self.vtoneId.get(),'contenttype':self.str_contenttype,'content':self.vcontent.get(),'ts':self.str_timestamp}
                # 删除空字段
                dict_msg = self.removeBlank(dict_msg)
                str_uri = self.fill_ApiMsg(dict_msg,self.str_secretkey,10)
                res,interval,body = self.sendmsg_http(str_uri,self.str_host_ip,self.str_host_port)
                print body
                self.showResult(body[14:17],interval,body,'音频信息更新')
            else:
                showwarning(message='音频ID、更新内容和appid均不能为空！')
        # 用于音频信息删除
        if '音频信息删除' == self.vChoose.get():
            if self.str_appid != '' and self.vtoneId.get() != '':
                dict_msg = {'appid':self.str_appid,'toneid':self.vtoneId.get(),'ts':self.str_timestamp}
                # 删除空字段
                dict_msg = self.removeBlank(dict_msg)
                str_uri = self.fill_ApiMsg(dict_msg,self.str_secretkey,11)
                res,interval,body = self.sendmsg_http(str_uri,self.str_host_ip,self.str_host_port)
                self.showResult(body[14:17],interval,body,'音频信息删除')
            else:
                showwarning(message='音频ID和appid均不能为空！')
        # 用于音频详情查询
        if '音频详情查询' == self.vChoose.get():
            if self.str_appid != '' and self.vtoneId.get() != '' and self.vusername.get() != '':
                dict_msg = {'appid':self.str_appid,'toneid':self.vtoneId.get(),'userid':self.vusername.get(),'ts':self.str_timestamp}
                # 删除空字段
                dict_msg = self.removeBlank(dict_msg)
                str_uri = self.fill_ApiMsg(dict_msg,self.str_secretkey,12)
                res,interval,body = self.sendmsg_http(str_uri,self.str_host_ip,self.str_host_port)
                self.showResult(body[14:17],interval,body,'音频详情查询')
            else:
                showwarning(message='音频ID、用户名和appid均不能为空！')


    # 用于删除字典的空字段
    def removeBlank(self,dict_msg):
        for key in dict_msg.keys():
            if '' == dict_msg[key]:
                del dict_msg[key]
        return dict_msg

    # 用于隐藏控件，方便重新布局
    def forgetAll(self):
        for i in [self.label1,self.label2,self.label3,self.label4,self.label5,self.label6,self.label7,self.label8,self.label9,
            self.label10,self.label11,self.label12,self.label13,self.label14,self.label15,self.label16,self.button1,self.button2,
            self.text1,self.text2,self.text3,self.text4,self.text5,self.text6,self.text7,self.text8,self.text9,self.text10,
            self.text11,self.text12,self.text13,self.text14,self.text15,self.label17,self.label18,self.text16,self.text17,
            self.label19,self.text19,self.label20,self.label21,self.text21,self.label22,self.label23,self.label24,self.label25,
            self.label26,self.label27,self.label28,self.label29,self.label30,self.label31,self.label32,self.label33,self.label34,
            self.label35,self.label36,self.label37,self.text22,self.text23,self.text24,self.label38,self.label39,self.label40,
            self.label41,self.text25,self.label42]:
            i.grid_forget()
        self.text20.pack_forget()

    # 用于清空控件内容
    def clearAll(self):
        for i in [self.vUsername,self.vPort,self.vHost,self.vNumbers,self.vPage,self.vAmount,self.vCause,self.vAppid,self.vEndTime
            ,self.vStartTime,self.vExpTime,self.vTradeType,self.vAddPoint,self.vTradeNo,self.vExPoint,self.vInitPoint,self.vInitLevel,
            self.vSecretKey,self.vinTradeno,self.vtoneId,self.vcontent,self.vcontenttype,self.vusername]:
            try:
                i.set('')
            except:
                pass
        self.text20.pack_forget()

    # 显示请求结果
    def showResult(self,res,interval,body,reqtype):
        if '200' == res:
            # 请求成功，背景为绿色；失败则为红色
            self.text20 = Text(self.frame2,bg='green')
            self.text20.pack(fill=BOTH)
            self.text20.insert(INSERT,self.vChoose.get()+'\n')
            self.text20.insert(INSERT,'结果：成功\n')
            self.text20.insert(INSERT,'耗时：'+str(interval)+'\n')
            dict_body = eval(body)
            if '积分用户注销' == reqtype:
                self.text20.insert(INSERT,'注销等级：'+str(dict_body['user_level'])+'\n')
                self.text20.insert(INSERT,'注销积分：'+str(dict_body['user_points'])+'\n')
            if '积分直接累加' == reqtype:
                self.text20.insert(INSERT,'当前等级：'+str(dict_body['user_level'])+'\n')
                self.text20.insert(INSERT,'当前积分：'+str(dict_body['user_points'])+'\n')
            if '积分规则累加' == reqtype:
                self.text20.insert(INSERT,'当前等级：'+str(dict_body['user_level'])+'\n')
                self.text20.insert(INSERT,'当前积分：'+str(dict_body['user_points'])+'\n')
                self.text20.insert(INSERT,'添加积分：'+str(dict_body['add_user_points'])+'\n')
            if '积分回退' == reqtype:
                self.text20.insert(INSERT,'当前等级：'+str(dict_body['user_level'])+'\n')
                self.text20.insert(INSERT,'当前积分：'+str(dict_body['user_points'])+'\n')
                self.text20.insert(INSERT,'回退积分：'+str(dict_body['canceled_user_points'])+'\n')
            if '积分兑换' == reqtype:
                self.text20.insert(INSERT,'当前等级：'+str(dict_body['user_level'])+'\n')
                self.text20.insert(INSERT,'当前积分：'+str(dict_body['user_points'])+'\n')
                self.text20.insert(INSERT,'兑换积分：'+str(dict_body['exchange_points'])+'\n')
            if '积分查询' == reqtype:
                self.text20.insert(INSERT,'当前等级：'+str(dict_body['user_level'])+'\n')
                self.text20.insert(INSERT,'当前积分：'+str(dict_body['user_points'])+'\n')
            if '积分明细查询' == reqtype:
                self.text20.insert(INSERT,'查询条数：'+str(dict_body['count'])+'\n')
                self.text20.insert(INSERT,'积分详情：'+str(dict_body['points_history_str'])+'\n')
            if '音频信息查询' == reqtype:
                self.text20.insert(INSERT,'查询条数：'+str(dict_body['totalcount'])+'\n')
                self.text20.insert(INSERT,'音频详情：'+str(dict_body['history_str'])+'\n')
            if '音频信息更新' == reqtype:
                pass
            if '音频信息删除' == reqtype:
                pass
            if '音频详情查寻' == reqtype:
                self.text20.insert(INSERT,'音频类型：'+str(dict_body['tonetype'])+'\n')
                self.text20.insert(INSERT,'音频详情：'+str(dict_body['tonevalue'])+'\n')
        else:
            self.text20 = Text(self.frame2,bg='red')
            self.text20.pack(fill=BOTH)
            self.text20.insert(INSERT,self.vChoose.get()+'\n')
            self.text20.insert(INSERT,'请求结果：失败\n')
            for i in [402,403,404,405,500,501,601,602,603,604,605,606,711,712]:
                if i == int(res):
                    self.text20.insert(INSERT,'失败原因：'+self.dict_error_msg[i]+'\n')
            self.text20.insert(INSERT,'请求耗时：'+str(interval)+'\n')
            #self.text20.insert(INSERT,'返回字段：'+body)

    # 装填消息
    def fill_ApiMsg(self,dict_msg,str_secretkey,int_api_type):
        # 判断消息，删除dict_msg中的空字段
        str_msg = ''
        if 0 == len(dict_msg):
            return 'Parameter dict_msg is empty.'
        # 按照首字母进行排序
        for key in sorted(dict_msg.items(), key = lambda dict_msg:dict_msg[0]):
            str_msg += key[0]+'='+dict_msg[key[0]]+'&'
        # 删除最后一个字符'&'
        str_msg = str_msg[:-1]
        obj_hmac = hmac.new(str_secretkey,str_msg,digestmod=hashlib.sha256)
        str_sign = obj_hmac.hexdigest()
        # 把签名添加到字典里面 
        dict_msg['sign'] = str_sign.upper()
        # 做urlencode，需要提供元组
        str_urlencoding = urllib.urlencode(dict_msg)
        str_uri = self.dict_api_type[int_api_type]+'?'+str_urlencoding
        return str_uri

    # 向服务器发送请求，并等待回复
    def sendmsg_http(self,str_msg_http,str_host_ip,str_host_port):
        # 必须每次新建http连接，此处无法复用
        try:
            obj_conn = httplib.HTTPSConnection(str_host_ip+':'+str_host_port,timeout=5)
        except Exception, e:
            obj_conn.close()
            return e,'xxxx'
        # 发送请求
        try:
            int_st = time.time()
            obj_conn.request('GET',str_msg_http)
        except Exception, e:
            obj_conn.close()
            return e,'xxxx'
        # 获取响应
        try:
            obj_res = obj_conn.getresponse()
        except Exception, e:
            obj_conn.close()
            return e,'xxxx'
        int_interval = time.time() - int_st
        # 这里不能关闭连接，否则解析不出http的body。之前没注释这一句，造成提取不到body
        # obj_conn.close()
        # 返回结果码、耗时、返回字段json
        return obj_res.status,int_interval,obj_res.read()

if __name__ == '__main__':
    myframe = MyFrame()
    mainloop()