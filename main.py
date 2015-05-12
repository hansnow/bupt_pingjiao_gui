#! /usr/bin/env python3
# -*- coding: utf8 -*-
from tkinter import *
from PIL import Image, ImageTk
import requests as rq
from bs4 import BeautifulSoup

COOKIES = {}
class makeLoginPanel:

    def __init__(self,master):
        global COOKIES
        self.master = master
        with  open('image.jpg','wb') as f:
            r = rq.get('http://jwxt.bupt.edu.cn/validateCodeAction.do')
            COOKIES = rq.utils.dict_from_cookiejar(r.cookies)
            print(COOKIES)
            f.write(r.content)
        frame = Frame(master)
        frame.pack()
        
        # variable to store checkbox value
        # self.keeplogin = IntVar()

        self.UserLabel = Label(frame,
            text="Username")
        self.PassLabel = Label(frame,
            text="Password")
        self.HashLabel = Label(frame,
            text="HashCode")
        self.UserLabel.grid(row=0,column=0,sticky=W)
        self.PassLabel.grid(row=1,column=0,sticky=W)
        self.HashLabel.grid(row=2,column=0,sticky=W)

        self.UserEntry = Entry(frame)
        self.PassEntry = Entry(frame,show='*')
        self.HashEntry = Entry(frame)
        self.UserEntry.grid(row=0,column=1,columnspan=2)
        self.PassEntry.grid(row=1,column=1,columnspan=2)
        self.HashEntry.grid(row=2,column=1,columnspan=2)

        self.ImgBox = ImageTk.PhotoImage(file='image.jpg')
        self.ImgLabel = Label(frame, image=self.ImgBox)
        self.ImgLabel.image = self.ImgBox
        self.ImgLabel.grid(row=3,column=0,columnspan=2)
        
        self.RefreshBtn = Button(frame, text="Refresh",command=self.refresh)
        self.RefreshBtn.grid(row=3,column=2,sticky=W+E)

        # self.KeepLoginChkBtn = Checkbutton(frame,text='KeepLogin',variable=self.keeplogin)
        # self.KeepLoginChkBtn.grid(row=4,column=0)

        self.LoginBtn = Button(frame,text='Login',command=self.login)
        self.LoginBtn.grid(row=4,column=1,columnspan=2,sticky=W+E)

    def refresh(self):
        with  open('image.jpg','wb') as f:
            r = rq.get('http://jwxt.bupt.edu.cn/validateCodeAction.do',cookies=COOKIES)
            # f.write(io.StringIO(r.content))
            f.write(r.content)
        self.ImgBox = ImageTk.PhotoImage(file='image.jpg')
        self.ImgLabel.config(image=self.ImgBox)
    def login(self):
        global COOKIES
        username = self.UserEntry.get()
        password = self.PassEntry.get()
        hashcode = self.HashEntry.get()

        # just for test locally
        # payload = {
        # "type": "sso",
        # "zjh": username,
        # "mm": password,
        # "v_yzm": hashcode
        # }
        with open('test/account.txt','r') as f:
            data = f.read().split(':')
            print(data)
        payload = {
        "type": "sso",
        "zjh": data[0],
        "mm": data[1],
        "v_yzm": hashcode
        }

        r = rq.post('http://jwxt.bupt.edu.cn/jwLoginAction.do',data=payload,allow_redirects=False,cookies=COOKIES)
        if not ('URP 综合教务系统 - 登录' in r.text):
            # print(r.text)
            print('login success')
            LoginRoot.destroy()
        else:

            print('login failed')

class makeMainPanel:
    def __init__(self,master):
        frame = Frame(master)
        frame.pack()

        # Test Command Here
        # print(self.getStuName())
        # print(self.getCourseInfo())

        # layout here
        self.SimpleBtn = Button(frame,text='Simple Mode',command=self.makeSimplePanel)
        self.SimpleBtn.grid(row=0,column=0)

        self.ProBtn = Button(frame,text='Pro Mode',command=self.makeProPanel)
        self.ProBtn.grid(row=0,column=1)


    def makeSimplePanel(self):
        self.SimpleRoot = Toplevel()
        makeSimplePanel(self.SimpleRoot)


    def makeProPanel(self):
        self.ProRoot = Toplevel()
        makeProPanel(self.ProRoot)

        



class makeSimplePanel:
    def __init__(self,master):
        frame = Frame(master)
        frame.pack()

        # Variable that store the RadioBtn value
        self.RadioBtnValue = IntVar()
        self.TeachersName = ''
        for i in getCourseInfo():
            self.TeachersName += (i['TeacherName'] + '、')
        self.TeachersName = self.TeachersName[0:-1]
        print(self.TeachersName)

        self.InfoLbl = Label(frame,text='对 '+self.TeachersName+' 等老师做出统一评价')
        self.InfoLbl.grid(row=0,column=0,columnspan=8)

        self.RadioBtn1 = Radiobutton(frame,text='优+',variable=self.RadioBtnValue,value=1)
        self.RadioBtn1.grid(row=1,column=0)

        self.RadioBtn2 = Radiobutton(frame,text='优',variable=self.RadioBtnValue,value=2)
        self.RadioBtn2.grid(row=1,column=1)

        self.RadioBtn3 = Radiobutton(frame,text='优-',variable=self.RadioBtnValue,value=3)
        self.RadioBtn3.grid(row=1,column=2)

        self.RadioBtn4 = Radiobutton(frame,text='良+',variable=self.RadioBtnValue,value=4)
        self.RadioBtn4.grid(row=1,column=3)

        self.RadioBtn5 = Radiobutton(frame,text='良',variable=self.RadioBtnValue,value=5)
        self.RadioBtn5.grid(row=1,column=4)

        self.RadioBtn6 = Radiobutton(frame,text='中',variable=self.RadioBtnValue,value=6)
        self.RadioBtn6.grid(row=1,column=5)

        self.RadioBtn7 = Radiobutton(frame,text='及格',variable=self.RadioBtnValue,value=7)
        self.RadioBtn7.grid(row=1,column=6)

        self.RadioBtn8 = Radiobutton(frame,text='不及格',variable=self.RadioBtnValue,value=8)
        self.RadioBtn8.grid(row=1,column=7)

        self.RadioBtnValue.set(2)

        self.CommentText = Text(frame,height=5,width=25,font=("Helvetica", 20))
        self.CommentText.grid(row=2,column=0,columnspan=8,rowspan=1,sticky=W+E+N+S)
        # self.CommentText.tag_config("test",font=("Helvetica", 20))
        self.CommentText.insert(END,'老师授课时重点突出，层次分明，注重理论和实际相结合，语言生动，举例充分恰当，鼓励学生踊跃发言，课堂气氛活跃。')

        self.SubmitBtn = Button(frame,text="提交",command=self.submitComment)
        self.SubmitBtn.grid(row=3,column=3,columnspan=2,sticky=W+E)
    def submitComment(self):
        print(self.CommentText.get('0.0',END).strip())

class makeProPanel:
    def __init__(self,master):
        self.MainFrame = Frame(master)
        self.MainFrame.pack()

        # self.ChildFrame = []
        # self.ChildLbl = []
        # self.ChildEntry = []

        self.ChkBtnVar = []
        self.ChkBtn = []
        self.InfoArray = getCourseInfo()


        self.initFrame()

        self.CommentText = Text(self.MainFrame,height=5,font=("Helvetica", 20))
        self.CommentText.grid(row=len(self.ChkBtn),column=0,sticky=W+E)

        self.submitBtn = Button(self.MainFrame,text="提交",command=self.submitComment)
        self.submitBtn.grid(row=len(self.ChkBtn)+1,column=0)


        # self.addFrame(getCourseInfo())
    # def addFrame(self,InfoArray):
    #     for count,data in enumerate(InfoArray):
            # self.ChildFrame.append(Frame(self.MainFrame))
            # self.ChildFrame[count].pack()

            # self.ChildLbl.append(Label(self.ChildFrame[count],text=data['TeacherName'],justify=LEFT))
            # self.ChildLbl[count].grid(row=count,column=0,columnspan=2,sticky=W+E)

            # self.ChildEntry.append(Entry(self.ChildFrame[count]))
            # self.ChildEntry[count].grid(row=count,column=2,columnspan=2)

    def initFrame(self):
        for count,data in enumerate(self.InfoArray):
            # print('enter the for loop')
            self.ChkBtnVar.append(IntVar())
            # print('add a variable')
            self.ChkBtn.append(Checkbutton(self.MainFrame,text=data['TeacherName']+' ('+data['CourseName']+')',variable=self.ChkBtnVar[count]))
            # print('create a chkbtn')
            self.ChkBtn[count].grid(row=count,column=0)
            # print('chkbtn has been layouted')

    def submitComment(self):
        for count,data in enumerate(self.ChkBtnVar):
            if data.get():
                print(self.InfoArray[count]['TeacherName'])

        print(self.CommentText.get('0.0',END).strip())

    def refreshFrame(self):
        pass

def getStuName():
    html = rq.get('http://jwxt.bupt.edu.cn/menu/s_top.jsp',cookies=COOKIES).text
    soup = BeautifulSoup(html)
    name = soup.select('a[onclick="logout()"]')[0].previous_sibling.strip()
    return name.split('\xa0')[1]

def getCourseInfo():

    # this function should return availiable course info
    # that is, courses that has been evaluated will be ignored

    html = rq.get('http://jwxt.bupt.edu.cn/jxpgXsAction.do?oper=listWj',cookies=COOKIES).text
    soup = BeautifulSoup(html)
    CourseInfo = []
    img = soup.select('img[title="评估"]')
    for i in img:
        content = i['name'].split('#@')
        CourseInfo.append({
            "num1": content[0],
            "num2": content[1],
            "num3": content[5],
            "TeacherName": content[2],
            "CourseName": content[4]
            })
    return CourseInfo
root = Tk()
LoginRoot = Toplevel()
LoginPanel = makeLoginPanel(LoginRoot)
def callback(event):
    print('callback function')
    MainPanel = makeMainPanel(root)
    root.deiconify()
    LoginRoot.unbind("<Destroy>",TopDestroy)
root.withdraw()
TopDestroy = LoginRoot.bind("<Destroy>",callback)
root.mainloop()