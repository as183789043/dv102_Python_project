import jieba
from wordcloud import WordCloud
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
stopwords = set()

wordlist = []
for x in open('GM非常泰.csv', "r", encoding="utf-8").readlines():
    wordlist.append(x.strip().split(' ')[0])
    
jiebaword = " ".join(jieba.cut(",".join(wordlist)))

content  = [stopword.strip() for stopword in open("stopwords.txt", "r", encoding="utf-8").readlines()]
stopwords.update(content)
font = 'General_Art.ttf' # 設定字體格式
pngfile = "C:/Users/SCE/520.png"
mask1 = np.array(Image.open(pngfile))

wc = WordCloud(background_color="white", margin=2, mask=mask1, font_path=font, max_words=200, stopwords=stopwords).generate(jiebaword)

# _from_frequencies
# wc.generate_from_text(content)
# 生成文字雲 # 吃入次數字典資料
plt.imshow(wc) 
plt.axis("off")
# 展示
plt.show()

# 儲存
wc.to_file('GM非常泰0.png')