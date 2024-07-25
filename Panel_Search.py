from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import pandas as pd
from Window_Edit import Window_Edit_User
from Window_Edit import Window_Edit_Book
from Window_Add import Window_Add_User
from Window_Add import Window_Add_Book
from PIL import Image
import os
from PIL import Image,ImageTk
from os import remove

WINDOW_GEOMETRY = '595x400'

SEARCH_ENTRY_WIDTH = 460
SEARCH_BTN_WIDTH = 100
SEARCH_HEIGHT = 24


SELECT_CANCEL_BTN_WIDTH = 81
BTN_WIDTH = 81

IMG_WIDTH = 120
IMG_HEIGHT = 160

INFO_BTN_Y = 315
LABEL_FOR_TABLE_Y = 340


DIR_CSV_USER = "csv/user.csv"
DIR_CSV_BOOK = "csv/book.csv"
DIR_CSV_RENT = "csv/rent.csv"

# =========================================================
# 클래스: 회원 검색 결과 윈도우
# =========================================================
class Panel_Search_User():
    # 생성자
    def __init__(self, window, x, y):
        self.load_widgets(self, window, x, y)
        self.load_table(self, window, x, y)

    def load_widgets(self, window, x, y):

        self.entry_search_user = Entry(window)
        self.entry_search_user.place(x=10, y=30, width=SEARCH_ENTRY_WIDTH, height=SEARCH_HEIGHT)
        self.entry_search_user.insert(0,window)

        self.btn_search_user = Button(window, text="검색", command=self.event_user_search)
        self.btn_search_user.place(x=SEARCH_ENTRY_WIDTH+20, y=30, width=SEARCH_BTN_WIDTH, height=SEARCH_HEIGHT)
        
        self.label_search_user = Label(window, text="회원 검색 결과: 0 개")
        self.label_search_user.place(x=10, y=75)

        self.btn_select_user = Button(window, text="선택", command=self.event_user_select)
        self.btn_select_user.place(x=400, y=360, width=SELECT_CANCEL_BTN_WIDTH)

        self.label_for_table = Label(text="[회원 정보]")
        self.label_for_table.place(x=x, y=y)

        self.label_for_table = Label(text="전체 조회: 입력 없이 [검색] 클릭", font=("맑은 고딕", 8), fg="red")
        self.label_for_table.place(x=x+238, y=y)

        self.entry_search_user = Entry(window)
        self.entry_search_user.place(x=x, y=y+30, width=SEARCH_ENTRY_WIDTH, height=SEARCH_HEIGHT)

        self.btn_search_user = Button(window, text="검색", command=self.event_user_search)
        self.btn_search_user.place(x=x+SEARCH_ENTRY_WIDTH+10, y=y+30, width=SEARCH_BTN_WIDTH, height=SEARCH_HEIGHT)

        self.btn_refresh_user = Button(window, text="새로고침", command=self.event_user_refresh)
        self.btn_refresh_user.place(x=x+240, y=y+INFO_BTN_Y, width=BTN_WIDTH)

        self.btn_save_user = None


        def clicked_table(event):
            select_Table = self.user_table.focus()
            self.getTable = self.user_table.item(select_Table).get('values')
        self.user_table.bind('<ButtonRelease-1>',clicked_table)
        self.event_user_search()

    # 멤버 메소드: 테이블 불러오기
    def load_table(self):
        column_tuple = ("전화번호", "이름", "생년월일", "성별", "이메일", "등록")
        width_tuple = (100, 70, 90, 50, 200, 60)

        self.user_table = ttk.Treeview(self.window, column=column_tuple, displaycolumns=column_tuple)
        self.user_table.place(x=10, y=100, height=240)

        # 컬럼(헤더) 설정
        for i in range(6):
            self.user_table.column(column_tuple[i], width=width_tuple[i], anchor="center")
            self.user_table.heading(column_tuple[i], text=column_tuple[i], anchor="center")

        self.user_table["show"] = "headings"    # 열 인덱스를 표시하지 않음
        self.scrollbar = Scrollbar(self.user_table, orient=HORIZONTAL)
        self.scrollbar.config() 

    # 멤버 메소드: [검색] 버튼 이벤트
    def event_user_search(self):
        # 테이블 초기화
        for item in self.user_table.get_children():
            self.user_table.delete(item)
        df_user = pd.read_csv(DIR_CSV_USER, encoding='CP949')
        df_user = df_user.set_index(df_user['USER_PHONE'])
        index_key = self.entry_search_user.get()
        try:
            int(index_key[0])
            condition = df_user[df_user["USER_PHONE"].str.contains(index_key)]
            count = 0
            for user_phone in condition["USER_PHONE"]:
                user_name = condition["USER_NAME"].loc[user_phone]
                user_birthday = condition["USER_BIRTH"].loc[user_phone]
                user_sex = condition["USER_SEX"].loc[user_phone]
                user_email = condition["USER_MAIL"].loc[user_phone]
                user_reg = condition["USER_REG"].loc[user_phone]
                user_add = (user_phone,user_name,user_birthday,user_sex,user_email,user_reg)
                self.user_table.insert("","end",text="",value=user_add,iid=user_add[0])
                count+=1
            self.label_search_user.config(text=f"회원 검색 결과: {count} 개")
        except:
            condition = df_user[df_user["USER_NAME"].str.contains(index_key)]
            count = 0
            for user_phone in condition["USER_PHONE"]:
                user_name = condition["USER_NAME"].loc[user_phone]
                user_birthday = condition["USER_BIRTH"].loc[user_phone]
                user_sex = condition["USER_SEX"].loc[user_phone]
                user_email = condition["USER_MAIL"].loc[user_phone]
                user_reg = condition["USER_REG"].loc[user_phone]
                user_add = (user_phone,user_name,user_birthday,user_sex,user_email,user_reg)
                self.user_table.insert("","end",text="",value=user_add,iid=user_add[0])
                
                count+=1
            self.label_search_user.config(text=f"회원 검색 결과: {count} 개")


    # 멤버 메소드: [선택] 버튼 이벤트
    def event_user_select(self):
        try:    
            messagebox.showinfo("회원 선택", f"{self.getTable[1]}({self.getTable[0]})를 선택하였습니다.")
            self.window.quit()
            self.window.destroy()
        except:
            messagebox.showinfo("회원 선택", "테이블을 선택해주세요!")

# =========================================================
# 클래스: 도서 검색 결과 윈도우
# =========================================================
class Panel_Search_Book():

    # 생성자
    def __init__(self, window, x, y):
        self.load_widgets(self, window, x, y)
        self.load_table(self, window, x, y)
        
    def load_widgets(self, window, x, y):
        self.label_for_table = Label(text="[도서 정보]")
        self.label_for_table.place(x=x, y=y)

        self.label_for_table = Label(text="전체 조회: 입력 없이 [검색] 클릭", font=("맑은 고딕", 8), fg="red")
        self.label_for_table.place(x=x+238, y=y)

        self.btn_refresh_book = Button(window, text="새로고침", command=self.event_user_refresh)
        self.btn_refresh_book.place(x=x+240, y=y+INFO_BTN_Y, width=BTN_WIDTH)

        self.btn_save_book = None

        self.entry_search_book = Entry(window)
        self.entry_search_book.place(x=10, y=30, width=SEARCH_ENTRY_WIDTH, height=SEARCH_HEIGHT)
        self.entry_search_book.insert(0,window)

        self.btn_search_book = Button(window, text="검색", command=self.event_book_search)
        self.btn_search_book.place(x=SEARCH_ENTRY_WIDTH+20, y=30, width=SEARCH_BTN_WIDTH, height=SEARCH_HEIGHT)
        
        self.label_search_book = Label(window, text="도서 검색 결과: 0 개")
        self.label_search_book.place(x=10, y=75)

        self.btn_select_book = Button(window, text="선택", command=self.event_book_select)
        self.btn_select_book.place(x=400, y=360, width=SELECT_CANCEL_BTN_WIDTH)

    # 멤버 메소드: 테이블 불러오기
    def load_table(self):
        column_tuple = ("ISBN", "도서명", "저자", "출판사")
        width_tuple = (140, 160, 160, 110)

        self.book_table = ttk.Treeview(self.window, column=column_tuple, displaycolumns=column_tuple)
        self.book_table.place(x=10, y=100, height=240)

        # 컬럼(헤더) 설정
        for i in range(4):
            self.book_table.column(column_tuple[i], width=width_tuple[i], anchor="center")
            self.book_table.heading(column_tuple[i], text=column_tuple[i], anchor="center")

        self.book_table["show"] = "headings"    # 열 인덱스를 표시하지 않음

        self.scrollbar = Scrollbar(self.book_table, orient=HORIZONTAL)
        self.scrollbar.config()

    # 멤버 메소드: [검색] 버튼 이벤트
    def event_book_search(self):
        # 테이블 초기화
        for item in self.book_table.get_children():
            self.book_table.delete(item)
        df_book = pd.read_csv(DIR_CSV_BOOK, encoding='CP949', dtype= {"BOOK_TITLE":object, "BOOK_AUTHOR":object, \
            "BOOK_PUB":object, "BOOK_DESCRIPTION": object, "BOOK_LINK": object})
        index_key = self.entry_search_book.get().strip()

        search_title_list = df_book["BOOK_TITLE"].str.contains(index_key)
        search_author_list = df_book["BOOK_AUTHOR"].str.contains(index_key)
        search_isbn = df_book[search_title_list | search_author_list]
        search_count = 0

        df_book.set_index(df_book["BOOK_ISBN"], inplace=True)
        for ISBN in list(search_isbn["BOOK_ISBN"]):
            book_title = df_book.loc[ISBN, "BOOK_TITLE"]
            book_author = df_book.loc[ISBN, "BOOK_AUTHOR"]
            book_publish = df_book.loc[ISBN, "BOOK_PUB"]
            book_add = (ISBN, book_title, book_author, book_publish)
            self.book_table.insert("","end",text="",value=book_add,iid=book_add[0])
            search_count += 1

        self.label_search_book.config(text=f"도서 검색 결과: {search_count} 개")

    # 멤버 메소드: [선택] 버튼 이벤트
    def event_book_select(self):
        try:    
            messagebox.showinfo("도서 선택", f"{self.getTable[1]}({self.getTable[0]})를 선택하였습니다.")
            self.window.quit()
            self.window.destroy()
        except:
            messagebox.showinfo("도서 선택", "테이블을 선택해주세요!", icon='error')

# =========================================================