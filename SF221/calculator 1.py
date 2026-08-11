import tkinter as tk

#ฟังก์ชันสำหรับรับค่าเมื่อกดปุ่มตัวเลขหรือเครื่องหมาย
def btn_click(item):
    global expression
    expression = expression + str(item)
    input_text.set(expression)

#ฟังก์ชันสำหรับปุ่ม C (Clear) ล้างหน้าจอ
def btn_clear():
    global expression
    expression = ""
    input_text.set("")

#ฟังก์ชันสำหรับคำนวณผลลัพธ์เมื่อกดปุ่ม =
def btn_equal():
    global expression
    try:
        # ใช้ eval() เพื่อคำนวณผลลัพธ์ทางคณิตศาสตร์จากข้อความ
        result = str(eval(expression))
        input_text.set(result)
        expression = result
    except ZeroDivisionError:
        input_text.set("Error: หารด้วยศูนย์ไม่ได้")
        expression = ""
    except Exception:
        input_text.set("Error")
        expression = ""

#สร้างหน้าต่างโปรแกรมหลัก
root = tk.Tk()
root.title("เครื่องคิดเลข (Calculator)")
root.geometry("320x420")
root.resizable(0, 0) # ป้องกันการขยายหน้าต่าง

expression = ""
input_text = tk.StringVar()

#สร้างพื้นที่สำหรับหน้าจอแสดงผล
input_frame = tk.Frame(root, width=512, height=216, bd=0, highlightbackground="black", highlightcolor="black", highlightthickness=1)
input_frame.pack(side=tk.TOP)

input_field = tk.Entry(input_frame, font=('arial', 18, 'bold'), textvariable=input_text, width=24, bg="#eee", bd=0, justify=tk.RIGHT)
input_field.grid(row=0, column=0)
input_field.pack(ipady=10) # เพิ่มความสูงให้กล่องข้อความ

#สร้างพื้นที่สำหรับปุ่มกด
btns_frame = tk.Frame(root, width=312, height=272.5, bg="grey")
btns_frame.pack()

#--- สร้างปุ่มต่างๆ ลงใน Grid ---
#แถวที่ 1: Clear และ หาร
tk.Button(btns_frame, text="C", fg="black", width=24, height=3, bd=0, bg="#ff9999", cursor="hand2", command=btn_clear).grid(row=0, column=0, columnspan=3, padx=1, pady=1)
tk.Button(btns_frame, text="/", fg="black", width=7, height=3, bd=0, bg="#eee", cursor="hand2", command=lambda: btn_click("/")).grid(row=0, column=3, padx=1, pady=1)
#แถวที่ 2: 7, 8, 9, คูณ
tk.Button(btns_frame, text="7", fg="black", width=7, height=3, bd=0, bg="#fff", cursor="hand2", command=lambda: btn_click(7)).grid(row=1, column=0, padx=1, pady=1)
tk.Button(btns_frame, text="8", fg="black", width=7, height=3, bd=0, bg="#fff", cursor="hand2", command=lambda: btn_click(8)).grid(row=1, column=1, padx=1, pady=1)
tk.Button(btns_frame, text="9", fg="black", width=7, height=3, bd=0, bg="#fff", cursor="hand2", command=lambda: btn_click(9)).grid(row=1, column=2, padx=1, pady=1)
tk.Button(btns_frame, text="", fg="black", width=7, height=3, bd=0, bg="#eee", cursor="hand2", command=lambda: btn_click("")).grid(row=1, column=3, padx=1, pady=1)

#แถวที่ 3: 4, 5, 6, ลบ
tk.Button(btns_frame, text="4", fg="black", width=7, height=3, bd=0, bg="#fff", cursor="hand2", command=lambda: btn_click(4)).grid(row=2, column=0, padx=1, pady=1)
tk.Button(btns_frame, text="5", fg="black", width=7, height=3, bd=0, bg="#fff", cursor="hand2", command=lambda: btn_click(5)).grid(row=2, column=1, padx=1, pady=1)
tk.Button(btns_frame, text="6", fg="black", width=7, height=3, bd=0, bg="#fff", cursor="hand2", command=lambda: btn_click(6)).grid(row=2, column=2, padx=1, pady=1)
tk.Button(btns_frame, text="-", fg="black", width=7, height=3, bd=0, bg="#eee", cursor="hand2", command=lambda: btn_click("-")).grid(row=2, column=3, padx=1, pady=1)
#แถวที่ 4: 1, 2, 3, บวก
tk.Button(btns_frame, text="1", fg="black", width=7, height=3, bd=0, bg="#fff", cursor="hand2", command=lambda: btn_click(1)).grid(row=3, column=0, padx=1, pady=1)
tk.Button(btns_frame, text="2", fg="black", width=7, height=3, bd=0, bg="#fff", cursor="hand2", command=lambda: btn_click(2)).grid(row=3, column=1, padx=1, pady=1)
tk.Button(btns_frame, text="3", fg="black", width=7, height=3, bd=0, bg="#fff", cursor="hand2", command=lambda: btn_click(3)).grid(row=3, column=2, padx=1, pady=1)
tk.Button(btns_frame, text="+", fg="black", width=7, height=3, bd=0, bg="#eee", cursor="hand2", command=lambda: btn_click("+")).grid(row=3, column=3, padx=1, pady=1)

#แถวที่ 5: 0, จุดทศนิยม, เท่ากับ
tk.Button(btns_frame, text="0", fg="black", width=16, height=3, bd=0, bg="#fff", cursor="hand2", command=lambda: btn_click(0)).grid(row=4, column=0, columnspan=2, padx=1, pady=1)
tk.Button(btns_frame, text=".", fg="black", width=7, height=3, bd=0, bg="#eee", cursor="hand2", command=lambda: btn_click(".")).grid(row=4, column=2, padx=1, pady=1)
tk.Button(btns_frame, text="=", fg="black", width=7, height=3, bd=0, bg="#b3ffb3", cursor="hand2", command=btn_equal).grid(row=4, column=3, padx=1, pady=1)

#เริ่มต้นการทำงานของโปรแกรม
root.mainloop()
