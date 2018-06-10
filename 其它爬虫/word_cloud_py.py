#coding:utf-8

"""
使用结巴分词生成云图
 说明这里
 1.生成词云一定要设置字体样式，否则汉字出现乱码或者不显示
 2.我不知道为什么本机一直显示不了中文，后面我加了jieba分词词库就可以显示中文了

"""

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba




#生成词云
def create_word_cloud(filename):
    text= open("{}.txt".format(filename)).read()
    # 结巴分词
    wordlist = jieba.cut(text, cut_all=True)
    wl = " ".join(wordlist)

    # 设置词云
    wc = WordCloud(
        # 设置背景颜色
        background_color="white",
         # 设置最大显示的词云数
       max_words=2000,
         # 这种字体都在电脑字体中，一般路径
       font_path='C:\Windows\Fonts\simfang.ttf',
       height= 1200,
       width= 1600,
        # 设置字体最大值
       max_font_size=100,
     # 设置有多少种随机生成状态，即有多少种配色方案
       random_state=30,
    )

    myword = wc.generate(wl)  # 生成词云
    # 展示词云图
    plt.imshow(myword)
    plt.axis("off")
    plt.show()
    wc.to_file('py_book.png')  # 把词云保存下


if __name__ == '__main__':
    create_word_cloud('fenng_wb')