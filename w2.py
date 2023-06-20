import random
import time
import tkinter as tk
from tkinter import filedialog
from prettytable import PrettyTable
import string
from textblob import TextBlob,Word
import ttkbootstrap as ttk
import chardet


def find_word(sentence, str):
    blob=TextBlob(str)
    tag=blob.lower().tags
    if tag[0][1] in ['VBD','VBN','VBG','VBP','VBZ']:
        w=Word(tag[0][0]).lemmatize(tag[0][1])
    else:
        w = Word(tag[0][0]).lemmatize()
    result=[]
    for c,i in enumerate(sentence):
        word=i[0].lower()
        if word[0]==blob.words[0][0]:
            if i[1] in ['VBD','VBN','VBG','VBP','VBZ']:
                if Word(word).lemmatize(i[1])==w:
                    result.append(c)
            else:
                if Word(word).lemmatize()==w:
                    result.append(c)
    # 如果没有，都变成动词试一下
    if len(result) == 0:
        w = Word(tag[0][0]).lemmatize('v')
        for c, i in enumerate(sentence):
            word = i[0].lower()
            if word[0] == blob.words[0][0]:
                if Word(word).lemmatize('v') == w:
                    result.append(c)
    return result

def parse_sentence(sentence):
    # 初始化一个空列表，用来存放结果
    result = []
    result1=[]
    # 用空格分割字符串，得到一个单词列表
    words = sentence.split()
    # 遍历单词列表
    for i,word in enumerate(words):
        # 如果单词以大写字母开头，并且不是第一个单词，说明它是一个例句的开始
        if word[0].isupper() and i!=0:
            #如果前一位是中文
            if '\u4e00' <= words[i-1][-1] <= '\u9fff':
                # 把之前的单词拼接成一个字符串，作为单词或词义，并添加到结果列表中
                result.append(" ".join(words[:i]))
                # 把剩下的单词拼接成一个字符串，作为例句，并添加到结果列表中
                result.append(" ".join(words[i:]))
                # 跳出循环
                break
            elif word[-1] == '.':
                result.append(" ".join(words[:i + 1]))
                result.append(" ".join(words[i + 1:]))
                break
            elif word[-1] == '?':
                result.append(" ".join(words[:i + 1]))
                result.append(" ".join(words[i + 1:]))
                break
        elif word[-1]=='.':
            result.append(" ".join(words[:i+1]))
            result.append(" ".join(words[i+1:]))
            break
        elif word[-1]=='?':
            result.append(" ".join(words[:i + 1]))
            result.append(" ".join(words[i + 1:]))
            break
        elif word[-1]=='。':
            result.append(" ".join(words[:i + 1]))
            result.append(" ".join(words[i + 1:]))
            break
        # 否则，继续遍历下一个单词
        else:
            continue
    fh=['。','？']
    result1.append(result[0])
    count = sum([1 for c in result[1] if c in fh])
    if count > 1:
        result1.extend(parse_sentence(result[1]))
    else:
        result1.append(result[1])
    # 返回结果列表
    return result1
mm=0
x = PrettyTable()
start=time.time()
qiehuan='r'

# 创建根窗口


root = ttk.Window(themename="xin")

# 创建样式对象
# style = ThemedStyle(root)
# style.set_theme("clearlooks") # 设置 win11 主题
#我的名字
root.title("单词背诵软件1.0")

# 更改窗口图标为指定的图像文件
root.iconbitmap("./word3.ico")
#更换背景颜色
def con_enter(e):
    e.widget.config(bg='#02b875')
#变回原来的背景颜色
def con_leave(e):
    global ta
    e.widget.config(bg=ta)
#更换边框颜色
def on_enter(e):
    e.widget.config(highlightbackground='red', highlightcolor='red')
#变回原边框颜色
def on_leave(e):
    global ta,tb
    e.widget.config(highlightbackground=ta, highlightcolor=tb)


# 创建一个全局变量来记录当前的数字
num = 0
js=[]
huan_word=0
huan_se=1
huan_zse=0
pd=0

# 函数：显示菜单（在鼠标位置）
def show_menu(event):
    # 创建菜单控件及菜单项
    menu = tk.Menu(event.widget.master, tearoff=0)
    # 获取鼠标点击的组件
    widget = event.widget
    # 获取鼠标选中的文本
    if widget.tag_ranges("sel"):
        selection = widget.selection_get()
        # 如果有，就启用复制和剪切菜单项
        # 添加菜单项，绑定相应的命令
        menu.add_command(label="剪切", command=lambda: [widget.clipboard_clear(),
                                                        widget.clipboard_append(selection),
                                                        widget.delete("sel.first", "sel.last")]
                         )
        menu.add_command(label="复制", command=lambda: widget.clipboard_append(selection))

    else:
        menu.add_command(label="粘贴", command=lambda: widget.insert('insert', widget.clipboard_get()))
    #显示菜单
    menu.post(event.x_root, event.y_root)

# 创建一个函数来处理确定按钮的点击事件
def confirm():
    global num,word_list,word_list3,rw,resultc,m,js,random_word,c_button,huan_zse,\
        label3,label4,label1,text,confirm_button,button_frame,tr,cancel_button,ta,qiehuan,\
        mr# 声明全局变量
    mr=0


    if num==0:
        # 创建一个我认识按钮
        cancel_button = tk.Button(button_frame, text="我认识", command=cancel, font=('黑体', 16))
        cancel_button.pack(side=tk.RIGHT, anchor=tk.CENTER, padx=20)

        update_label()  # 更新标签，显示第一个单词
        if qiehuan=='r':
            confirm_button.config(text="例句")
            #鼠标靠近时更换背景
            ta=cancel_button.cget('bg')
            confirm_button.bind("<Enter>", con_enter)
            confirm_button.bind("<Leave>", con_leave)
        if qiehuan=='w':
            confirm_button.config(text="我不认识")
            mr=1
            # 鼠标靠近时更换背景
            ta = cancel_button.cget('bg')
            confirm_button.bind("<Enter>", con_enter)
            confirm_button.bind("<Leave>", con_leave)
        cancel_button.bind("<Enter>", con_enter)
        cancel_button.bind("<Leave>", con_leave)


    if len(word_list)==0:  # 判断标签的文本是否是结束
        root.destroy()  # 结束程序
        return 0
    #非第一个单词，从中挑选一个单词。
    if num!=0 and num%2==0:
        #挑选
        random_word = random.choice(word_list)
        #寻找例句
        c = parse_sentence(random_word)
        resultc = c[0:-1]
        resultc.extend(parse_sentence(c[-1]))
        js[word_list3.index(random_word)] += 1
        rw = random_word.split()
        if qiehuan=='r':
            confirm_button.config(text="例句")
        if qiehuan=='w':
            confirm_button.config(text='我不认识')
            mr=1
        update_label()  # 更新标签
        try:
            c_button.destroy()
            text.delete('1.0', 'end')
        except:
            text.delete('1.0', 'end')
        tr = 1
    if num!=0 and num%2==1:
        #挑选例句
        if len(resultc) > 3:
            # 获取resultc长度的奇数索引
            odd_indexes = [i for i in range(1, len(resultc), 2)]

            # 从奇数索引中进行随机选择
            m = random.choice(odd_indexes)
        else:
            m = 1
        #例句中寻找单词
        bl=TextBlob(resultc[m])
        tg=bl.tags
        # print(tg,rw[0])
        ys = find_word(tg, rw[0])
        se=bl.words
        j = 0
        st=''
        ed=''
        kb=''
        for q in ys:
            st+=" ".join(se[j:q])+" "
            kb+=se[q] + " "
            j = q + 1
        ed+=" ".join(se[j:])+"."
        # label2.config(text=str("[example] "+kb))

        # print(st+"///"+kb+'....'+ed)
        confirm_button.config(text="我不认识")
        #创建Chinese按钮，表示按下即可出现翻译
        c_button = tk.Button(root, text="Chinese?",command=chinese,font=("Times New Roman", 16))
        c_button.pack(side=tk.BOTTOM, anchor=tk.CENTER)
        # 鼠标靠近时更换背景
        ta = cancel_button.cget('bg')
        confirm_button.bind("<Enter>", con_enter)
        confirm_button.bind("<Leave>", con_leave)
        cancel_button.bind("<Enter>", con_enter)
        cancel_button.bind("<Leave>", con_leave)
        c_button.bind("<Enter>", con_enter)
        c_button.bind("<Leave>", con_leave)
        text_se(st, kb, ed)
    # else:
    #     label2.config(text='')

    num += 1  # 增加数字
    #如果有翻译了，那么将他们删除
    if huan_zse==1:
        label3.destroy()
        label4.destroy()
        text.delete('1.0', 'end')
        huan_zse=0

#chinese翻译
def chinese():
    global c_button,resultc,m,rw,huan_zse,label3,label4,label1,text,confirm_button,button_frame
    # print(m,len(resultc))
    #label3在这创建
    if m+1 < len(resultc):
        label3 = tk.Label(root, font=("黑体", 15), text=resultc[m+1])
        label3.pack()
    else:
        tk.messagebox.showinfo("提示", "翻译错误\n句子"+str((m+1)/2))
    #label4在这里
    label4 = tk.Label(root, font=("Times New Roman", 15), text=rw[0]+" "+ rw[1])
    label4.pack()
    # 创建一个标签来显示文字
    huan_zse=1
    c_button.destroy()


def validate_entry(txt,kb):
    global entry,label1,rw,x_button,label4,word_list,random_word,w_button,jx_button
    if str(txt) == str(kb):
        entry.configure({"foreground": "green"})
        label1.config(text=str(rw[0]) + " " + str(rw[1]))
        try:
            w_button.destroy()

            x_button = tk.Button(button_frame, text="下一个", command=lambda: [word_list.remove(random_word)
                ,xyg()], font=('黑体', 16))
            x_button.pack(side=tk.RIGHT, anchor=tk.CENTER, padx=20)
            # 更换颜色
            ta = x_button.cget('bg')
            x_button.bind("<Enter>", con_enter)
            x_button.bind("<Leave>", con_leave)
        except:
            pass
        try:
            label4.destroy()
            jx_button = tk.Button(button_frame, text="继续背", command=lambda: [
                jx_button.destroy(),
                xyg()], font=('黑体', 16))
            jx_button.pack(side=tk.RIGHT, anchor=tk.CENTER, padx=20)
            # 更换颜色
            ta = jx_button.cget('bg')
            jx_button.bind("<Enter>", con_enter)
            jx_button.bind("<Leave>", con_leave)
        except:
            pass

        return False
    if txt in kb:
        entry.configure({"foreground": "green"})
        label1.config(text=str(rw[1]))
    else:
        entry.configure({"foreground": "red"})
    return True

#英语句子，该单词显示红颜色
def text_se(st,kb,ed):
    global text,qiehuan,entry,c_button,mr,num,confirm_button,cancel_button
    if qiehuan=='r':
        text.delete('1.0', 'end')
        text.insert(tk.END, "[")
        text.insert(tk.END, "example", "red")
        text.insert(tk.END, "] ")
        text.insert(tk.END, st)
        text.insert(tk.END, kb ,"red")
        text.insert(tk.END, ed)
        text.tag_add("center", '1.0', 'end')
    if qiehuan =='w' and mr==1:
        text.delete('1.0', 'end')
        text.insert(tk.END, "[")
        text.insert(tk.END, "example", "red")
        text.insert(tk.END, "] ")
        text.insert(tk.END, st)
        #获取插入位置
        cursor_pos = text.index(tk.INSERT)
        #创建用户输入按钮，内嵌在text中,居中显示,取消边框
        entry=tk.Entry(text,justify="center",highlightthickness=0,
                       borderwidth=0,font=text.cget("font"))
        #前景色
        entry.configure({"foreground": "gray"})
        #验证为实时验证
        entry.configure({"validate": "key"})
        #验证函数，kb为验证的单词
        entry.configure({"validatecommand": (entry.register(validate_entry), '%P',kb)})
        text.tag_configure("underlined", underline=True)
        #对应位置插入输入框
        text.window_create(cursor_pos,window=entry)

        #插入剩余句子
        text.insert(tk.END, ed)
        text.tag_add("center", '1.0', 'end')
    if qiehuan=='w' and mr==0:
        text.delete('1.0', 'end')
        text.insert(tk.END, "[")
        text.insert(tk.END, "example", "red")
        text.insert(tk.END, "] ")
        text.insert(tk.END, st)
        text.insert(tk.END, kb ,"red")
        text.insert(tk.END, ed)
        text.tag_add("center", '1.0', 'end')
        num += 1
        confirm_button.destroy()
        cancel_button.config(text='拼写')

def xyg():
    global cancel_button,confirm_button,num,x_button,ta,jx_button
    if num % 2 == 1:
        num += 1
    try:
        jx_button.destroy()
    except:
        pass
    x_button.destroy()
    cancel_button = tk.Button(button_frame, text="我认识", command=cancel, font=('黑体', 16))
    cancel_button.pack(side=tk.RIGHT, anchor=tk.CENTER, padx=20)
    confirm_button = tk.Button(button_frame, text="例句", command=confirm, font=('黑体', 16))
    confirm_button.pack(side=tk.LEFT, anchor=tk.CENTER, padx=20)
    ta = cancel_button.cget('bg')
    confirm_button.bind("<Enter>", con_enter)
    confirm_button.bind("<Leave>", con_leave)
    cancel_button.bind("<Enter>", con_enter)
    cancel_button.bind("<Leave>", con_leave)
    confirm()

def view_word():
    global w_button,kb,label4
    w_button.destroy()
    label4 = tk.Label(root, font=("Times New Roman", 15), text="单词:"+kb)
    label4.pack()



# 创建一个函数来处理我认识按钮的点击事件
def cancel():
    global m,num,resultc,word_list,random_word,label1,text,confirm_button,button_frame,tr,rw\
    ,cancel_button,x_button,ta,qiehuan,c_button,w_button,kb,mr# 声明全局变量
    if qiehuan=='r':
        mr=0
        if num!=0:
            word_list.remove(random_word)
            # if num % 2 == 1:
            label1.config(text=str(rw[0]) + " " + str(rw[1]))
            confirm_button.destroy()
            cancel_button.destroy()
            x_button = tk.Button(button_frame, text="下一个", command=xyg, font=('黑体', 16))
            x_button.pack(side=tk.RIGHT, anchor=tk.CENTER, padx=20)
            #更换颜色
            ta = x_button.cget('bg')
            x_button.bind("<Enter>", con_enter)
            x_button.bind("<Leave>", con_leave)
            # else:
            #     confirm()

    if qiehuan=='w':
        mr = 1
        if num!=0 and num%2==0:
            try:
                c_button.destroy()
                text.delete('1.0', 'end')
            except:

                text.delete('1.0', 'end')
        else:
            cancel_button.destroy()
            confirm_button.destroy()

            label1.config(text='')
            # 挑选例句
            if len(resultc) > 3:
                # 获取resultc长度的奇数索引
                odd_indexes = [i for i in range(1, len(resultc), 2)]

                # 从奇数索引中进行随机选择
                m = random.choice(odd_indexes)
            else:
                m = 1
            # 例句中寻找单词
            bl = TextBlob(resultc[m])
            tg = bl.tags
            # print(tg,rw[0])
            ys = find_word(tg, rw[0])
            se = bl.words
            j = 0
            st = ''
            ed = ''
            kb = ''
            for q in ys:
                st += " ".join(se[j:q]) + " "
                kb += se[q] + " "
                j = q + 1
            ed += " ".join(se[j:]) + "."
            # label2.config(text=str("[example] "+kb))
            w_button = tk.Button(button_frame, text="显示单词", command=view_word, font=('黑体', 16))
            text_se(st, kb, ed)
            # print(st+"///"+kb+'....'+ed)

            w_button.pack(side=tk.RIGHT, anchor=tk.CENTER, padx=20)
            # 更换颜色
            ta = w_button.cget('bg')
            w_button.bind("<Enter>", con_enter)
            w_button.bind("<Leave>", con_leave)







# 创建一个函数来更新标签的文本
def update_label():
    global num,rw,label1,text,confirm_button,button_frame # 声明全局变量

    label1.config(text=str(rw[0])) # 更新标签的文本为数字
    # if num==5:
    #     label2.config(text="结束") # 更新标签的文本为结束





def winclose():
    global window,label1,text,confirm_button,button_frame,\
        rw,word_list,word_list3,js,resultc,random_word,tr,mm,ta,num, \
        cancel_button,x_button,c_button,pd
    pd=1
    # 如果得到文件就关闭
    if filepath_var.get():
        stri=filepath_var.get()
        if stri[-3:]!='txt':
            tk.messagebox.showinfo("提示", "请选择txt类型的文件")
            return 0
        try:
            # 获取文件编码类型
            with open(filepath_var.get(), 'rb') as f:
                bm = chardet.detect(f.read())
            # print(bm['encoding'])
            # 打开文件并读取单词列表
            with open(filepath_var.get(), 'r',encoding=bm['encoding']) as f:
                word_list2 = f.read().splitlines()


            bt = word_list2[0]
            word_list1 = word_list2[1:]
            word_list = [value for value in word_list1 if value]
            js = [0] * len(word_list)
            word_list3 = [value for value in word_list]
            # print(bt)
            mm = len(word_list)

            # 做格式检查。
            for check in word_list:
                c = parse_sentence(check)
                resultc = c[0:-1]
                resultc.extend(parse_sentence(c[-1]))
                js[word_list3.index(check)] += 1
                rw = check.split()
                if len(resultc) % 2 == 0:
                    tk.messagebox.showinfo("提示", '格式错误\nproblem in line:'+str(word_list2.index(check) + 1))
                    # print('problem in', word_list2.index(check) + 1)
                    return 0
                if resultc[-1] == '':
                    tk.messagebox.showinfo("提示", '格式错误\nproblem in line:'
                                           + str(word_list2.index(check) + 1)
                                           +"\n 分隔出错"
                                           )
                    # print('problem in', word_list2.index(check) + 1)
                    return 0
                # 首先判断resultc是否正确
                # print(resultc)
                for cjs, nr in enumerate(resultc):
                    if cjs % 2 == 1:
                        for cword in nr:
                            # 英文句子中没
                            if cword == '’':
                                continue
                            if '0'<= cword <= '9':
                                continue
                            if cword=="\u201c" or cword=='\u201d':
                                continue
                            if cword not in string.ascii_letters + " " + string.punctuation:
                                tk.messagebox.showinfo("提示", '格式错误\nproblem in line:'
                                                       + str(word_list2.index(check) + 1)
                                                       +"\n出错字符"+str(cword)
                                                       +"\nascii="+str(ascii(cword)))
                                # print(cword)
                                # print(ascii(cword))
                                # print(resultc)
                                return 0
                    # 检测中文句子
                    if cjs != 0 and cjs % 2 == 0:
                        if nr[-1] not in string.ascii_letters + " ":
                            continue
                        else:
                            tk.messagebox.showinfo("提示", '格式错误\nproblem in line:' + str(word_list2.index(check) + 1))
                            return 0
                            # print(resultc)

        except:
            pd=0
        if pd==0:
            tk.messagebox.showinfo("提示", "请选择正确的文件")
        if pd==1:
            window.destroy()  # 关闭子窗口
            button2.destroy() # 摧毁这个按钮

            # 清除当前（主）窗口中所有的控件除菜单
            for widget in root.winfo_children():
                if not isinstance(widget, tk.Menu):
                    widget.destroy()

            label1 = tk.Label(root, font=("Times New Roman", 20), text=str(bt))
            label1.pack()
            # 创建一个标签来显示数字
            # label2 = tk.Label(root, font=("Arial", 10), text=str(num))
            # label2.pack()
            num=0

            # 创建一个文本组件,显示句子
            text = tk.Text(root, font=("Times New Roman", 15), height=2, wrap="word")
            text.pack(pady=10)
            # 将 highlightthickness 设置为 0 将边框宽度设为 0
            text.configure(bg='SystemButtonFace', highlightthickness=0)

            # 插入一段字符串
            text.insert(tk.END, "Please click 开始 to begin reciting vocabulary words.")
            # 使用标签 "red" 将 "apple" 部分文本设置为红色
            text.tag_configure("red", foreground="red")
            # 配置并定义名称为 "center" 的新标签
            text.tag_configure("center", justify='center')

            text.insert(tk.END, ".")
            # 将所有文本与 "center" 标签相关联
            text.tag_add("center", '1.0', 'end')
            # 为 text 绑定右键点击事件
            text.bind('<Button-3>', show_menu)

            # 创建一个 Frame 容器，以便包含这两个按钮
            button_frame = tk.Frame(root)

            button_frame.pack(side=tk.BOTTOM, expand=True)

            # 创建一个确定按钮
            confirm_button = tk.Button(button_frame, text="开始", command=confirm, font=('黑体', 16))
            confirm_button.pack(side=tk.LEFT, anchor=tk.CENTER, padx=20)
            # 更换颜色
            ta = confirm_button.cget('bg')
            confirm_button.bind("<Enter>", con_enter)
            confirm_button.bind("<Leave>", con_leave)
            # 随机选择一个单词
            random_word = random.choice(word_list)
            c = parse_sentence(random_word)
            resultc = c[0:-1]
            resultc.extend(parse_sentence(c[-1]))
            js[word_list3.index(random_word)]+=1
            rw=random_word.split()

def browse_file():
    file_path = filedialog.askopenfilename()
    filepath_var.set(file_path)

def open_window():
    global window,ta
    # 创建一个 Toplevel 对象作为子窗口
    window = tk.Toplevel(root)
    window.resizable(0, 0)
    window.attributes('-toolwindow', True)
    # 设置子窗口的标题和大小
    window.title("选择文件")

    #让子窗口一直在最前端
    window.grab_set()
    # 创建一个 Frame 让用户输入文件路径，
    # 并将其设置为在左侧（WEST）排列
    filepath_frame = tk.Frame(window)
    filepath_frame.pack(pady=10, padx=20, side=tk.LEFT)

    filepath_label = tk.Label(filepath_frame, text="请输入文件路径:")
    filepath_label.grid(row=0, column=0)

    filepath_entry = tk.Entry(filepath_frame, textvariable=filepath_var)
    filepath_entry.grid(row=0, column=1)

    # 创建一个 "打开文件" 的按钮，
    # 并将其设置为在右侧（EAST）排列
    button_frame = tk.Frame(window)
    button_frame.pack(pady=10, padx=20, side=tk.RIGHT)

    button = tk.Button(button_frame, text="打开文件", command=browse_file)
    button.pack(side=tk.LEFT, padx=5)

    button2 = tk.Button(button_frame, text="确定", command=winclose)
    button2.pack(side=tk.RIGHT)
    # 更换颜色
    ta = button.cget('bg')
    button.bind("<Enter>", con_enter)
    button.bind("<Leave>", con_leave)
    button2.bind("<Enter>", con_enter)
    button2.bind("<Leave>", con_leave)


def word_qiehuan():
    global qiehuan
    qiehuan='r'
def write_qiehuan():
    global qiehuan
    qiehuan='w'

# 设置窗口大小
root.geometry("800x300")

input_text = tk.StringVar()

# 创建菜单并添加选项
menu_bar = tk.Menu(root)

file_menu = tk.Menu(menu_bar, tearoff=False)

file_menu.add_command(label="new",command=open_window)
#file_menu.add_command(label="Save")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.destroy)

menu_bar.add_cascade(label="File", menu=file_menu)

mode_menu = tk.Menu(menu_bar, tearoff=False)

mode_menu.add_checkbutton(label='word',variable=0, onvalue=1, offvalue=0,command=word_qiehuan)
mode_menu.add_checkbutton(label='write',variable=0, onvalue=2, offvalue=0,command=write_qiehuan)

menu_bar.add_cascade(label="mode", menu=mode_menu)


# 将菜单添加到主窗口
root.config(menu=menu_bar)


# 创建一个 StringVar 对象用于追踪已选择的文件路径
filepath_var = tk.StringVar()


# 在根窗口中添加一个按钮
button2 = tk.Button(root, text="打开文件", command=open_window)
button2.pack( expand=True)
button2.place(relx=0.5, rely=0.5, anchor='center')
#更换颜色
ta = button2.cget('bg')
button2.bind("<Enter>", con_enter)
button2.bind("<Leave>", con_leave)









# 运行主循环
root.mainloop()

def end_root():
    root2.destroy()



if pd==1:
    # 创建根窗口
    root2 = tk.Tk()

    #我的名字
    root2.title("单词背诵结束1.0(by Xingyu)")
    # 设置窗口大小
    root2.geometry("600x300")

    end=time.time()
    max=[]
    j=0
    for i in js:
        if i > 5:
            max.append(j)
        j=j+1
    label1 = tk.Label(root2, font=("黑体", 20), text="重复较高的单词:")
    label1.pack()


    fm=tk.Frame(root2)
    fm.pack()

    table=[]
    x.field_names = ["Word","Translation", "Count"]
    for i in max:
        k=word_list3[i].split()

        x.add_row([k[0],k[1],js[i]])
        # print(word_list3[i],end=' ')
        # print("背诵了：",js[i],"次")
    text = tk.Text(fm, height=5,font=("Times New Roman", 20),wrap="word")
    scrollbar = tk.Scrollbar(fm, command=text.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    scrollbar.config(command=text.yview)


    text.configure(yscrollcommand=scrollbar.set)



    text.pack(padx=10, pady=10)


    text.tag_configure("center", justify='center')  # 定义 "center" 标签为居中对齐
    text.insert(1.0, str(x))  # 将文件插入文本框的开头
    text.tag_add("center", "1.0", tk.END)  # 为文字添加 "center" 标签

    ta = text.cget('highlightcolor')
    tb = text.cget('highlightbackground')

    #更换边框颜色
    text.bind("<Enter>",on_enter)
    text.bind("<Leave>", on_leave)





    # 为 text 绑定右键点击事件
    text.bind('<Button-3>', show_menu)


    t=end-start
    hours, remainder = divmod(t, 3600)
    minutes, seconds = divmod(remainder, 60)

    # 创建一个文本组件,显示句子
    text = tk.Text(root2,font=("Times New Roman", 15), height=3,wrap="word")
    text.pack()
    # 将 highlightthickness 设置为 0 将边框宽度设为 0
    text.configure(bg='SystemButtonFace', highlightthickness=0)

    # 插入一段字符串
    text.insert(tk.END, "本章单词共：")
    # 使用标签 "red" 将 "apple" 部分文本设置为红色
    text.tag_configure("red", foreground="red")
    # 配置并定义名称为 "center" 的新标签
    text.tag_configure("center", justify='center')

    text.insert(tk.END, str(mm),"red")
    text.insert(tk.END, " 个\n")
    text.insert(tk.END, "本次背诵时间为：")
    text.insert(tk.END, str(int(hours)),"red")
    text.insert(tk.END, "时")
    text.insert(tk.END, str(int(minutes)),"red")
    text.insert(tk.END, "分")
    text.insert(tk.END, str(round(seconds, 2)),"red")
    text.insert(tk.END, "秒")
    # 将所有文本与 "center" 标签相关联
    text.tag_add("center", '1.0', 'end')
    # 创建一个取消按钮
    cancel_button = tk.Button(root2, text="结束", command=end_root)
    cancel_button.pack(side=tk.BOTTOM, anchor=tk.CENTER)

    s=open(".\\Repeat higher words.txt","a+")
    for i in max:
        s.write(word_list3[i])
        s.write("\n")
    s.close()


    # 运行主循环
    root2.mainloop()