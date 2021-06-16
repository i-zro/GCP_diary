from wordcloud import WordCloud, STOPWORDS
from eunjeon import Mecab
import matplotlib.pyplot as plt
import pandas as pd

# 한글 폰트 패스로 지정
import matplotlib.font_manager as fm
import re
import collections

from nlp.analysis import TextAnalysis

ta = TextAnalysis('행복한 하루입니다.')

result = ta.text_analysis()

words = result['word_count']

# print(words)


spwords = set(STOPWORDS)

wordcloud = WordCloud(max_font_size=200, font_path='/content/drive/My Drive/Colab Notebooks/malgun.ttf',
                     stopwords=spwords,
                     background_color='#FFFFFF',
                     width=1200,height=800).generate_from_frequencies(words)


plt.figure(figsize = (8, 8), facecolor = None) 
plt.imshow(wordcloud) 
plt.axis("off") 
plt.tight_layout(pad = 0) 
  
plt.show() 