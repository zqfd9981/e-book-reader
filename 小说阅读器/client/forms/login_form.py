import tkinter as tk
from tkinter import *
from tkinter import messagebox
from typechange.message_type import MessageType
from ExtendedSocket import ExtendedSocket
from typechange.bytetotype import *
import client.memory
from client.forms.register_form import RegisterForm
from client.forms.bookshelf_form import BookshelfForm

class LoginForm(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.createForm()
        self.sc = client.memory.sc
        master.protocol("WM_DELETE_WINDOW", self.destroy_window)

    def createForm(self):
        #self.master.resizable(width=False, height=False)
        self.master.geometry('300x100')        
        self.master.title("小说阅读器-登陆")
        Label(self, text="用户名").grid(row=0,sticky=E)
        Label(self, text="密码").grid(row=1,sticky=E)
        self.username = Entry(self)
        self.password = Entry(self, show="*")
        self.username.grid(row=0, column=1,columnspan=2)
        self.password.grid(row=1, column=1,columnspan=2)
        self.buttonframe = Frame(self)
        self.buttonframe.grid(row=2, column=0, columnspan=2, pady=(4, 6))  
        self.logbtn = Button(self.buttonframe, text="登陆", command=self.do_login)
        self.logbtn.grid(row=0, column=0)
        self.registerbtn = Button(self.buttonframe, text="注册", command=self.show_register)
        self.registerbtn.grid(row=0, column=1)
        self.pack()
        

    def do_login(self):
        """使用账号和密码登陆"""
        username = self.username.get()
        password = self.password.get()
        if not username:
            messagebox.showerror("出错了！", "用户名不能为空")
            return
        if not password:
            messagebox.showerror("出错了！", "密码不能为空")
            return
        self.sc.send_message(MessageType.login, [username, password])
        message = self.sc.recv_message()
        if not message:
            messagebox.showerror('连接失败', '请稍后再试~')
            self.destroy_window()
            return
        if message['type'] == MessageType.login_failed:
            messagebox.showerror('登录失败', '用户名或密码错误！')
            return
        if message['type'] == MessageType.login_successful:
            client.memory.current_user = username 
            print('登陆成功')
            self.master.destroy()
            bookshelf = Toplevel(client.memory.tk_root, takefocus=True)
            BookshelfForm(bookshelf)
            return

    def show_register(self):
        register_form = Toplevel()
        RegisterForm(master=register_form)

    def destroy_window(self):
        client.memory.tk_root.destroy()