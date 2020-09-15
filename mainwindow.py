import tkinter as tk
from tkinter import filedialog,messagebox,ttk
from ocrprocesser import Ocr_model


ocr_model=Ocr_model("","","",[])
img_type_dict=("手写体","印刷体","身份证","名片","表格","整题")

def get_files():
    files = filedialog.askopenfilenames(filetypes=[('img files', '.png'),('img files', '.jpg')])
    ocr_model.img_paths=files
    if files:
        for file in files:
            text1.insert(tk.END, file + '\n')
            text1.update()
    else:
        print('你没有选择任何文件')

def get_img_type(*args):
    select=combox.get()
    ocr_model.img_type=img_type_dict.index(select)
def ocr_files():
    if ocr_model.img_paths:
        ocr_result=ocr_model.ocr_files()
        text_result.insert(tk.END,ocr_result)
        #print(ocr_model.img_type)
        #tk.messagebox.showinfo("提示","搞定")
    else :
        tk.messagebox.showinfo("提示","无文件")

def clean_text():
    text_result.delete('1.0','end')
    text1.delete('1.0','end')

root=tk.Tk()
root.title("netease youdao ocr test")
frm = tk.Frame(root)
frm.grid(padx='100', pady='100')

btn_get_file = tk.Button(frm, text='选择待识别图片', command=get_files)
btn_get_file.grid(row=0, column=0,  padx='10', pady='20')
text1 = tk.Text(frm, width='40', height='5')
text1.grid(row=0, column=1)

combox=ttk.Combobox(frm,textvariable=tk.StringVar(),width=38)
combox["value"]=img_type_dict
combox.current(0)
combox.bind("<<ComboboxSelected>>",get_img_type)
combox.grid(row=1,column=1)

label=tk.Label(frm,text="识别结果：")
label.grid(row=2,column=0)
text_result=tk.Text(frm,width='40',height='20')
text_result.grid(row=2,column=1)

btn_sure=tk.Button(frm,text="开始识别",command=ocr_files)
btn_sure.grid(row=3,column=1)
btn_clean=tk.Button(frm,text="清空",command=clean_text)
btn_clean.grid(row=3,column=2)

root.mainloop()
