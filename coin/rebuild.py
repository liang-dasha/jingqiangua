import tkinter as tk
from PIL import Image, ImageTk
import random as rd
import copy
import webbrowser
import re
try:
    from 数据 import get_entry
except:
    try:
        from 爬虫 import Spider
        Spider.run()
    except:
        pass


class Main():
    def __init__(self):
        # 创建并运行窗口
        self.window_center()
        # 导入图片
        self.input_imp()
        # 初始化变量
        self.values_reset()
        # 创建所有框架和部件
        self.init_ui()
        # 创建按钮
        self.button_set()
        self.throw_btn.pack(side='bottom', pady=(0, 30))
        # 必要初始化
        self.yao_names = [['上','五','四','三','二','初'],['六','九']]
        self.gua_names = [
                ["坤为地", "山地剥", "水地比", "风地观", "雷地豫", "火地晋", "泽地萃", "天地否"],
                ["地山谦", "艮为山", "水山蹇", "风山渐", "雷山小过", "火山旅", "泽山咸", "天山遯"],
                ["地水师", "山水蒙", "坎为水", "风水涣", "雷水解", "火水未济", "泽水困", "天水讼"],
                ["地风升", "山风蛊", "水风井", "巽为风", "雷风恒", "火风鼎", "泽风大过", "天风姤"],
                ["地雷复", "山雷颐", "水雷屯", "风雷益", "震为雷", "火雷噬嗑", "泽雷随", "天雷无妄"],
                ["地火明夷", "山火贲", "水火既济", "雷火丰", "离为火", "泽火革", "天火同人"],
                ["地泽临", "山泽损", "水泽节", "风泽中孚", "雷泽归妹", "火泽睽", "兑为泽", "天泽履"],
                ["地天泰", "山天大畜", "水天需", "风天小畜", "雷天大壮", "火天大有", "泽天夬", "乾为天"]
                ]
               
    def window_center(self):
        # 创建窗口
        self.window = tk.Tk()
        self.window.title("六爻")
        # 获取屏幕宽度和高度
        width = self.window.winfo_screenwidth()
        height = self.window.winfo_screenheight()
        # 计算窗口居中位置
        x = (width - 800) / 2
        y = (height - 600) / 2
        # 设置窗口位置
        self.window.geometry("800x600+%d+%d" % (x, y))
        # 获取背景颜色
        self.bg_color = self.window.cget("bg")

    def input_imp(self):
        self.back_img = Image.open('0.png')
        self.front_img = Image.open('1.png')
        self.back_img = self.back_img.resize((50, 50))
        self.front_img = self.front_img.resize((50, 50))
        self.back_img = ImageTk.PhotoImage(self.back_img)
        self.front_img = ImageTk.PhotoImage(self.front_img)
    
    def values_reset(self):
        self.coin_list = [[None for _ in range(3)] for _ in range(6)]
        self.yaos_list = [""]*6
        self.dongyao = [None] * 6
        self.gua = ['', '']
        self.click_cut = 6
             
    def init_ui(self):
        # 放置标题标签
        title = tk.Label(self.window, text='领取好运', bg=self.bg_color, fg='black', 
                         font=('TkHeadingFont', 12), width=12, height=2,
                         highlightbackground='black', highlightthickness=1)
        title.pack(pady=(20, 30))
        # 初始化UI界面
        self.frame_reset()  # 创建框架
           
    def frame_make(self, root, width, height, TF='T', side='top', padx=(0, 0)):
        frame = tk.Frame(root, bg=self.bg_color, width=width, height=height)
        if TF == 'F':
            frame.pack_propagate(False)
        frame.pack(anchor='w', side=side, padx=padx)
        return frame
        
    def frame_reset(self):
        # 预设内容
        frame_style1 = {'height': 330, 'TF': 'F', 'side': 'left', 'padx': (30, 0)}
        # 主框架设置
        self.frame = self.frame_make(self.window, 800, 600)
        # 左侧掷硬币框架
        self.left_frame = self.frame_make(self.frame, 260, **frame_style1)
        self.left_part_make()
        # 右侧展示卦象框架
        self.right_frame = self.frame_make(self.frame, 450, **frame_style1)
        self.right_part_make()  

    def button_set(self):
        # 定义按钮的样式
        button_style = {'bg': 'white', 'fg': 'black',
                        'font': ('TkDefaultFont', 12),
                        'width': 10, 'height': 2}

        # 创建按钮
        self.throw_btn = tk.Button(self.window, text='投掷硬币', **button_style,
                                   command=lambda: self.hit_throw())
        self.chenggua_btn = tk.Button(self.window, text='成卦', **button_style,
                                     command=lambda: self.hit_cut())
        self.reset_btn = tk.Button(self.window, text='再来一次', **button_style,
                                command=self.hit_reset)

    def left_part_make(self):
        # 必要初始化
        show_cut = ['一', '二', '三', '四', '五', '六']
        self.text_labels = []  # 将text_labels定义为实例变量
        self.result_frames = []  # 将result_frames定义为实例变量

        # 左框架中的六行投掷结果框架及标签 
        for i in range(5, -1, -1):
            result_frame = tk.Frame(self.left_frame, bg=self.bg_color)
            result_frame.pack()
            text_label = tk.Label(result_frame, text=f'第{show_cut[i]}次投掷:', bg=self.bg_color, fg='black', font=('TkDefaultFont', 12))
            self.result_frames.append(result_frame)  # 将result_frame添加到实例变量中
            self.text_labels.append(text_label)  # 将text_label添加到实例变量中

    def right_part_make(self):
        root=self.right_frame
        #展示卦象文字的框架
        self.gua_text_frame=self.frame_make(root, 450, 25, 'F')
        # 展示卦象图案的框架
        self.gua_img_frame=self.frame_make(root, 450, 150, 'F')
        #展示本卦卦象图案的画布
        self.canvas = tk.Canvas(self.gua_img_frame, width=230, height=150, bg=self.bg_color)
        self.canvas.pack_propagate(False)
        self.canvas.pack(side=tk.LEFT)
        #展示变卦卦象图案的画布
        self.canvas2 = tk.Canvas(self.gua_img_frame, width=220, height=150, bg=self.bg_color)
        self.canvas2.pack_propagate(False)
        self.canvas2.pack(side=tk.LEFT)
        #展示取卦/爻辞的文字
        self.choose_label=tk.Label(root, text='', bg=self.bg_color, fg='black', font=('TkDefaultFont', 12))
        #展示具体的爻辞或卦辞
        self.link_text = tk.Text(root, height=1, bg=self.bg_color, fg='black', font=('Arial', 12), wrap=tk.WORD,
                                  borderwidth=0, highlightthickness=0)
     
    def write_gua(self, text, padx, gua=None):
        if gua is None:
            gua = self.yaos_list
        shanggua_num = gua[2] * 4 + gua[1] * 2 + gua[0]
        xiagua_num = gua[5] * 4 + gua[4] * 2 + gua[3]
        gua_name = self.gua_names[xiagua_num][shanggua_num]
        gua_text = tk.Label(self.gua_text_frame, text=f'{text}卦为：{gua_name}', bg=self.bg_color, fg='black', font=('TkDefaultFont', 12))
        gua_text.pack(side=tk.LEFT, padx=padx)
        return gua_name

    def draw_gua(self,gua,canvas):
        place=self.yao_names[0].copy()
        liujiu=self.yao_names[1].copy()
        width=20
        clr=['blue','red']
        for index, yao in enumerate(gua):
            line=index+1
            y=10+line*width
            yingyao=[[45, y, 78, y],[92, y, 125, y]]
            yangyao=[[45, y, 125,y]]

            if index == 0 or index == 5:
                text=place[index]+liujiu[yao]
            else:
                text=liujiu[yao]+place[index]
            canvas.create_text(20, y, text=text, fill=clr[yao], font=('Helvetica', 12))
            if yao == 0:
                canvas.create_line(yingyao[0], fill=clr[yao], width=4)
                canvas.create_line(yingyao[1], fill=clr[yao], width=4)
            else:
                canvas.create_line(yangyao[0], fill=clr[yao], width=4)

    def show_gua(self):
        '''展示卦象'''
        bengua=self.yaos_list.copy()
        self.gua[0]=self.write_gua('本',(0,120))
        self.draw_gua(bengua,self.canvas)
        biangua=self.biangua(bengua)
        self.gua[1]=self.write_gua('变',(0,0),bengua)
        self.draw_gua(biangua,self.canvas2)

    def biangua(self,gua):
        for index, dongyao in enumerate(self.dongyao):
            if dongyao == 1:
                gua[index] = 0 if gua[index] == 1 else 1
        return gua

    def choose(self):
        cut = self.dongyao.count(1)
        gua_name = self.gua[1]  # 默认使用变卦

        # 处理特殊情况：乾为天或坤为地且六爻皆动
        if (self.gua[1] == '乾为天' or self.gua[1] == '坤为地') and cut == 6:
            text = f'六爻皆动，变卦{self.gua[1]}，取{self.gua[1]}用{"九" if self.gua[1] == "乾为天" else "六"}：'
            num_input = 7
        else:
            # 根据动爻数量选择本卦或变卦
            gua_name = self.gua[0] if cut <= 3 else self.gua[1]
            text, qvyao = self.get_yao_text_and_index(cut, self.dongyao, self.yaos_list)
            num_input = 6 - qvyao if qvyao != -1 else 0

        # 更新界面显示
        self.choose_label.config(text=text)
        self.choose_label.pack(anchor='nw', side='top', pady=5)
        self.link_TEXT(gua_name, num_input)

    def link_TEXT(self, gua, num):
        input_dic = f"{gua}-{num}"
        dic_need = get_entry(input_dic)
        text1=re.search(r'[\u4e00-\u9fa5]$', gua).group()
        text2 = dic_need['辞']
        link = dic_need['链接']

        # 插入文本和设置文本不可编辑
        self.link_text.insert(tk.END, f'{text1}卦丨{text2}', 'link')
        self.link_text.config(state=tk.DISABLED)

        # 绑定鼠标点击事件
        self.link_text.tag_bind("link", "<Button-1>", lambda event: self.open_link(event,link))

        # 绑定鼠标悬停事件
        self.link_text.tag_bind("link", "<Enter>", self.on_enter)  # 鼠标进入时
        self.link_text.tag_bind("link", "<Leave>", self.on_leave)  # 鼠标离开时

        self.link_text.pack(anchor='nw', side='top', pady=20)

    def on_enter(self, event):
        # 设置鼠标指针为手型
        event.widget.config(cursor="hand2")
        self.link_text.tag_config("link", foreground='blue', underline=True)

    def on_leave(self, event):
        # 恢复默认鼠标指针
        event.widget.config(cursor="")
        self.link_text.tag_config("link", foreground='black', underline=False)

    def open_link(self,event,link):
        # 打开链接
        webbrowser.open(link)  

    def get_yao_text_and_index(self,cut, dongyao, yaos_list):
        if cut == 0:
            return '无动爻，取本卦卦辞：', -1
        elif cut == 1:
            return '一动爻，取本卦动爻：', [index for index, value in enumerate(dongyao) if value == 1][0]
        elif cut == 2:
            dong = [index for index, value in enumerate(dongyao) if value == 1]
            if yaos_list[dong[0]] == yaos_list[dong[1]]:
                return '二动爻，同阴阳取本卦上动爻：', dong[0]
            else:
                return '二动爻，一阴一阳取本卦老阴爻：', dong[0] if yaos_list[dong[0]] == 0 else dong[1]
        elif cut == 3:
            return '三动爻，取本卦中间动爻：', [index for index, value in enumerate(dongyao) if value == 1][1]
        elif cut == 4:
            dong = [index for index, value in enumerate(dongyao) if value == 0]
            if yaos_list[dong[0]] == yaos_list[dong[1]]:
                return '四动爻，静爻同阴阳取下静爻：', dong[1]
            else:
                return '四动爻，静爻一阴一阳取阳静爻：', dong[0] if yaos_list[dong[0]] == 1 else dong[1]
        elif cut == 5:
            return '五动爻，取变卦静爻：', [index for index, value in enumerate(dongyao) if value == 0]
        else:
            return '六动爻，取变卦卦辞：', -1

    def main_cut(self):
        coin_list = copy.deepcopy(self.coin_list)
        yaos_list = self.yaos_list.copy()
        dongyao_list = self.dongyao.copy()

        for index, coin_group in enumerate(coin_list):
            for i in range(len(coin_group)):
                coin_group[i] = rd.randint(0, 1)
            yaos_list[index] = 1 if sum(coin_group) >= 2 else 0
            dongyao_list[index] = 1 if sum(coin_group) in [0, 3] else 0

        self.yaos_list = yaos_list
        self.coin_list = coin_list
        self.dongyao = dongyao_list

    def hit_throw(self):
        self.click_cut -= 1
        i=self.click_cut
        if i == 5:
            self.main_cut()
        self.text_labels[i].pack(side='left')  
        for j in range(3):
            if self.coin_list[i][j] == 1:
                imp_label = tk.Label(self.result_frames[i], image=self.front_img, bg=self.bg_color)
            else:
                imp_label = tk.Label(self.result_frames[i], image=self.back_img, bg=self.bg_color)
            imp_label.pack(side='left')

        if i == 0:
            self.throw_btn.pack_forget()
            self.chenggua_btn.pack(side='bottom', pady=(0, 30))

    def hit_cut(self):
        self.show_gua()
        self.choose()
        self.chenggua_btn.pack_forget()
        self.reset_btn.pack(side='bottom', pady=(0, 30))

    def hit_reset(self):
        self.frame.destroy()
        self.values_reset()
        self.frame_reset()

        self.reset_btn.pack_forget()
        self.throw_btn.pack(side='bottom', pady=(0, 30))

    def run(self):
        # 运行窗口
        self.window.mainloop()

if __name__ == '__main__':
    main = Main()
    main.run()
