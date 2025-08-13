import csv
import re
from collections import Counter
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog

# 读取CSV文件
def read_titles(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row['Title'] for row in reader]

# 清洗与分词（中英文适配）
def process_text(text):
    text = re.sub(r'[^\w\s]', '', text.lower())  # 去标点、转小写
    words = text.split()      # 英文按空格分词
    return words

# 统计词频并过滤停用词
def count_word_freq(titles):
    all_words = []
    stop_words = set(['and', 'the', 'of','for','in','as','with','on','by','to','is','are','and','its','that','this','was','were','will','would','have','had','has','had','be','been','be','being','do','does','did','get','got','give','given','take','taken','use','used','get','got','give','take','use','want','need','like','love','hate','know','think','feel','see','hear','smell',])  # 自定义停用词表
    
    for title in titles:
        words = process_text(title)
        filtered = [w for w in words if w not in stop_words and len(w) > 1]  # 过滤单字停用词
        all_words.extend(filtered)
    
    return Counter(all_words)

def csvSelect():
    global titles
     # 弹出文件选择对话框
    root = tk.Tk()
    root.withdraw()  # 不显示主窗口
    file_path = filedialog.askopenfilename(
        title="请选择CSV文件",
        filetypes=[("CSV files", "*.csv")]
    )
    if not file_path:
        print("未选择文件，程序退出。")
        exit()
    titles = read_titles(file_path)


# 主流程
if __name__ == "__main__":

    # 下面两条二选一
    #csvSelect()  # 弹出文件选择对话框，选择CSV文件
    titles = read_titles(r'C:\Users\Xivinyr\Desktop\导出的条目.csv')  # 读取CSV文件中的标题
    
    
    word_freq = count_word_freq(titles)  # 根据语言切换

    # 导出词频表（CSV）
    with open('词频统计.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Word', 'Count'])
        for word, count in word_freq.most_common():
            writer.writerow([word, count])
    
    # 可视化
    top_words = word_freq.most_common(30)  # 获取前30个高频词
    # 升序排列
    top_words = sorted(top_words, key=lambda x: x[1])
    words, counts = zip(*top_words)
    plt.figure(figsize=(10, 8))
    bars = plt.barh(words, counts)
    plt.title('Common Words')
    plt.tight_layout()
    # 在条形图上显示词频数值
    for bar, count in zip(bars, counts):
        plt.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, str(count), va='center')

    print("词频统计完成")
    plt.show()  # 显示图表