
# scrapy 프로젝트 모음

최종수정일: 2025-07-21

1. lottomax  

lottomax history 데이타를 가져오는 스크립트로 2009년부터 2025년까지 저장함.
저장은 MYSQL test DB에 저장
lottomax : 1등 및 보너스 번호 저장
countmax : 년도별 번호별 출력횟수 카운트


2. lotto649  

lotto649 history 데이타를 가져오는 스크립트로 1982년부터 2025년까지 저장함.
저장은 MYSQL test DB에 저장
lotto649 : 1등 및 보너스 번호 저장
count649 : 년도별 번호별 출력횟수 카운트


3. lotto

매일 또는 매주 로또 정보를 가져와서 저장하기

수행방법: 
1) CD H:\VENV\lotto\lotto
2) scrapy crawl lottodaily




# 인스톨

uv add scrapy  
uv pip install -e pkylib (로칼라이브러리)


# 순서

1. 프로젝트 폴더 생성
uv init <폴더명>
cd <폴더명>

2. 가상환경 설치
uv venv

3. scrapy 설치
uv add scrapy

4. 가상환경 실행
.venv\Scripts\activate

5. scrapy 프로젝트 만들기
scrapy startproject <프로젝트명>

6. scrapy 프로젝트 폴더로 이동
cd <프로젝트명>

7. 기본 스파이더 생성
scrapy genspider <스파이더명> <크롤링 도메인>

8. 스파이더 작성 시작
cd <프로젝트명>\spiders
<스파이더명>.py 파일을 열고 시작

9. 스파이더 시작
scrapy crawl <스파이더명>

10. 설정파일 수정
settings.py