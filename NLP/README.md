# README

1. KoNLPy  품사 태깅 클래스 간 비교

   1. 로딩 시간 : 사전 로딩을 포함하여 클래스를 로딩하는 시간.
      - [`Kkma`](https://konlpy.org/ko/v0.4.3/api/konlpy.tag/#konlpy.tag._kkma.Kkma): 5.6988 *secs*
      - [`Komoran`](https://konlpy.org/ko/v0.4.3/api/konlpy.tag/#konlpy.tag._komoran.Komoran): 5.4866 *secs*
      - [`Hannanum`](https://konlpy.org/ko/v0.4.3/api/konlpy.tag/#konlpy.tag._hannanum.Hannanum): 0.6591 *secs*
      - [`Twitter`](https://konlpy.org/ko/v0.4.3/api/konlpy.tag/#konlpy.tag._twitter.Twitter): 1.4870 *secs*
      - [`Mecab`](https://konlpy.org/ko/v0.4.3/api/konlpy.tag/#konlpy.tag._mecab.Mecab): 0.0007 *secs*

   2. 실행 시간 : 10만 문자의 문서를 대상으로 각 클래스의 `pos` 메소드를 실행하는데 소요되는 시간.
      - [`Kkma`](https://konlpy.org/ko/v0.4.3/api/konlpy.tag/#konlpy.tag._kkma.Kkma): 35.7163 *secs*
      - [`Komoran`](https://konlpy.org/ko/v0.4.3/api/konlpy.tag/#konlpy.tag._komoran.Komoran): 25.6008 *secs*
      - [`Hannanum`](https://konlpy.org/ko/v0.4.3/api/konlpy.tag/#konlpy.tag._hannanum.Hannanum): 8.8251 *secs*
      - [`Twitter`](https://konlpy.org/ko/v0.4.3/api/konlpy.tag/#konlpy.tag._twitter.Twitter): 2.4714 *secs*
      - [`Mecab`](https://konlpy.org/ko/v0.4.3/api/konlpy.tag/#konlpy.tag._mecab.Mecab): 0.2838 *secs*

   3. 성능 분석
      - _`Mecab`_, _`Twitter`_가 가장 우수한 성능을 보여줌.

   

   *자세한 사항은 https://konlpy.org/ko/v0.4.3/morph/ 참조.*

   

2. 윈도우에서 mecab 간단 설치.

   - https://cleancode-ws.tistory.com/97 링크 참조
   - `mecab-ko-dic-msvs` : mecab-ko 기본 사전
   - `mecab-ko-msvc` : mecab을 윈도우에서 실행될 수 있게 컴파일 하는 역할.
   - mecab 폴더를 C:\ 위치로 옮기기.

   

3. python 에서 eunjeon 라이브러리 다운

   ```bash
   $ pip install eunjeon
   ```

