from eunjeon import Mecab

import matplotlib.pyplot as plt
import pandas as pd

# 한글 폰트 패스로 지정
import matplotlib.font_manager as fm
import re
import collections

def decompose(ls,score):
    # print(ls)
    tag = ['VCP', 'VCN', 'NNG', 'IC', 'MAG', 'VA', 'VV', 'XR']

    if score == 1:
        tag.pop(1)
    elif score == -1:
        tag[1:]
    
    word_list = []

    for txt in ls:
        out = mecab.pos(txt)
        for word in out:
            if word[1] in tag:
                word_list.append(word[0])
    
    return list(set(word_list))

mecab = Mecab()


positive = pd.read_csv('positive.txt', sep="\t", engine="python", encoding ="utf-8")
pos = decompose(positive.T.values[0],1)

negative = pd.read_csv('negative.txt', sep="\t", engine="python", encoding ="utf-8")
neg = decompose(negative.T.values[0],-1)

unknown = pd.read_csv('unknown.txt', sep="\t", engine="python", encoding ="utf-8")
unk = decompose(unknown.T.values[0],0)

# 불용어 정의
stopwords=['의','가','이','은','들','는','좀','꽤','주','잘','걍','과','도','를','으로','자','에','와','한','하','다','있']

chk = []
for word in pos:
    if word in neg:
        chk.append(word)

for word in neg:
    if word in pos:
        chk.append(word)

chk = list(set(chk))

print('chk', len(chk))

print('before pos', len(pos))
print('before neg', len(neg))

for word in chk:
    if word in pos:
        pos.remove(word)
    if word in neg:
        neg.remove(word)

for word in stopwords:
    if word in pos:
        pos.remove(word)
    if word in neg:
        neg.remove(word)

print('after pos', len(pos))
print('after neg', len(neg))


# print('chk', sorted(chk))

plus = ['새롭', '안정', '신통', '멋', '순하', '똘똘', '온순', '다정', '편하', '그리움', '깨끗', '시원', '깜찍', '편리', '자지러지', 
'웃', '이익', '성글', '흡족', '행복', '착하', '편안', '산뜻', 
'든든', '귀염', '아름답', '대단', '평온','있'
'익살', '사랑', '은혜', '흥', '상서', '안심',
'상쾌', '깨달음', '열심히', '희희', '이득', '향기', '훌륭', '희망', '따뜻', '좋']

minus = ['근심', '원통', '원망', '불만', '더러움', '부담', '아쉬움', '부당', '애타',
'구차', '거짓', '측은', '나쁘', '무너지', '망상', '고문',
'떨리', '결점', '괴로움', '혼란', '지저분', '괴롭', '잃', '어려움', '어긋남', '칠칠', '거부',
'없', '형벌', '걱정', '잘못', '싸우', '어긋나', '않', '분하']

pos += plus
neg += minus

pos = list(set(pos))
neg = list(set(neg))

print('pos',len(pos))
print('neg',len(neg))

with open('pos.txt', 'w') as f:
    for item in pos:
        f.write("{}\n".format(item))
f.close()

with open('neg.txt', 'w') as f:
    for item in neg:
        f.write("{}\n".format(item))
f.close()

with open('unk.txt', 'w') as f:
    for item in unk:
        f.write("{}\n".format(item))
f.close()