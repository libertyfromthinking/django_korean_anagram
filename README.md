# Django Korean Anagram

http://freethinking.pythonanywhere.com/
학습용으로 만든 한글 아나그램입니다.
장고 웹서버를 기반으로 만들었습니다.

## 설치방법(우분투 18.04 기준)
가상환경을 설치합니다
```sh
$ python3 -m virtualenv .venv
```

가상환경을 활성화합니다
```sh
$ source .venv/bin/activate
```

git 저장소를 clone 합니다

```sh
$ git clone https://github.com/libertyfromthinking/django_korean_anagram.git
```

프로젝트 디렉토리로 이동 후 pip를 업데이트 합니다

```sh
$ cd django_korean_anagram
$ pip install -upgrade pip
```

requirements.txt 파일로 패키지들을 설치합니다

```sh
$ pip install -r requirements.txt
```

```sh
$ python3 manage.py makemigrations 
```

```sh
$ python3 manage.py migrate
```

```sh
$ python3 manage.py runserver
```

## 사용방법

### 1. 웹 브라우저 오픈 후 주소창에 localhost:8000 또는 127.0.0.1:8000
### 2. 아나그램할 이름 입력
