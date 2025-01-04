import tkinter as tk


# 输入输出可视化类
class Main:
    SYMBOLS = ['+', '-', '×', '÷', '(', ')']  # 定义常量符号列表
    def __init__(self):
        self.inoutput_text = None  # 初始化输入输出文本框的属性
        self.last_line = 1  # 初始化最后一次计算的行号

        # 创建窗口元素
        self.window = tk.Tk()
        self.window.title("计算器gui")
        self.window.geometry("500x400")

        # 获取窗口的背景颜色
        self.window_bg_color = self.window.cget("bg")

        # 放置标题标签
        title = tk.Label(self.window, text='计算器gui', bg=self.window_bg_color, fg='black', font=('Arial', 12),
                         width=12, height=2,
                         highlightbackground='black', highlightthickness=1)
        title.pack(pady=(20, 0))

        # 放置输入输出文本框框架
        inoutput_frame = tk.Frame(self.window, width=300, height=30)
        inoutput_frame.pack(pady=(10, 10))

        # 放置输入输出文本框
        self.inoutput_text = tk.Text(inoutput_frame, width=18, height=1, font=('Arial', 24))  # 使用实例属性
        self.inoutput_text.pack(side='left')

        # 创建滚动条
        self.scrollbar = tk.Scrollbar(inoutput_frame, command=self.inoutput_text.yview)  # 关联文本框
        self.scrollbar.pack(side='right', fill='y')  # 在文本框右侧放置滚动条
        self.inoutput_text.config(yscrollcommand=self.scrollbar.set) # 配置文本框以使用滚动条

        # 创建数字和运算符按钮 
        self.create_buttons()  # 创建按钮
    
    def create_button(self,frame, text, width,command):
            """辅助方法用于创建按钮"""
            return tk.Button(frame, text=text, bg=self.window_bg_color, fg='black', font=('Arial', 12),
                            width=width, height=2,
                            highlightbackground='black', highlightthickness=1,
                            command=command)
    
    def create_symbol_buttons(self, frame, symbols):
            """创建符号按钮"""
            for idx, symbol in enumerate(symbols[:2]):  # 只取前两个符号
                padx_value = 10 if idx == 0 else 5  # 第一个按钮加10的左间距，第二个按钮加5的左间距
                symbol_button = self.create_button(frame, symbol, 5, lambda symbol_var=symbol: self.do_calc(symbol_var))
                symbol_button.pack(side="left", padx=(padx_value, 0))  # 使用计算得到的间距
            del symbols[:2]  # 删除已使用的符号

    def create_special_buttons(self, frame):
        """创建特殊按钮0、AC 和 ="""
        zero_button = self.create_button(frame, '0', 5, lambda symbol_var='0': self.do_calc(symbol_var))
        zero_button.pack(side="left",padx=(0,5))
        clear_button = self.create_button(frame, 'AC', 12, self.clear_input)
        clear_button.pack(side="left")
        equal_button = self.create_button(frame, '=', 12, lambda symbol_var='=': self.do_calc(symbol_var))
        equal_button.pack(side="left", padx=(12, 0))

    def create_buttons(self):
        symbols = self.SYMBOLS.copy()  # 使用常量符号列表
        for i in range(3, 0, -1):
            button_frame = tk.Frame(self.window)
            button_frame.pack(anchor='w', padx=(100, 5)) 
            for j in range(i * 3 - 2, i * 3 + 1):
                # 创建数字按钮
                num_button = self.create_button(button_frame, str(j),5, lambda num=j: self.do_calc(num))
                num_button.pack(side="left", padx=(0, 5))

                # 按照位置创建运算符号按钮
                if j in (3, 6, 9):
                    self.create_symbol_buttons(button_frame, symbols)

                    # 创建'AC'和'=' 按钮
                    if j == 3:
                        long_frame = tk.Frame(self.window)
                        long_frame.pack(anchor='w', padx=(100, 5), pady=(5, 0))
                        self.create_special_buttons(long_frame)

    def update_output_view(self, text):
        """更新输出视图并滚动到最新位置"""
        self.inoutput_text.insert('end', text)  # 插入文本
        self.inoutput_text.see(tk.END)  # 滚动到最新位置
        self.last_line = self.inoutput_text.index('end').split('.')[0]  # 更新行号
    
    def do_calc(self, num):
        var = str(num)  # 将num转换为字符串
        if var == '=':
            # 从上次计算的行号开始获取文本框内容
            expression = self.inoutput_text.get(f'{self.last_line}.0', tk.END).strip()  # 获取文本框内容并去除两端空白

            # 替换字符为计算符号
            expression = expression.replace('×', '*').replace('÷', '/')
            try:
                result = eval(expression)  # 计算结果，eval() 会将传入的字符串解析为 Python 表达式，并在当前的全局和局部命名空间中执行它，然后返回执行结果。
                # 在文本框中插入换行符和计算结果
                self.update_output_view(f'\n= {result}')  # 更新视图

            except Exception as e:
                self.update_output_view('\n错误')  # 更新视图
            
            # 插入换行符
            self.inoutput_text.insert('end', '\n')
        else:
            self.inoutput_text.see(tk.END)  # 让滚动条滚动到最新位置
            self.inoutput_text.insert('end', var)  # 使用实例属性

    def clear_input(self):
        self.inoutput_text.delete('1.0', tk.END)
        self.last_line = 1  

    def run(self):
        self.window.mainloop()  # 主循环，保持窗口打开

if __name__ == '__main__':
    main = Main()  # 创建 Main 类的实例
    main.run()  # 主循环，保持窗口打开
