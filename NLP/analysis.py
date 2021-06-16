#-*- coding: utf-8 -*-
import os
from collections import Counter

from eunjeon import Mecab
import pandas as pd


class TextAnalysis:

    mecab = Mecab()
    emotion_idx = {
        'happy': 1, 'sad': 2, 'delight': 3, 'boring': 4, 'angry': 5, 'surprise': 6, 'horror': 7
    }
    tag = ['VCP', 'VCN', 'NNG', 'IC', 'MAG', 'VA', 'VV', 'XR']
    stopwords=['의','가','이','은','들','는','좀','꽤','주','잘','걍','과','도','를','으로','자','에','와','한','하','다','있']
    minus_discard_list = ['웃음', '남부럽', '탄복', '가슴', '기분', '개', '자식', '기집', '터지', '되', '오르', '만족', '속', '유쾌', '의심', '끼치', '치', '안정', '느끼']

    pos = []
    neg = []
    horror = []
    delight = []
    surprise = []
    angry = []
    sad = []
    boring = []
    happy = []
    minus2 = []
    minus3 = []

    # def __init__(self, text):
    #     self.text = text
    def __init__(self, data):
        self.content = data['text']
        self.title = data['title']
        self.emotions = []
        if data.get('stickers'):
            self.emotions = [
                sticker['emotion']['name'] for sticker in data['stickers']
            ]

    @classmethod
    def decompose(cls, ls):

        word_list = []

        for word in ls:
            if '+' in word[1]:
                if word[1].split('+')[0] in cls.tag and word[0] not in cls.stopwords:
                    word_list.append(word[0])
            elif word[1] in cls.tag and word[0] not in cls.stopwords:
                word_list.append(word[0])
        
        return set(word_list)

    @classmethod
    def get_pos(cls):
        if cls.pos:
            return cls.pos
        pos = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pos.txt'), "r", encoding="cp949").read().split('\n')        
        pos.pop()

        cls.pos = pos
        return pos
    
    @classmethod
    def get_neg(cls):
        if cls.neg:
            return cls.neg
        neg = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'neg.txt'), "r", encoding="cp949").read().split('\n')

        neg.pop()

        cls.neg = neg
        return neg

    @classmethod
    def get_horror(cls):
        if cls.horror:
            return cls.horror
        h = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'horror.txt'), encoding='UTF-8', names=['word'], sep='\n')
        horror = cls.decompose(cls.mecab.pos(' '.join(h.T.values[0])))

        for word in cls.minus_discard_list:
            horror.discard(word)
        
        cls.horror = horror
        return horror
    
    @classmethod
    def get_delight(cls):
        if cls.delight:
            return cls.delight
        d = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'delight.txt'), encoding='UTF-8', names=['word'], sep='\n')
        delight = cls.decompose(cls.mecab.pos(' '.join(d.T.values[0])))
        delight.discard('보')
        delight.discard('좋')
        delight.discard('재미있')
        cls.delight = delight
        return delight

    @classmethod
    def get_surprise(cls):
        if cls.surprise:
            return cls.surprise
        s = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'surprise.txt'), encoding='UTF-8', names=['word'], sep='\n')
        surprise = cls.decompose(cls.mecab.pos(' '.join(s.T.values[0])))
        surprise.discard('금')

        cls.surprise = surprise
        return surprise

    @classmethod
    def get_angry(cls):
        if cls.angry:
            return cls.angry
        a = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'angry.txt'), encoding='UTF-8', names=['word'], sep='\n')
        angry = cls.decompose(cls.mecab.pos(' '.join(a.T.values[0])))

        for word in cls.minus_discard_list:
            angry.discard(word)
        
        cls.angry = angry
        return angry

    @classmethod
    def get_sad(cls):
        if cls.sad:
            return cls.sad
        s = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sad.txt'), encoding='UTF-8', names=['word'], sep='\n')
        sad = cls.decompose(cls.mecab.pos(' '.join(s.T.values[0])))
        sad.add('싫')

        for word in cls.minus_discard_list:
            sad.discard(word)
        
        cls.sad = sad
        return sad

    @classmethod
    def get_boring(cls):
        if cls.boring:
            return cls.boring
        b = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'boring.txt'), encoding='UTF-8', names=['word'], sep='\n')
        boring = cls.decompose(cls.mecab.pos(' '.join(b.T.values[0])))

        cls.boring = boring
        return boring

    @classmethod
    def get_happy(cls):
        if cls.happy:
            return cls.happy
        h = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'happy.txt'), encoding='UTF-8', names=['word'], sep='\n')
        happy = cls.decompose(cls.mecab.pos(' '.join(h.T.values[0])))
        happy.discard('기분')
        happy.discard('속')

        cls.happy = happy
        return happy

    @classmethod
    def get_minus2(cls):
        if cls.minus2:
            return cls.minus2
        down2 = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'down2.txt'), encoding='UTF-8', names=['word'], sep='\n')
        minus2 = cls.decompose(cls.mecab.pos(' '.join(down2.T.values[0])))

        for word in cls.minus_discard_list:
            minus2.discard(word)
        
        cls.minus2 = minus2
        return minus2

    @classmethod
    def get_minus3(cls):
        if cls.minus3:
            return cls.minus3
        down3 = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'down3.txt'), encoding='UTF-8', names=['word'], sep='\n')
        minus3 = cls.decompose(cls.mecab.pos(' '.join(down3.T.values[0])))
        minus3.add('싫')

        for word in cls.minus_discard_list:
            minus3.discard(word)
        
        cls.minus3 = minus3
        return minus3

    def count_words(self):
        # 텍스트에서 명사만 추출하는 함수
        out = self.mecab.nouns(self.content)
        out_title = self.mecab.nouns(self.title)
        out += out_title
        for ch in out:
            if ch in self.stopwords:
                out.remove(ch)
        word_counts = Counter(out)
        
        sorted_word_counts = sorted(word_counts.items(), key=lambda x : x[1], reverse=True)
        
        for i in range(len(sorted_word_counts)):
            keyword = sorted_word_counts[i][0]
            if keyword in self.get_pos():
                sorted_word_counts[i] = list(sorted_word_counts[i])
                sorted_word_counts[i].append(1)
            elif keyword in self.get_delight():
                sorted_word_counts[i] = list(sorted_word_counts[i])
                sorted_word_counts[i].append(1)
            elif keyword in self.get_happy():
                sorted_word_counts[i] = list(sorted_word_counts[i])
                sorted_word_counts[i].append(1)
            elif keyword in self.get_neg():
                sorted_word_counts[i] = list(sorted_word_counts[i])
                sorted_word_counts[i].append(-1)
            elif keyword in self.get_minus2():
                sorted_word_counts[i] = list(sorted_word_counts[i])
                sorted_word_counts[i].append(-1)
            elif keyword in self.get_minus3():
                sorted_word_counts[i] = list(sorted_word_counts[i])
                sorted_word_counts[i].append(-1)
            else:
                sorted_word_counts[i] = list(sorted_word_counts[i])
                sorted_word_counts[i].append(0)
        
        return sorted_word_counts

    def calc_score(self, source, feel, cnt, score, p, n, is_title=False):
        additional_score = 0
        if is_title:
            additional_score = 1

        analyzed_source = self.mecab.pos(source)
        word_list = self.decompose(analyzed_source)
        for word in word_list:
            if word in self.get_delight():
                score += 2 + additional_score
                cnt += 2 + additional_score
                feel[self.emotion_idx['delight']] = feel.get(self.emotion_idx['delight'],0) + 1 + additional_score  
            elif word in self.get_happy():
                score += 3 + additional_score
                cnt += 3 + additional_score
                feel[self.emotion_idx['happy']] = feel.get(self.emotion_idx['happy'],0) + 1 + additional_score  
            elif word in self.get_minus2():
                score -= 2 + additional_score
                cnt += 2 + additional_score
                if word in self.get_horror():
                    feel[self.emotion_idx['horror']] = feel.get(self.emotion_idx['horror'],0) + 1 + additional_score  
                elif word in self.get_angry():
                    feel[self.emotion_idx['angry']] = feel.get(self.emotion_idx['angry'],0) + 1 + additional_score  
                elif word in self.get_sad():
                    feel[self.emotion_idx['sad']] = feel.get(self.emotion_idx['sad'],0) + 1 + additional_score
            elif word in self.get_minus3():
                score -= 3 + additional_score
                cnt += 3 + additional_score
                if word in self.get_horror():
                    feel[self.emotion_idx['horror']] = feel.get(self.emotion_idx['horror'],0) + 1 + additional_score
                elif word in self.get_angry():
                    feel[self.emotion_idx['angry']] = feel.get(self.emotion_idx['angry'],0) + 1 + additional_score
                elif word in self.get_sad():
                    feel[self.emotion_idx['sad']] = feel.get(self.emotion_idx['sad'],0) + 1 + additional_score  
            elif word in self.get_boring():
                feel[self.emotion_idx['boring']] = feel.get(self.emotion_idx['boring'], 0) + 1 + additional_score
            elif word in self.get_surprise():
                feel[self.emotion_idx['surprise']] = feel.get(self.emotion_idx['surprise'], 0) + 1 + additional_score
            elif word in self.get_pos():
                score += 1 + additional_score
                cnt += 1 + additional_score
                p.append(word)
            elif word in self.get_neg():
                score -= 1 + additional_score
                cnt += 1 + additional_score
                n.append(word)
        return (cnt, score)

    def day_score(self):
        cnt = 0
        score = 0
        p = []
        n = []

        feel = {}
        c1, s1 = self.calc_score(self.content, feel, cnt, score, p, n, is_title=False)
        c2, s2 = self.calc_score(self.title, feel, cnt, score, p, n, is_title=True)
        cnt = c1 + c2
        score = s1 + s2

        for emotion in self.emotions:
            if emotion and emotion != 'no_emotion':
                feel[self.emotion_idx[emotion]] = feel.get(self.emotion_idx[emotion], 0) + 2 
                if self.emotion_idx[emotion] in [1,3]:
                    score += 6
                    cnt += 6
                elif self.emotion_idx[emotion] in [2,5,7]:
                    score -= 6
                    cnt -= 6  
                    
        if cnt == 0:
            return cnt, feel
        return score/cnt, feel

    def text_analysis(self):
        # 일일 감정점수
        score, feel = self.day_score()
        # 일일 감정분류
        for key, value in feel.items():
            if score > 0:
                if key == self.emotion_idx['horror'] or key == self.emotion_idx['angry'] or key == self.emotion_idx['sad']:
                    feel[key] = 0
            elif score < 0:
                if key == self.emotion_idx['happy'] or key == self.emotion_idx['delight']:
                    feel[key] = 0
                    
        sorted_feel = sorted(feel.items(), key=lambda item:item[1], reverse=True)
        if len(sorted_feel) == 0:
            sorted_feel = [(4, 0)]
        # 단어 갯수 (wordcloud용)\
        # print('word count', self.count_words())
        word_count = self.count_words()
        return {
            "score": score,
            "feel": sorted_feel,
            "word_count": word_count
        }

if __name__ == "__main__":
    data = {
        'title' : 'Test',
        'text' : '''
        후하암 졸려
        ''',
        'stickers': []
    }
    a = TextAnalysis(data)
    b = a.text_analysis()
    print(b)
    feel = ""
    word_list = []
    if b['feel'][0][0] == 1 or b['feel'][0][0] == 3:
        feel = "행복"
    elif b['feel'][0][0] == 2:
        feel = "슬픔"
    elif b['feel'][0][0] == 4:
        feel = "지루"
    elif b['feel'][0][0] == 5:
        feel = "분노"
    elif b['feel'][0][0] == 6:
        feel = "공포"
    else:
        feel = "중립"
    print(feel)
    for num, i in enumerate(b['word_count']):
        word_list.append(i[0])
        if num>=2:
            break
    print(word_list)
    


