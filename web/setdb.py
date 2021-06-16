def create_db():
    import sqlite3

    conn = sqlite3.connect("twitter.db", isolation_level=None)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS twitterdb \
        (time datetime, content text, likey integer, retweet integer, keyword text, feeling text)")

    # 이전 테이블 내용 삭제
    conn.execute("DELETE from twitterdb")
    conn.close()

    con = sqlite3.connect("naver.db", isolation_level=None)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS naver \
        (content text, title text, link text, postdate text, keyword text, feeling text)")

    # 이전 테이블 내용 삭제
    con.execute("DELETE from naver")
    con.close()


def twitterAPI(x, y, z):
    import tweepy
    import config
    import sqlite3

    conn = sqlite3.connect("twitter.db", isolation_level=None)
    c = conn.cursor()

    # 트위터 Application에서 발급 받은 key 정보들 문자열로 입력
    consumer_key = config.twitter_consumer_key
    consumer_secret = config.twitter_consumer_secret
    access_token = config.twitter_access_token
    access_token_secret = config.twitter_access_secret

    # 1. 핸들러 생성 및 개인정보 인증요청
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    # 2. 액세스 요청
    auth.set_access_token(access_token, access_token_secret)

    # 3. twitter API 생성
    api = tweepy.API(auth)

    keyword = str(x)
    feeling = str(z)
    result = []  # 크롤링 텍스트를 저장 할 리스트 변수

    for i in range(1, y + 1):  # 1,2 페이지 크롤링
        tweets = api.search(keyword)  # keyword 검색 실시. 결과가 tweets 변수에 담긴다.
        result = []
        for tweet in tweets:
            c.execute("INSERT INTO twitterdb (time, content, likey, retweet, keyword, feeling) \
                VALUES(?,?,?,?,?,?)",
                      (tweet.created_at, tweet.text, tweet.favorite_count, tweet.retweet_count, keyword, feeling))

    conn.close()


def naverBlogOpenAPI(x, y, z, w):
    import sqlite3
    import requests
    from urllib.parse import urlparse

    conn = sqlite3.connect("naver.db", isolation_level=None)
    c = conn.cursor()

    keyword = str(x)
    feeling = str(w)

    i = 1

    for i in range(1, y + 1):
        if i == 1:
            url = "https://openapi.naver.com/v1/search/blog?query=" + keyword + "&display=" + str(z) + "&start=" + str(
                i)
        elif i > 1:
            url = "https://openapi.naver.com/v1/search/blog?query=" + keyword + "&display=" + str(z) + "&start=" + str(
                (i - 1) * z + 1)

        result = requests.get(urlparse(url).geturl(),
                              headers={"X-Naver-Client-Id": "EJcURJ8Hx8GkYLFJxLWU",
                                       "X-Naver-Client-Secret": "pbyoqfSBIV"})

        json_data = result.json()

        for item in json_data['items']:
            li = item['link'].replace("<b>", "").replace("</b>", "")
            ti = item['title'].replace("<b>", "").replace("</b>", "")
            de = item['description'].replace("<b>", "").replace("</b>", "")
            po = item['postdate']

            c.execute("INSERT INTO naver (content, title, link, postdate, keyword, feeling) VALUES(?,?,?,?,?,?)",
                      (de, ti, li, po, keyword, feeling))

    conn.close()


# 디비 내용 갱신

def put_sad():
    feeling = '슬픔'
    naverBlogOpenAPI('힐링', 1, 15, feeling)  # (키워드, 1번, 15개씩, 감정)
    twitterAPI('힐링', 1, feeling)  # (키워드, 1번, 감정) 15개씩
    naverBlogOpenAPI('유머', 1, 15, feeling)
    twitterAPI('유머', 1, feeling)
    naverBlogOpenAPI('웃긴', 1, 15, feeling)
    twitterAPI('웃긴', 1, feeling)
    naverBlogOpenAPI('기분 좋아지는', 1, 15, feeling)
    twitterAPI('기분 좋아지는', 1, feeling)


def put_neutral():
    feeling = '중립'
    naverBlogOpenAPI('중립', 1, 15, feeling)
    twitterAPI('중립', 1, feeling)


def put_happy():
    feeling = '행복'
    naverBlogOpenAPI('행복', 1, 15, feeling)
    twitterAPI('행복', 1, feeling)


def put_anxious():
    feeling = '불안'
    naverBlogOpenAPI('안정', 1, 15, feeling)
    twitterAPI('안정', 1, feeling)
    naverBlogOpenAPI('좋은 글귀', 1, 15, feeling)
    twitterAPI('좋은 글귀', 1, feeling)
    naverBlogOpenAPI('힘나는', 1, 15, feeling)
    twitterAPI('힘나는', 1, feeling)


def put_angry():
    feeling = '분노'
    naverBlogOpenAPI('기분전환', 1, 15, feeling)
    twitterAPI('기분전환', 1, feeling)
    naverBlogOpenAPI('고양이', 1, 15, feeling)
    twitterAPI('고양이', 1, feeling)
    naverBlogOpenAPI('강아지', 1, 15, feeling)
    twitterAPI('강아지', 1, feeling)