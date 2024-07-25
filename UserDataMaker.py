import random
from datetime import date, timedelta
import calendar
import pandas as pd
import string

def get_rand_name():
    last_names = ["김", "이", "박", "최", "정", "강", "조", "윤", "장", "임", 
                  "한", "오", "서", "신", "권", "황", "안", "송", "류", "전", 
                  "홍", "고", "문", "양", "손", "배", "조", "백", "허", "유", 
                  "남", "심", "노", "정", "하", "곽", "성", "차", "주", "우",
                  "남궁", "황보", "제갈", "사공", "선우", "서문", "독고"]

    first_names = ["강", "건", "경", "고", "관", "나", "남", "노", "누", "다",
                   "단", "담", "대", "덕", "도", "동", "라", "래", "로", "루", 
                   "마", "만", "명", "무", "문", "미", "민", "백", "범", "별", 
                   "병", "보", "빛", "사", "산", "상", "새", "서", "석", "선", 
                   "아", "안", "애", "엄", "영", "예", "오", "옥", "완", "요", 
                   "자", "장", "재", "전", "정", "조", "종", "주", "준", "지", 
                   "찬", "창", "채", "천", "철", "초", "춘", "복", "치", "탐", 
                   "태", "택", "하", "한", "해", "혁", "현", "형", "혜", "호"]
    
    last_name = random.choice(last_names) 
    first_name = "".join(random.sample(first_names, 2))
    full_name = last_name + first_name
    
    return full_name

def get_rand_phone_number():
        numbers = "0123456789"
        num1 = "".join(random.sample(numbers, 4))
        num2 = "".join(random.sample(numbers, 4))
        
        phone_num = "010-{0}-{1}".format(num1, num2)
        
        return phone_num

def get_rand_birthday(start_year=1901, end_year=2021):
    rand_year = random.randint(start_year, end_year)
    rand_month = random.randint(1, 12)
    rand_date = random.randint(1, calendar.monthrange(rand_year, rand_month)[1])
    return str(rand_year).ljust(4, "0") + str(rand_month).rjust(2, "0") + str(rand_date).rjust(2, "0")


def get_rand_email():
    srting_pool = string.ascii_letters
    return ''.join(random.choice(srting_pool) for _ in range(12)) + "@test.com"

def get_rand_member_ID():
    alphabet_numbes = "abcdefghizklmnopqrstuvwxyz0123456789"
    digit = random.randint(4,10)
    
    while(True):
        member_ID = "".join(random.sample(alphabet_numbes, digit))
        if(member_ID[0] not in '0123456789'): 
            break                            
    
    return member_ID



def get_rand_sex():
     sexes = ["여", "남"]
     sex = random.choice(sexes)

     return sex
     
user_infos = []

for i in range(100):
     name = get_rand_name()
     phone_number = get_rand_phone_number()
     member_ID = get_rand_member_ID()
     email = get_rand_email()
     sex = get_rand_sex()
     birthday = get_rand_birthday()
     pw = birthday
     
     user_infos.append([name, phone_number, member_ID, email, sex, birthday, pw])

columns_name = ['이름', '휴대폰번호', '회원ID', '이메일주소', '성별', '생년월일', '비밀번호']
df = pd.DataFrame(user_infos, columns=columns_name)

csv_file_name = "users.csv"
df.to_csv(csv_file_name)