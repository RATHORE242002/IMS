from tkinter import*
from PIL import ImageTk
from tkinter import messagebox
import sqlite3
import os
import email_pass
import smtplib # pip install smtplib
import time
class login_System:
    def __init__(self, root):
        self.root=root
        self.root.title("Login Page")
        self.root.geometry("2500x1200+0+0")
        self.root.config(bg="#fafafa")

        self.otp=''
        #===Images=====#
        self.phone_image=ImageTk.PhotoImage(file="images/phone.png")
        self.lbl_phone_image=Label(self.root,image=self.phone_image,bd=0).place(x=300,y=50)
        #===Login_Frame====#0
        self.employee_id=StringVar()
        self.password=StringVar()

        login_frame=Frame(self.root,bd=4,relief=RIDGE, bg="white")
        login_frame.place(x=760,y=150,width=350,height=435)

        title=Label(login_frame,text="Login Here", font=("Arial",30,"bold"),bg="white").place(x=0,y=30,relwidth=1)

        lbl_user=Label(login_frame, text="Employee ID",font=("Andalus",15),bg="white",fg="#767171").place(x=50,y=100)
        txt_username=Entry(login_frame,textvariable=self.employee_id,font=("times new roman",15),bg="#ECECEC").place(x=50,y=140,width=250)

        lbl_pass=Label(login_frame, text="Password",font=("Andalus",15),bg="white",fg="#767171").place(x=50,y=180)
        txt_pass=Entry(login_frame,textvariable=self.password,show="*",font=("times new roman",15),bg="#ECECEC").place(x=50,y=220,width=250)

        btn_login=Button(login_frame,command=self.login,text="Log in", font=("Arial Rounded MT Bold",15),bg="#00B0F0" ,activebackground="#00B0F0",fg="white", activeforeground="white",cursor="hand2").place(x=50,y=270,width=250,height=35)

        hr=Label(login_frame,bg="lightgray").place(x=50,y=337,width=250,height=2)
        or_=Label(login_frame,text="OR",bg="white",fg="lightgray", font=("times new roman",15,"bold")).place(x=150,y=325 )

        btn_forget=Button(login_frame,text="Forget Password?",command=self.forget_window, font=("times new roman",13),bg="white",fg="#00759E",bd=0, activebackground="white", activeforeground="#00759E").place(x=100,y=370)

        #======Frame2========
        register_frame=Frame(self.root,bd=4,relief=RIDGE, bg="white")
        register_frame.place(x=760,y=590,width=350,height=70)


        lbl_reg=Label(register_frame,text="THIS IS OUR PYTHON PROJECT", font=("times new roman",13),bg="white").place(x=0,y=20,relwidth=1)

        #=============Animation Images==============
        self.im1=ImageTk.PhotoImage(file="Images/im1.png")
        self.im2=ImageTk.PhotoImage(file="Images/im2.png")
        self.im3=ImageTk.PhotoImage(file="Images/im3.png")

        self.lbl_change_image=Label(self.root,bg="white")
        self.lbl_change_image.place(x=509,y=182,width=232,height=459)

        self.animate()
        

    def animate(self):
        self.im=self.im1
        self.im1=self.im2
        self.im2=self.im3
        self.im3=self.im
        self.lbl_change_image.config(image=self.im)
        self.lbl_change_image.after(2000,self.animate)


    def login(self):
        con=sqlite3.connect(database=r'rathore.db')
        cur=con.cursor()
        try:
            if self.employee_id.get()=="" or self.password.get()=="":
                messagebox.showerror("Error","All fields are reqiured", parent=self.root)
            else:
                cur.execute("select utype from employee where eid=? AND pass=?",(self.employee_id.get(),self.password.get()))
                user=cur.fetchone()
                if user==None:
                    messagebox.showerror("Error","Invalid USERNAME/PASSWORD", parent=self.root)
                else:
                    if user[0]=="Admin":
                        self.root.destroy()
                        os.system(" python dashboard.py")
                    else:
                        self.root.destroy()
                        os.system("python billing.py")

        
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)    


    def forget_window(self):
        con=sqlite3.connect(database=r'rathore.db')
        cur=con.cursor()
        try:
            if self.employee_id.get()=="":
                messagebox.showerror("Error", "Employee ID must be required", parent=self.root)
            else:
                cur.execute("select email from employee where eid=?",(self.employee_id.get(),))
                email=cur.fetchone()
                if email==None:
                    messagebox.showerror("Error","Invalid Employee Id, try Again", parent=self.root)
                else:
                   #======forget window===========
                   self.var_otp=StringVar()
                   self.var_new_pass=StringVar()
                   self.var_conf_pass=StringVar()
                   #call send_email_function()
                   chk=self.send_email(email[0])
                   if chk!='s':
                        messagebox.showerror("Error","Connection Error ,try again",parent=self.root)
                   else:
                    self.forget_win=Toplevel(self.root)
                    self.forget_win.title("Reset Password")
                    self.forget_win.geometry('400x350+500+100')
                    self.forget_win.focus_force()

                    title=Label(self.forget_win,text='Reset Password', font=('goudy old style',15,'bold'),bg="#3f51b5",fg="white").pack(side=TOP,fill=X)
                    lbl_reset=Label(self.forget_win, text="Enter OTP Sent on Registered Email", font=("times new roman",15)).place(x=20,y=60)
                    txt_reset=Entry(self.forget_win, textvariable=self.var_otp,font=("times new roman",15),bg='lightyellow').place(x=20,y=100, width=250, height=30)
                    self.btn_reset=Button(self.forget_win,text="SUBMIT",command=self.validate_otp,font=("times new roman",15),bg='lightblue')
                    self.btn_reset.place(x=280,y=100, width=100, height=30)
                    
                    lbl_new_pass=Label(self.forget_win,text='New Password', font=("times new roman",15)).place(x=20,y=160)
                    txt_new_pass=Entry(self.forget_win, textvariable=self.var_new_pass,font=("times new roman",15),bg='lightyellow').place(x=20,y=190, width=250, height=30)
                    
                    lbl_c_pass=Label(self.forget_win,text='Confirm Password', font=("times new roman",15)).place(x=20,y=225)
                    txt_c_pass=Entry(self.forget_win, textvariable=self.var_conf_pass,font=("times new roman",15),bg='lightyellow').place(x=20,y=255, width=250, height=30)

                    self.btn_update=Button(self.forget_win,text="Update",command=self.update_password,state=DISABLED,font=("times new roman",15),bg='lightblue')
                    self.btn_update.place(x=150,y=300, width=100, height=30)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    
    def update_password(self):
        if self.var_new_pass.get()=="" or self.var_conf_pass.get()=="":
            messagebox.showerror("Error","Password is required", parent=self.forget_win)
        elif self.var_new_pass.get()!=self.var_conf_pass.get():
            messagebox.showerror("Error","Password & confirmed password should be Same", parent=self.forget_win)
        else:
            con=sqlite3.connect(database=r'rathore.db')
            cur=con.cursor()
            try:
                cur.execute("Update employee SET pass=? where eid=?",(self.var_new_pass.get(),self.employee_id.get()))
                con.commit()
                messagebox.showinfo("Sucess", "Password Updated Sucessfully", parent=self.forget_win)
                self.forget_win.destroy()
            except Exception as ex:
                messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

            
    def validate_otp(self):
        if int(self.otp)==int(self.var_otp.get()):
            self.btn_update.config(state=NORMAL)
            self.btn_reset.config(state=DISABLED)
        else:
           messagebox.showerror("Error","Invalid OTP, Try again", parent=self.forget_win)


    def send_email(self,to_):
        s=smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        email_=email_pass.email_
        pass_=email_pass.pass_

        s.login(email_,pass_)
        self.otp=int(time.strftime("%H%S%M"))+int(time.strftime("%S"))
        print(self.otp)
        
        subj='IMS-Reset Password OTP'
        msg=f'Dear Sir/Madam, \n\n Your Reset OTP is {str(self.otp)}.\n\nWith Regards, \n RATHORE Team'
        msg="Subject:{}\n\n{}".format(subj,msg)
        s.sendmail(email_,to_,msg)
        chk=s.ehlo()
        if chk[0]==250:
            return 's'
        else:
            return 'f'
    

root=Tk()
obj=login_System(root)
root.mainloop() 