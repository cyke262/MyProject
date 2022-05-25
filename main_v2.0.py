import pymssql
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
from tooltip import create_ToolTip

def dbTools():
    conn = pymssql.connect(server='192.168.18.5', user='sa', password='2001', database='test')
    # 获取游标
    cursor = conn.cursor()
    return conn, cursor


class Login(object):
    def __init__(self):
        # 创建主窗口,用于容纳其它组件
        self.root = tkinter.Tk()
        # 给主窗口设置标题内容
        self.root.title("医院信息管理系统")
        self.root.geometry('400x200')

        self.root.config(background="#CCEEFF")

        # 窗口大小不可调
        self.root.resizable(0, 0)

        # 创建一个label名为账户:
        self.label_account = tkinter.Label(self.root, text='账户: ', font=('microsoft yahei', 11), bg="#CCEEFF")
        # 创建一个label名为密码:
        self.label_password = tkinter.Label(self.root, text='密码: ', font=('microsoft yahei', 11), bg="#CCEEFF")

        # 创建一个账号输入框,并设置尺寸
        self.input_account = tkinter.Entry(self.root, width=30)
        # 创建一个密码输入框,并设置尺寸
        self.input_password = tkinter.Entry(self.root, show='*', width=30)

        # 创建一个登录系统的按钮
        self.login_button = tkinter.Button(self.root,
                                           command=self.backstage_interface,
                                           text="登录",
                                           width=10,
                                           bg='#CCDDFF')
        #将回车与登录按钮绑定，同时backstage函数增加event参数
        self.root.bind('<Return>', self.backstage_interface)

        self._gui_arrang()

    # 完成布局
    def _gui_arrang(self):
        self.label_account.place(x=60, y=50)
        self.label_password.place(x=60, y=75)
        self.input_account.place(x=110, y=50)
        self.input_password.place(x=110, y=75)
        self.login_button.place(x=150, y=105)

    # 进行登录信息验证
    def backstage_interface(self, event=''):
        account = self.input_account.get()
        password = self.input_password.get()

        if (len(account) == 0 or len(password) == 0):
            tkinter.messagebox.showerror(message='用户名或密码为空')
            return

        conn, cursor = dbTools()
        sql = "select * from doctor where id={0} and pwd='{1}'".format(
            account, password)
        cursor.execute(sql)
        rows=cursor.fetchone()
        # 关闭游标
        cursor.close()
        # 关闭连接
        conn.close()
        if rows!=None:
            tkinter.messagebox.showinfo(title='登录成功', message='登录成功')
            self.root.destroy()
            o = Menu(account)
        else:
            tkinter.messagebox.showinfo(title='登录失败', message='登录失败')


class Menu(object):
    def __init__(self, id):
        self.name = ' '
        # 创建主窗口,用于容纳其它组件
        self.root = tkinter.Tk()
        # 给主窗口设置标题内容
        self.root.title("医院管理系统")
        self.root.geometry('230x220')

        self.id = id

        # 主菜单栏
        self.main_menu = tkinter.Menu(self.root)
        # 账户菜单栏
        self.reg_menu = tkinter.Menu(self.main_menu, tearoff=False)
        self.reg_menu.add_command(label='切换账户', command=self._changeReg, accelerator="Ctrl+Q")
        # 添加分隔符
        self.reg_menu.add_separator()
        
        self.reg_menu.add_command(label='退出', command=self.root.quit)

        # 在主目录菜单上新增"账户"选项，并通过menu参数与下拉菜单绑定
        self.main_menu.add_cascade(label='账户', menu=self.reg_menu)

        self.root.bind('<Control-q>', self._changeReg)

        # 病人登记 *finish
        self.record_patient_button = tkinter.Button(
            self.root, text="病人登记", width=10, command=self._intoRecordPatient)

        # 病人查询 *finish
        self.query_patient_button = tkinter.Button(
            self.root, text="病人查询", width=10, command=self._intoQueryPatient)

        # 病例查询 *finish
        self.query_pa_list_button = tkinter.Button(
            self.root, text="病例查询", width=10, command=self._intoQueryPaList)

        # 新增病例 *finish
        self.add_pa_list_button = tkinter.Button(self.root,
                                                 text="新增病例",
                                                 width=10,
                                                 command=self._intoAddPaList)
        # 管理中心 *finish
        self.admin_button = tkinter.Button(self.root,
                                           text="管理中心",
                                           width=10,
                                           command=self._intoAdmin)

        # 既往病史 *finish
        self.anamnesis_button = tkinter.Button(self.root,
                                               text="既往病史",
                                               width=10,
                                               command=self._intoAnamnesis)

        # 个人信息 *finish
        self.label_information = tkinter.Label(self.root, text='')

        self._infomation_get()
        self._gui_arrang()

    def _intoRecordPatient(self):
        i = RecordPatient()

    def _intoQueryPatient(self):
        q = QueryPatient()

    def _intoQueryPaList(self):
        q = QueryPaList()

    def _intoAddPaList(self):
        i = AddPaList(self.id)

    def _intoAdmin(self):
        if self.admin:
            a = Admin()
        else:
            tkinter.messagebox.showerror('没有权限')

    def _intoAnamnesis(self):
        t = QueryAnamnesis()

    def _changeReg(self, event=''):
        self.root.destroy()
        L = Login()

    def _infomation_get(self):
        conn, cursor = dbTools()
        sql = "select doctor.id, doctor.name, type.name, type.isadmin from doctor, type where doctor.id={0} and doctor.belong=type.id".format(
            self.id)
        cursor.execute(sql)
        result = cursor.fetchone()
        self.label_information['text'] = '欢迎您,{0}{1}'.format(
            result[1], result[2])
        self.admin = result[3]
        self.name = result[1]
        # 关闭游标
        cursor.close()
        # 关闭连接
        conn.close()

    def _gui_arrang(self):
        self.root.config(menu=self.main_menu)
        self.record_patient_button.place(x=20, y=40)
        self.query_patient_button.place(x=120, y=40)
        self.query_pa_list_button.place(x=20, y=100)
        self.add_pa_list_button.place(x=120, y=100)
        self.anamnesis_button.place(x=20, y=160)
        self.admin_button.place(x=120, y=160)
        self.label_information.place(x=50, y=10)


class RecordPatient(object):
    '''
    病人登记
    '''
    def __init__(self):
        # 创建主窗口,用于容纳其它组件
        self.root = tkinter.Tk()
        # 给主窗口设置标题内容
        self.root.title("病人登记")
        self.root.geometry('300x250')

        # 性别下拉框
        self.cmb = ttk.Combobox(self.root, width=10)
        self.cmb['values'] = ('M', 'F')
        self.cmb.current(0)

        self.name_label = tkinter.Label(self.root, text='姓名: ')

        self.birthdate_label = tkinter.Label(self.root,
                                             text='出生日期: \n(yyyy-mm-dd)')

        self.sex_label = tkinter.Label(self.root, text='性别: ')

        self.input_name = tkinter.Entry(self.root, width=12)

        self.input_birthdate = tkinter.Entry(self.root, width=12)

        self.okk_button = tkinter.Button(self.root,
                                         text="登记",
                                         width=10,
                                         command=self._confirm)

        self._gui_arrang()

    def _gui_arrang(self):
        self.name_label.place(x=20, y=20)
        self.birthdate_label.place(x=20, y=80)
        self.sex_label.place(x=20, y=140)

        self.input_name.place(x=160, y=20)
        self.input_birthdate.place(x=160, y=80)
        self.cmb.place(x=160, y=140)

        self.okk_button.place(x=90, y=180)

    def _confirm(self):
        name = self.input_name.get()
        birthdate = self.input_birthdate.get()
        sex = self.cmb.get()

        if not (len(name) and len(birthdate) and len(sex)):
            tkinter.messagebox.showerror(message='有内容为空')
            return

        conn, cursor = dbTools()
        sql = "INSERT INTO patient (name, birthdate, sex) VALUES ('{0}', '{1}', '{2}')".format(
            name, birthdate, sex)
        cursor.execute(sql)
        conn.commit()
        # sql = 'select max(id) from patient'
        # cursor.execute(sql)
        # result = cursor.fetchone()[0]
        conn.close()

        tkinter.messagebox.showinfo('注册成功', '注册成功!,病人姓名为{0}'.format(name))
        self.input_name.delete(0, 'end')


class QueryPatient(object):
    def __init__(self):
        # 创建主窗口,用于容纳其它组件
        self.root = tkinter.Tk()
        # 给主窗口设置标题内容
        self.root.title("病人查询")
        self.root.geometry('300x250')

        self.id_label = tkinter.Label(self.root, text='账号: ')

        self.input_id = tkinter.Entry(self.root, width=12)

        self.okk_button = tkinter.Button(self.root,
                                         text="查询",
                                         width=10,
                                         command=self._query)
        mat = "{:^20}\t{:^20}\t{:^20}"

        self.title = tkinter.Label(self.root,
                                   text=mat.format('姓名', '年龄', '性别'))
        self.content = tkinter.Label(self.root, text='')

        self._gui_arrang()

    def _gui_arrang(self):
        self.id_label.place(x=20, y=20)
        self.input_id.place(x=160, y=20)
        self.okk_button.place(x=90, y=60)

        self.title.place(x=0, y=100)
        self.content.place(x=0, y=130)

    def _query(self):
        pid = self.input_id.get()

        if not len(pid):
            return

        conn, cursor = dbTools()
        sql = "select NAME, AGE, SEX from bw where pid='{0}' ".format(
            pid)
        cursor.execute(sql)
        result = cursor.fetchone()
        conn.close()
        if not result:
            tkinter.messagebox.showerror(message='未查询到记录')
            self.content['text'] = ''
            return
        mat = "{:^20}\t{:^20}\t{:^20}"
        self.content['text'] = mat.format(str(result[0]), str(int(result[1])),
                                          str(result[2]))


class QueryPaList(object):
    def __init__(self):
        # 创建主窗口,用于容纳其它组件
        self.root = tkinter.Tk()
        # 给主窗口设置标题内容
        self.root.title("病例查询")
        self.root.geometry('300x250')

        self.id_label = tkinter.Label(self.root, text='病人PID: ')

        self.input_id = tkinter.Entry(self.root, width=12)

        self.okk_button = tkinter.Button(self.root,
                                         text="查询",
                                         width=10,
                                         command=self._query)

        self._gui_arrang()

    def _gui_arrang(self):
        self.id_label.place(x=20, y=20)
        self.input_id.place(x=160, y=20)
        self.okk_button.place(x=90, y=60)

    def _query(self):
        pid = self.input_id.get()

        if not len(pid):
            return

        conn, cursor = dbTools()
        sql = "select * from bg where pid='{0}' ".format(
            pid)
        cursor.execute(sql)
        result = cursor.fetchone()
        conn.close()
        if not result:
            tkinter.messagebox.showerror(message='未查询到记录')
        else:
            GetPalist(pid)


class GetPalist(object):
    def __init__(self, pid):
        # 创建主窗口,用于容纳其它组件
        self.root = tkinter.Tk()
        # 给主窗口设置标题内容
        self.root.title("PID {0}病例".format(pid))
        self.pid = pid

        self.scrollbar = tkinter.Scrollbar(self.root)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        title = [
            '1',
            '2',
            '3',
            '4',
            '5',
            '6',
            '7',
            '8',
            '9',
            '10'
        ]
        self.box = ttk.Treeview(self.root,
                                columns=title,
                                yscrollcommand=self.scrollbar.set,
                                show='headings')

        self.box.column('1', width=80, anchor='center')
        self.box.column('2', width=80, anchor='center')
        self.box.column('3', width=40, anchor='center')
        self.box.column('4', width=135, anchor='center')
        self.box.column('5', width=80, anchor='center')
        self.box.column('6', width=80, anchor='center')
        self.box.column('7', width=80, anchor='center')
        self.box.column('8', width=80, anchor='center')
        self.box.column('9', width=200, anchor='center')
        self.box.column('10', width=200, anchor='center')

        self.box.heading('1', text='病人账号')
        self.box.heading('2', text='病人姓名')
        self.box.heading('3', text='性别')
        self.box.heading('4', text='身份证号')
        self.box.heading('5', text='入院类型')
        self.box.heading('6', text='科室')
        self.box.heading('7', text='已付金额')
        self.box.heading('8', text='检查类型')
        self.box.heading('9', text='检查部位')
        self.box.heading('10', text='具体部位')
        self._get()
        self.scrollbar.config(command=self.box.yview)
        self.box.pack()

    def _get(self):
        conn, cursor = dbTools()
        sql = "select PID, NAME, SEX, SFZ, PTYPE, SQKS, PRICE, LX, JCBW, BWBW from bw where pid='{0}'".format(
            self.pid)
        cursor.execute(sql)
        results = cursor.fetchall()
        if results == None:
            tkinter.messagebox.showerror(message='未查询到记录')
            self.root.destroy()

       
        for row in results:
            self.box.insert('', 'end', values=row)
        conn.close()
        cursor.close()


class AddPaList(object):
    def __init__(self, id):

        self.id = id

        # 创建主窗口,用于容纳其它组件
        self.root = tkinter.Tk()
        # 给主窗口设置标题内容
        self.root.title("新增病例")
        self.root.geometry('300x370')

        self.id_label0 = tkinter.Label(self.root, text='病人账号: ')
        self.input_id0 = tkinter.Entry(self.root, width=12)

        self.id_label1 = tkinter.Label(self.root, text='病人姓名: ')
        self.input_id1 = tkinter.Entry(self.root, width=12)

        self.id_label2 = tkinter.Label(self.root, text='病人性别: ')
        # 性别下拉框
        self.cmb = ttk.Combobox(self.root, width=9)
        self.cmb['values'] = ('M', 'F')
        self.cmb.current(0)

        self.id_label3 = tkinter.Label(self.root, text='身份证号: ')
        self.input_id3 = tkinter.Entry(self.root, width=12)

        self.id_label4 = tkinter.Label(self.root, text='入院类型: ')
        self.input_id4 = tkinter.Entry(self.root, width=12)

        self.id_label5 = tkinter.Label(self.root, text='科室: ')
        self.input_id5 = tkinter.Entry(self.root, width=12)

        self.id_label6 = tkinter.Label(self.root, text='已付金额: ')
        self.input_id6 = tkinter.Entry(self.root, width=12)

        self.id_label7 = tkinter.Label(self.root, text='检查类型: ')
        self.input_id7 = tkinter.Entry(self.root, width=12)

        self.id_label8 = tkinter.Label(self.root, text='检查部位: ')
        self.input_id8 = tkinter.Entry(self.root, width=12)

        self.id_label9 = tkinter.Label(self.root, text='具体部位: ')
        self.input_id9 = tkinter.Entry(self.root, width=12)

        self.okk_button = tkinter.Button(self.root,
                                         text="提交",
                                         width=10,
                                         command=self._query)

        self._gui_arrang()

    def _gui_arrang(self):
        self.id_label0.place(x=20, y=20)
        self.input_id0.place(x=160, y=20)

        self.id_label1.place(x=20, y=50)
        self.input_id1.place(x=160, y=50)

        self.id_label2.place(x=20, y=80)
        self.cmb.place(x=160, y=80)

        self.id_label3.place(x=20, y=110)
        self.input_id3.place(x=160, y=110)

        self.id_label4.place(x=20, y=140)
        self.input_id4.place(x=160, y=140)

        self.id_label5.place(x=20, y=170)
        self.input_id5.place(x=160, y=170)

        self.id_label6.place(x=20, y=200)
        self.input_id6.place(x=160, y=200)

        self.id_label7.place(x=20, y=230)
        self.input_id7.place(x=160, y=230)

        self.id_label8.place(x=20, y=260)
        self.input_id8.place(x=160, y=260)

        self.id_label9.place(x=20, y=290)
        self.input_id9.place(x=160, y=290)

        self.okk_button.place(x=90, y=340)

    def _query(self):
        PID = self.input_id0.get()
        NAME = self.input_id1.get()
        SEX = self.cmb.get()
        SFZ = self.input_id3.get()
        PTYPE = self.input_id4.get()
        SQKS = self.input_id5.get()
        PRICE = self.input_id6.get()
        LX = self.input_id7.get()
        JCBW = self.input_id8.get()
        BWBW = self.input_id9.get()



        if not (len(PID)):
            return

        conn, cursor = dbTools()
        # sql = "select * from bg where pid='{0}' ".format(pid)
        # cursor.execute(sql)
        # result = cursor.fetchone()
        # if not result:
        #     tkinter.messagebox.showerror(message='未查询到此病人')
        #     self.content['text'] = ''
        #     return
        sql = "select doctor.name from doctor where doctor.id={0}".format(self.id)
        cursor.execute(sql)
        name = cursor.fetchone()
        sql = "INSERT INTO bw (PID, NAME, SEX, SFZ, PTYPE, SQYS, SQKS, PRICE, LX, JCBW, BWBW) " \
              "VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}')".format(
            PID, NAME, SEX, SFZ, PTYPE, name[0], SQKS, PRICE, LX, JCBW, BWBW)
        cursor.execute(sql)
        conn.commit()
        conn.close()
        tkinter.messagebox.showinfo('成功', '插入成功')


class QueryAnamnesis(object):
    def __init__(self):
        # 创建主窗口,用于容纳其它组件
        self.root = tkinter.Tk()
        # 给主窗口设置标题内容
        self.root.title("既往病史")
        self.root.geometry('400x350')

        self.id_label = tkinter.Label(self.root, text='病人PID: ')

        self.input_id = tkinter.Entry(self.root, width=12)

        self.okk_button = tkinter.Button(self.root,
                                         text="查询",
                                         width=10,
                                         command=self._query)

        self._gui_arrang()

    def _gui_arrang(self):
        self.id_label.place(x=20, y=20)
        self.input_id.place(x=160, y=20)
        self.okk_button.place(x=90, y=60)

    def _query(self):
        pid = self.input_id.get()

        if not len(pid):
            return

        conn, cursor = dbTools()
        sql = "select * from bw where pid='{0}' ".format(
            pid)
        cursor.execute(sql)
        result = cursor.fetchone()
        conn.close()
        if not result:
            tkinter.messagebox.showerror(message='未查询到记录')
        else:
            GetAnamnesis(pid)

class GetAnamnesis(object):
    def __init__(self, pid):
        # 创建主窗口,用于容纳其它组件
        self.root = tkinter.Tk()
        # 给主窗口设置标题内容
        self.root.title("PID {0}病史".format(pid))
        self.pid = pid

        self.scrollbar = tkinter.Scrollbar(self.root)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        title = [
            '1',
            '2',
            '3',
        ]
        self.box = ttk.Treeview(self.root,
                                columns=title,
                                yscrollcommand=self.scrollbar.set,
                                show='headings')

        self.box.column('1', width=200, anchor='center')
        self.box.column('2', width=80, anchor='center')
        self.box.column('3', width=120, anchor='center')

        self.box.heading('1', text='递交时间')
        self.box.heading('2', text='部门')
        self.box.heading('3', text='部位')
        self._get()
        self.scrollbar.config(command=self.box.yview)
        self.box.pack()

    def _get(self):
        conn, cursor = dbTools()
        sql = "select DJSJ, SQKS, BWBW from bw where pid='{0}' order by KDRQ".format(
            self.pid)
        cursor.execute(sql)
        results = cursor.fetchall()
        if results == None:
            tkinter.messagebox.showerror(message='未查询到记录')
            self.root.destroy()


        for row in results:
            self.box.insert('', 'end', values=row)
            conn.close()
            cursor.close()


class Admin(object):
    def __init__(self):
        # 创建主窗口,用于容纳其它组件
        self.root = tkinter.Tk()
        # 给主窗口设置标题内容
        self.root.title("管理中心")
        self.root.geometry('230x220')

        self.id = id

        # 医生管理 f
        self.doc_button = tkinter.Button(self.root,
                                         text="医生管理",
                                         width=10,
                                         command=self._intoDoctorQuery)
        # 药品管理 f
        self.med_button = tkinter.Button(self.root,
                                         text="药品管理",
                                         width=10,
                                         command=self._intoMedicine)
        # 医生一览 f
        self.all_doc = tkinter.Button(self.root,
                                      text="医生一览",
                                      width=10,
                                      command=self._intoalldoc)

        # 药品一览 f
        self.all_med = tkinter.Button(self.root,
                                      text="药品一览",
                                      width=10,
                                      command=self._intoallmed)

        self._gui_arrang()

    def _intoDoctorQuery(self):
        d = doctorAdmin()

    def _intoMedicine(self):
        m = medicineAdmin()

    def _intoalldoc(self):
        a = AllDoctor()

    def _intoallmed(self):
        a = AllMedicine()

    def _gui_arrang(self):
        self.doc_button.place(x=20, y=40)
        self.med_button.place(x=120, y=40)
        self.all_doc.place(x=20, y=100)
        self.all_med.place(x=120, y=100)


class doctorAdmin(object):
    def __init__(self):
        # 创建主窗口,用于容纳其它组件
        self.root = tkinter.Tk()
        # 给主窗口设置标题内容
        self.root.title("医生管理")
        self.root.geometry('500x300')

        self.account = tkinter.Label(self.root, text='id')
        self.name = tkinter.Label(self.root, text='姓名')
        self.birthday = tkinter.Label(self.root, text='生日')
        self.pwd = tkinter.Label(self.root, text='密码')
        self.belong = tkinter.Label(self.root, text='所属部门id')
        self.sex = tkinter.Label(self.root, text='性别')

        self.input_account = tkinter.Entry(self.root, width=10)
        self.input_name = tkinter.Entry(self.root, width=10)
        self.input_birthday = tkinter.Entry(self.root, width=10)
        self.input_pwd = tkinter.Entry(self.root, width=10)
        self.input_belong = tkinter.Entry(self.root, width=10)
        self.input_sex = tkinter.Entry(self.root, width=10)

        self.query = tkinter.Button(self.root,
                                    text="查询",
                                    width=10,
                                    command=self._Query)
        create_ToolTip(self.query, '输入医生id以查询')

        self.update = tkinter.Button(self.root,
                                     text="更新",
                                     width=10,
                                     command=self._Update)

        self.insert = tkinter.Button(self.root,
                                     text="插入",
                                     width=10,
                                     command=self._Insert)

        self.delete = tkinter.Button(self.root,
                                     text="删除",
                                     width=10,
                                     command=self._Delete)
        create_ToolTip(self.delete, '输入医生id以删除')

        self._gui_arrang()

    def _gui_arrang(self):
        self.account.place(x=20, y=0)
        self.name.place(x=200, y=0)
        self.birthday.place(x=380, y=0)
        self.pwd.place(x=20, y=100)
        self.belong.place(x=200, y=100)
        self.sex.place(x=380, y=100)

        self.input_account.place(x=20, y=50)
        self.input_name.place(x=200, y=50)
        self.input_birthday.place(x=380, y=50)
        self.input_pwd.place(x=20, y=150)
        self.input_belong.place(x=200, y=150)
        self.input_sex.place(x=380, y=150)

        self.query.place(x=40, y=200)
        self.update.place(x=140, y=200)
        self.insert.place(x=240, y=200)
        self.delete.place(x=340, y=200)

    def _Query(self):
        id = self.input_account.get()
        if not len(id):
            return

        conn, cursor = dbTools()
        sql = "select id, name, birthdate, pwd, belong, sex from doctor where id={0}".format(
            id)
        cursor.execute(sql)
        result = cursor.fetchone()
        conn.close()
        if result == None:
            tkinter.messagebox.showerror('无此记录', '无此记录')
            return

        v = tkinter.StringVar(self.root)
        v.set(result[1])
        self.input_name['textvariable'] = v

        v = tkinter.StringVar(self.root)
        v.set(result[2])
        self.input_birthday['textvariable'] = v

        v = tkinter.StringVar(self.root)
        v.set(result[3])
        self.input_pwd['textvariable'] = v

        v = tkinter.StringVar(self.root)
        v.set(result[4])
        self.input_belong['textvariable'] = v

        v = tkinter.StringVar(self.root)
        v.set(result[5])
        self.input_sex['textvariable'] = v

    def _Delete(self):
        id = self.input_account.get()
        if not len(id):
            return

        conn, cursor = dbTools()

        sql = "select * from doctor where id={0}".format(id)
        cursor.execute(sql)
        result = cursor.fetchone()

        if result == None:
            conn.close()
            tkinter.messagebox.showerror('无此记录', '无此记录')
            return

        sql = "delete from doctor where id={0}".format(id)
        cursor.execute(sql)
        conn.commit()
        conn.close()
        tkinter.messagebox.showinfo('成功', '删除成功')
        self.input_account.delete(0, 'end')

    def _Insert(self):
        id = self.input_account.get()
        name = self.input_name.get()
        birthday = self.input_birthday.get()
        pwd = self.input_pwd.get()
        belong = self.input_belong.get()
        sex = self.input_sex.get()
        if not (len(id) and len(name) and len(birthday) and len(pwd) and len(belong) and len(sex)):
            tkinter.messagebox.showerror('有内容为空', '不能有空缺选项！')

        conn, cursor = dbTools()
        sql = "INSERT INTO doctor (id, name, birthdate, pwd, belong, sex) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(
            id, name, birthday, pwd, belong, sex)
        cursor.execute(sql)
        conn.commit()
        conn.close()
        tkinter.messagebox.showinfo('成功', '插入成功')

    def _Update(self):
        id = self.input_account.get()
        name = self.input_name.get()
        birthday = self.input_birthday.get()
        pwd = self.input_pwd.get()
        belong = self.input_belong.get()
        sex = self.input_sex.get()
        if not (len(name) and len(birthday) and len(pwd) and len(belong) and len(sex) and len(id)):
            tkinter.messagebox.showerror('有内容为空', '不能有空缺选项！')

        conn, cursor = dbTools()
        sql = "select * from doctor where id={0}".format(id)
        cursor.execute(sql)
        result = cursor.fetchone()

        if result == None:
            conn.close()
            tkinter.messagebox.showerror('无此记录', '无此记录')
            return
        sql = "update doctor set name='{0}', birthdate='{1}', pwd='{2}', belong='{3}', sex='{4}' where id={5}".format(
            name, birthday, pwd, belong, sex, id)
        cursor.execute(sql)
        conn.commit()
        conn.close()
        tkinter.messagebox.showinfo('成功', '更新成功')


class AllMedicine(object):
    def __init__(self):
        # 创建主窗口,用于容纳其它组件
        self.root = tkinter.Tk()
        # 给主窗口设置标题内容
        self.root.title("库存和商品一览")
        # self.root.geometry('400x200')

        self.scrollbar = tkinter.Scrollbar(self.root)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        title = [
            '1',
            '2',
            '3',
        ]
        self.box = ttk.Treeview(self.root,
                                columns=title,
                                yscrollcommand=self.scrollbar.set,
                                show='headings')

        self.box.column('1', width=100, anchor='center')
        self.box.column('2', width=100, anchor='center')
        self.box.column('3', width=100, anchor='center')

        self.box.heading('1', text='编号')
        self.box.heading('2', text='药名')
        self.box.heading('3', text='售价')

        self._get()
        self.scrollbar.config(command=self.box.yview)
        self.box.pack()

    def _get(self):
        conn, cursor = dbTools()
        sql = "select * from medicine"
        cursor.execute(sql)
        results = cursor.fetchall()
        if results == None:
            return
        
        for row in results:
            self.box.insert('', 'end', values=row)
        conn.close()
        cursor.close()


class AllDoctor(object):
    def __init__(self):
        # 创建主窗口,用于容纳其它组件
        self.root = tkinter.Tk()
        # 给主窗口设置标题内容
        self.root.title("医生一览")
        # self.root.geometry('400x200')

        self.scrollbar = tkinter.Scrollbar(self.root)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        title = ['1', '2', '3', '4', '5', '6']
        self.box = ttk.Treeview(self.root,
                                columns=title,
                                yscrollcommand=self.scrollbar.set,
                                show='headings')

        self.box.column('1', width=100, anchor='center')
        self.box.column('2', width=100, anchor='center')
        self.box.column('3', width=100, anchor='center')
        self.box.column('4', width=100, anchor='center')
        self.box.column('5', width=100, anchor='center')
        self.box.column('6', width=100, anchor='center')

        self.box.heading('1', text='帐户')
        self.box.heading('2', text='姓名')
        self.box.heading('3', text='生日')
        self.box.heading('4', text='密码')
        self.box.heading('5', text='部门')
        self.box.heading('6', text='性别')

        self._get()
        self.scrollbar.config(command=self.box.yview)
        self.box.pack()

    def _get(self):
        conn, cursor = dbTools()
        sql = "select * from doctor "
        cursor.execute(sql)
        results = cursor.fetchall()
        if results == None:
            return
        for row in results:
            self.box.insert('', 'end', values=row)
        conn.close()
        cursor.close()


class medicineAdmin(object):
    def __init__(self):
        # 创建主窗口,用于容纳其它组件
        self.root = tkinter.Tk()
        # 给主窗口设置标题内容
        self.root.title("药品管理")
        self.root.geometry('500x200')

        self.id = tkinter.Label(self.root, text='药品id')
        self.name = tkinter.Label(self.root, text='名称')
        self.price = tkinter.Label(self.root, text='价格')

        self.input_id = tkinter.Entry(self.root, width=10)
        self.input_name = tkinter.Entry(self.root, width=10)
        self.input_price = tkinter.Entry(self.root, width=10)

        self.query = tkinter.Button(self.root,
                                    text="查询",
                                    width=10,
                                    command=self._Query)
        create_ToolTip(self.query, '输入药品名称以查询')

        self.update = tkinter.Button(self.root,
                                     text="更新",
                                     width=10,
                                     command=self._Update)

        self.insert = tkinter.Button(self.root,
                                     text="插入",
                                     width=10,
                                     command=self._Insert)

        self.delete = tkinter.Button(self.root,
                                     text="删除",
                                     width=10,
                                     command=self._Delete)
        create_ToolTip(self.delete, '输入药品id以删除')

        self._gui_arrang()

    def _gui_arrang(self):
        self.id.place(x=20, y=0)
        self.name.place(x=200, y=0)
        self.price.place(x=380, y=0)

        self.input_id.place(x=20, y=50)
        self.input_name.place(x=200, y=50)
        self.input_price.place(x=380, y=50)

        self.query.place(x=40, y=100)
        self.update.place(x=140, y=100)
        self.insert.place(x=240, y=100)
        self.delete.place(x=340, y=100)

    def _Query(self):
        name = self.input_name.get()
        if not len(name):
            return

        conn, cursor = dbTools()
        sql = "select id, name, price from medicine where name='{0}'".format(name)
        cursor.execute(sql)
        result = cursor.fetchone()
        conn.close()
        if result == None:
            tkinter.messagebox.showerror('无此记录', '无此记录')
            return

        v=tkinter.StringVar(self.root)
        v.set(result[0])
        self.input_id['textvariable'] = v

        v=tkinter.StringVar(self.root)
        v.set(result[2])
        self.input_price['textvariable'] =v


    def _Delete(self):
        id = self.input_id.get()
        if not len(id):
            return

        conn, cursor = dbTools()

        sql = "select * from medicine where id={0}".format(id)
        cursor.execute(sql)
        result = cursor.fetchone()

        if result == None:
            conn.close()
            tkinter.messagebox.showerror('无此记录', '无此记录')
            return

        sql = "delete from medicine where id={0}".format(id)
        cursor.execute(sql)
        conn.commit()
        conn.close()
        tkinter.messagebox.showinfo('成功', '删除成功')
        self.input_id.delete(0, 'end')

    def _Insert(self):
        name = self.input_name.get()
        price = self.input_price.get()

        if not (len(name) and len(price)):
            tkinter.messagebox.showerror('name或price内容为空', '不能有空缺选项！')
            return

        conn, cursor = dbTools()
        sql = "INSERT INTO medicine (name, price) VALUES ('{0}', {1})".format(name, price)
        cursor.execute(sql)
        conn.commit()
        conn.close()
        tkinter.messagebox.showinfo('成功', '插入成功')

    def _Update(self):
        id = self.input_id.get()
        name = self.input_name.get()
        price = self.input_price.get()

        if not (len(name) and len(price) and len(id)):
            tkinter.messagebox.showerror('内容为空', '内容为空')
            return

        conn, cursor = dbTools()
        sql = "select * from medicine where id={0}".format(id)
        cursor.execute(sql)
        result = cursor.fetchone()

        if result == None:
            conn.close()
            tkinter.messagebox.showerror('无此记录', '无此记录')
            return
        sql = '''update medicine set name='{0}', price='{1}' where id={2}'''.format(
            name, price, id)
        cursor.execute(sql)
        conn.commit()
        conn.close()
        tkinter.messagebox.showinfo('成功', '更新成功')


if __name__ == '__main__':
    # 初始化对象
    L = Login()
    # 主程序执行
    # AllDoctor()
    tkinter.mainloop()
