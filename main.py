from tkinter import *
from recommander import *
import random

class NewWindow():

    def __init__(self,title, entry=None):
        if entry is not None:
            entry.delete(0, 'end')
        if title.strip() != '':
            self.newWindow = Toplevel(root)
            #self.newWindow.overrideredirect(1)
            self.newWindow.title("Movie Recommendation")
            #self.newWindow.geometry("200x500")
            self.newWindow.focus_force()

            self.newWindow.bind("<Escape>", self.callback)
            self.newWindow.bind("<Return>", self.callback)
            Label(self.newWindow,
                  text="추천 영화").pack()

            Label(self.newWindow, text="------Press Enter to Close------").pack(side=BOTTOM)
            txt = Text(self.newWindow, width=50,  wrap=WORD)
            txt.pack()
            try:
                top10_similar_movies = get_similar_movies(title)

                for t in top10_similar_movies:
                    txt.insert(0.0, t + "\n")
            except:
                txt.insert(0.0, "검색하신 영화가 없습니다. \n다시 입력해주세요.")

    def callback(self, event):
        print("pressed")
        self.newWindow.destroy()



class main():

    def __init__(self, master):
        frame1 = Frame(master, borderwidth=5)
        frame1.pack(fill="both", expand=True)
        self.et1 = Entry(frame1, width = 30)
        self.et1.insert(0, '영화이름을 직접 입력하셔도 됩니다.')
        self.et1.pack(padx=5, pady=5,side=LEFT,expand=True)
        self.et1.bind("<Return>", self.onReturn)
        #self.et1.bind("<Escape>", self.onReturn)
        self.et1.bind("<Button-1>", self.clearValue)


        frame2 = Frame(master, borderwidth=5)
        frame2.pack(fill="both",expand=True)
        refresh = Button(frame2, text='새로고침', command=lambda: self.clearFrame(frame2,frame3, master), width = 10, height = 2)
        refresh.pack(side=LEFT,expand=True)
        search = Button(frame2, text='종료',bg= 'red4',fg='white', command=master.destroy, width = 10, height = 2)
        search.pack(side=LEFT,expand=True)
        search = Button(frame2, text='추천영화 검색',bg= 'dark green',fg='snow2', width = 10, height = 2,  command=lambda: NewWindow(self.et1.get(), entry=self.et1))
        search.pack(side=LEFT,expand=True)

        titles = df['title'].tolist()
        titles = random.sample(titles, 25)
        frame3 = Frame(master, borderwidth=5)
        frame3.pack(expand=True)
        for title in titles:
            btn = Button(frame3, text=title, bg='purple', fg='white',
                         command=lambda title=title: NewWindow(title))
            btn.pack()

        frame4 = Frame(master,bg='gray', borderwidth=5)
        frame4.pack(side=BOTTOM,fill="both", expand=True)
        Label(frame4,bg='gray',text="Copyright © 2021. Sangyub Han. All rights reserved \ngkstkdduq1@gmail.com").pack()


    def clearFrame(self, frame2,frame3, master):
        frame2.destroy()
        frame3.destroy()
        frame2 = Frame(master, borderwidth=5)
        frame2.pack(fill="both", expand=True)
        refresh = Button(frame2, text='새로고침', command=lambda: self.clearFrame(frame2, frame3, master), width=10,
                         height=2)
        refresh.pack(side=LEFT, expand=True)
        search = Button(frame2, text='종료', bg='red4', fg='white', command=master.destroy, width=10, height=2)
        search.pack(side=LEFT, expand=True)
        search = Button(frame2, text='추천영화 검색', bg='dark green', fg='snow2', width=10, height=2,
                        command=lambda: NewWindow(self.et1.get(), entry=self.et1))
        search.pack(side=LEFT, expand=True)

        titles = df['title'].tolist()
        titles = random.sample(titles, 25)
        frame3 = Frame(master, borderwidth=5)
        frame3.pack(fill="both", expand=True)
        for title in titles:
            btn = Button(frame3, text=title, bg='purple', fg='white',
                         command=lambda title=title: NewWindow(title))
            btn.pack(side=BOTTOM)

    def clearValue(self, event):
        print("return pressed")
        self.et1.delete(0, 'end')

    def onReturn(self, event):
        print("return pressed")
        if self.et1.get() != "":
            NewWindow(self.et1.get(), entry=self.et1)


if __name__ == '__main__':
    root = Tk()
    root.focus_force()
    root.title("Movie Recommendation")

    main(root)
    root.mainloop()
