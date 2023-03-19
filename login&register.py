import tkinter as tk
import tkinter.messagebox as messagebox
import pymysql
from ttkbootstrap import Style
'''
在本次更新的代码中，添加了一个名为“注册/找回账号”的按钮，该按钮打开一个新窗口以进行帐户注册或恢复。
当用户单击该按钮时，登录窗口将被隐藏，注册窗口将显示。注册窗口有三个输入字段，用于用户名、密码和密码确认。
如果两个密码字段不匹配或用户名已存在于数据库中，则会显示适当的错误消息。如果注册成功，则会显示成功消息，关闭注册窗口，然后再次显示登录窗口。
注册窗口还有一个“返回”按钮，允许用户返回登录窗口。
'''
class LoginWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("登陆")
        self.master.geometry("300x200")

        self.style = Style(theme="superhero")
        self.style.configure("TLabel", font=("Helvetica", 12))
        self.style.configure("TEntry", font=("Helvetica", 12))
        self.style.configure("TButton", font=("Helvetica", 12))

        self.create_widgets()

    def create_widgets(self):
        self.username_label = tk.Label(self.master, text="账号：")
        self.username_label.grid(row=0, column=0, padx=10, pady=10)

        self.password_label = tk.Label(self.master, text="密码：")
        self.password_label.grid(row=1, column=0, padx=10, pady=10)

        self.username_entry = tk.Entry(self.master)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        self.password_entry = tk.Entry(self.master, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        # Bind "Return" key to login button
        self.master.bind('<Return>', lambda event: self.login())

        self.login_button = tk.Button(self.master, text="登陆账号", command=self.login)
        self.login_button.grid(row=2, column=0, padx=10, pady=10)

        self.register_button = tk.Button(self.master, text="注册账号", command=self.show_register_window)
        self.register_button.grid(row=2, column=1, padx=10, pady=10)



    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            db = pymysql.connect(host="localhost", user="root", password="qwe1234567", database="db01")
            with db.cursor() as cursor:
                sql = "SELECT * FROM tUser WHERE user_account=%s AND password=%s"
                cursor.execute(sql, (username, password))
                result = cursor.fetchone()

            if result:
                self.master.destroy()
                # main()
            else:
                messagebox.showerror("错误", "账号或密码错误")

        except Exception as e:
            messagebox.showerror("错误", f"数据库错误: {e}")
        finally:
            if db:
                db.close()

    def show_register_window(self):
        self.master.withdraw()

        register_window = tk.Toplevel()
        register_window.title("注册/找回账号")
        register_window.geometry("300x200")

        fields = ["账号", "密码", "确认密码"]
        entries = []

        for i, field in enumerate(fields):
            label = tk.Label(register_window, text=f"{field}：")
            label.grid(row=i, column=0, padx=10, pady=10)

            entry = tk.Entry(register_window, show="*")
            entry.grid(row=i, column=1, padx=10, pady=10)

            entries.append(entry)


        register_button = tk.Button(register_window, text="注册", command=lambda: self.register(entries, register_window))
        register_button.grid(row=len(fields), column=0, padx=10, pady=10)

        back_button = tk.Button(register_window, text="返回", command=lambda: self.back_to_login(register_window))
        back_button.grid(row=len(fields), column=1, padx=10, pady=10)

        # center the window
        register_window.update_idletasks()
        width = register_window.winfo_width()
        height = register_window.winfo_height()
        x = (register_window.winfo_screenwidth() // 2) - (width // 2)
        y = (register_window.winfo_screenheight() // 2) - (height // 2)
        register_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def register(self, entries, register_window):
        username = entries[0].get()
        password = entries[1].get()
        confirm_password = entries[2].get()

        if password != confirm_password:
            messagebox.showerror("错误", "两次输入的密码不相同")
            return

        if not username:
            messagebox.showerror("错误","账号不能为空")
            return

        if not password:
            messagebox.showerror("错误","密码不能为空")
            return

        try:
            db = pymysql.connect(host="localhost", user="root", password="qwe1234567", database="db01")
            with db.cursor() as cursor:
                sql = "SELECT * FROM tUser WHERE user_account=%s"
                cursor.execute(sql, (username,))
                result = cursor.fetchone()

            if result:
                messagebox.showerror("错误", "该账号已存在")
            else:
                with db.cursor() as cursor:
                    sql = "INSERT INTO tUser (user_account, password) VALUES (%s, %s)"
                    cursor.execute(sql, (username, password))
                    db.commit()
                messagebox.showinfo("成功", "注册成功")
                register_window.destroy()
                self.master.deiconify()

        except Exception as e:
            messagebox.showerror("错误", f"数据库错误: {e}")
        finally:
            if db:
                db.close()

    def back_to_login(self, register_window):
        register_window.destroy()
        self.master.deiconify()



def main():
    root = tk.Tk()
    app = LoginWindow(root)
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    root.mainloop()

if __name__ == '__main__':
    main()