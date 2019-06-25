from django.shortcuts import render
from django.views.generic import DetailView, TemplateView, ListView
from .models import *

from django.views.generic.edit import FormView
from .forms import AnagramForm

import itertools
# Create your views here.

# class AnagramTV(TemplateView):
#     Model = Anagram
#     template_name = 'my_anagram/main.html'

# class AnagramDV(DetailView):
#     Model = Anagram

# 초성 리스트. 00 ~ 18
CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
# 중성 리스트. 00 ~ 20
JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
# 종성 리스트. 00 ~ 27 + 1(1개 없음)
JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

## 문자열 s1, s2 아나그램 관계 비교
def anagramSolution1(s1,s2):    
    alist = list(s2)    ## 문자열 s2를 리스트화 alist, None값 넣기 위함

    pos1 = 0    ## 문자열 s1의 인덱스를 나타내는 pos1 변수
    stillOK = True      ## 문자열 s1 s2가 아나그램관계인지 확인2

    ## 인덱스변수가 문자열의 길이보다 작은지 확인하는 반복문
    while pos1 < len(s1) and stillOK:
        pos2 = 0    ## 문자열 s2, 즉 alist의 인덱스변수 pos2
        found = False   ## s1과 alist가 같을 때 True를 갖는 변수   
        while pos2 < len(alist) and not found:  ## s2의 인덱스변수 pos2가 s2의 길이보다 작고 found가 False일때 실행, 
            if s1[pos1] == alist[pos2]:     ## s1과 s2의 인덱스의 문자가 같으면
                found = True    ## found에 True 값 삽입, 반복문 탈출
            else:           ## s1과 s2가 같지 않으면, 반복문 계속됨
                pos2 = pos2 + 1     ## s2의 인덱스변수 pos2 + 1

        if found:           ## found 가 참일때, s1과 s2가 같을 때                  
            alist[pos2] = None  ## s1과 s2가 같으면 s2의 해당 인덱스에 None값 삽입, 해당 값을 없앰
        else:               ## found 가 거짓이면, s1과 s2가 달라서 s2의 인덱스를 다 훑고 반복문에서 빠져 나왔을 때
            stillOK = False     ## s1과 s2가 anagram관계임을 나타내는 변수에 False삽입, s2의 루프에서 s1이 하나도 나오지 않으면 anagram 관계 아님

        pos1 = pos1 + 1     ## s1의 인덱스변수 pos1 + 1

    return stillOK      ## anagram 관계를 나타내는 stillOK 반환

def korean_to_be_englished(korean_word):
    r_lst = []
    for w in list(korean_word.strip()):
        ## 영어인 경우 구분해서 작성함. 
        if '가'<=w<='힣':
            ## 588개 마다 초성이 바뀜. 
            ch1 = (ord(w) - ord('가'))//588
            ## 중성은 총 28가지 종류
            ch2 = ((ord(w) - ord('가')) - (588*ch1)) // 28
            ch3 = (ord(w) - ord('가')) - (588*ch1) - 28*ch2
            r_lst.append(CHOSUNG_LIST[ch1])
            r_lst.append(JUNGSUNG_LIST[ch2])
            if ch3: 
                r_lst.append(JONGSUNG_LIST[ch3])    
        else:
            r_lst.append(w)
    return r_lst

# ㅂ 12610->48148 (CHOSUNG_LIST.index(c)*588)+ord('가')
# ㅏ 12623->48148 (JUNGSUNG_LIST.index(c)*28) + (ord('가') + (588*(이전의 초성인덱스)))
# ㄱ 12593 (JONGSUNG_LIST.index(c)+(28*이전의 중성인덱스)) + (588*(이전의 초성인덱스)) + ord('가')

# 자음모음 하나하나를 튜플로 받아 재조합, 문자열로 리턴
def combine_letter(c):
    nlist = ''      ## 리턴할 문자열
    i=1     ## 첫번째 모음의 인덱스, 하나의 음절을 인식하는데 사용
    while i<len(c):     
        if i==len(c)-1:
            nlist += chr(JUNGSUNG_LIST.index(c[i])*28 + ord('가')+(588*(CHOSUNG_LIST.index(c[i-1]))))   ## 중성
            break
        else:
            i = i+1
            if i==len(c)-1:
                nlist += chr(JONGSUNG_LIST.index(c[i])+(28*JUNGSUNG_LIST.index(c[i-1])) + (588*(CHOSUNG_LIST.index(c[i-2]))) + ord('가'))   ## 종성
                break
            else:
                if c[i+1] in JUNGSUNG_LIST:
                    nlist += chr(JUNGSUNG_LIST.index(c[i-1])*28 + ord('가') + (588*(CHOSUNG_LIST.index(c[i-2]))))   ## 중성
                    i = i+1
                else:
                    nlist += chr(JONGSUNG_LIST.index(c[i])+(28*JUNGSUNG_LIST.index(c[i-1])) + (588*(CHOSUNG_LIST.index(c[i-2]))) + ord('가'))   ## 종성
                    i = i+2
    return nlist

# 리스트내의 문자열들 중복제거
def remove_duplicates(li):
    my_set = set()
    res = []
    for i in li:
        if i not in my_set:
            res.append(i)
            my_set.add(i)
    return res

# 자모의 배열 순서에 맞는 문자열만 리스트에 추가       
def case_of_word(word):
    wlist = []
    for perm in itertools.permutations(word):
        i = 0
        while i<len(perm):
            if perm[i] in CHOSUNG_LIST:
                if i==len(perm)-1:
                    break
                i = i+1
                if perm[i] in JUNGSUNG_LIST:
                    if i==len(perm)-1:
                        wlist.append(perm)
                        break
                    else:
                        i=i+1
                        if i==len(perm)-1:
                            if perm[i] in JONGSUNG_LIST:
                                wlist.append(perm)
                                break
                            else:break
                        elif perm[i+1] in JUNGSUNG_LIST:
                            pass
                        else:
                            if perm[i] in JONGSUNG_LIST:
                                i=i+1
                            else:break              
                else:break
            else:break
    return wlist

class SearchFormView(FormView):
    form_class = AnagramForm
    template_name = 'my_anagram/main.html'
    
    def form_valid(self, form):
        name = '%s' % self.request.POST['search_word']
        s1 = korean_to_be_englished(name) 
        slist = case_of_word(s1)
        object_list = remove_duplicates(list(map(combine_letter, slist)))       
        object_num = len(object_list)

        context = {}
        context['object_list'] = remove_duplicates(list(map(combine_letter, slist)))       
        context['object_num'] = object_num
        context['form'] = form
        context['search_term'] = name

        return render(self.request, self.template_name, context)