from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from time import sleep

class Spider:
    def __init__(self):
        # 设置浏览器驱动
        self.driver = webdriver.Edge(service=Service('D:/edgedriver_win64/msedgedriver.exe'))

    def run(self):
        dic_all={}
        # 遍历每个 li 元素
        for i in range (1,16):
            next_url = 'http://www.xshiqi.com/category_zyzs/dzzs/gddy/index_' + str(i) + '.html'
            self.driver.get(next_url)
            ul = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[1]/ul'))
            )
            li_elements = ul.find_elements(By.TAG_NAME, 'li')
            for li in li_elements:
                # 创建字典
                text=li.text
                parts=text.split('-')
                if len(parts)!=4:
                    continue
                print(parts)
                parts[2]=parts[2].replace(']','')
                gua=parts[1]+'-'+parts[2]
                ci=parts[3]
                single_data = {
                    '辞': ci,  # 获取 li 的文本内容
                    '链接': li.find_element(By.TAG_NAME, 'a').get_attribute('href')  # 获取链接
                }
                # 保存字典到字典的字典中
                dic_all[gua]=single_data

        # 保存字典到新python文件中
        with open(r'e:\\python_work\\.aaavscode\\coin\\数据.py', 'w', encoding='utf-8') as f:
            f.write('data = ' + str(dic_all) + '\n\n')
            f.write('def get_entry(key):\n')
            f.write('    """根据给定的 key 返回对应的条目内容，确保返回的字典有两个元素"""\n')
            f.write('    entry = data.get(key, None)\n')
            f.write('    if entry is not None:\n')
            f.write('        return {\n')
            f.write('            "辞": entry["辞"],\n')
            f.write('            "链接": entry["链接"]\n')
            f.write('        }\n')
            f.write('    else:\n')
            f.write('        return {"错误": "条目不存在"}\n')
                

        # 关闭浏览器
        self.driver.quit()
        print('爬取完成')

# 使用 Spider 类
if __name__ == "__main__":
    spider_instance = Spider()
    spider_instance.run()
