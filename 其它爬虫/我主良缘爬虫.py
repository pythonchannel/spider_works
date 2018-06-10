# coding:utf-8
import urllib2,urllib,requests
import os
import json
import sys
import xlwt
reload(sys)
sys.setdefaultencoding('utf-8')

class wzly(object):

    def __init__(self):
        self.gender = 0
        self.stargage = 0
        self.endgage = 0
        self.startheight = 0
        self.endheight = 0
        self.marry = 1
        self.salary = 0
        self.eduction = 0
        self.count = 1  #表示数据条数,这里先去掉第一行的标题，所以是从1开始
        self.f = None
        self.sheetInfo = None
        self.create_execl()
        pass

    def create_execl(self):
        '''创建Execl'''
        self.f = xlwt.Workbook() #创建工作薄
        self.sheetInfo = self.f.add_sheet(u'我主良缘',cell_overwrite_ok=True)
        rowTitle = [u'编号',u'昵称',u'性别',u'年龄',u'身高',u'籍贯',u'学历',u'内心独白',u'照片']
        # 填充标题
        for i in range(0, len(rowTitle)):
            self.sheetInfo.write(0, i, rowTitle[i])

    def query_data(self):
        '''
        筛选条件
        年龄，
        身高，
        教育，
        期望薪资,
        :return:
        '''
        raw_input('请输入你的筛选条件，直接回车可以忽略本筛选条件：')
        self.query_age()
        self.query_sex()
        self.query_height()
        self.query_money()
        print '你的筛选条件是年龄:{}-{}岁\n性别是:{}\n对方身高是:{}-{}\n对方月薪是:{}'.format(self.stargage,self.endgage,self.gender,self.startheight,self.endheight,self.salary)
        self.craw_data()

    def query_age(self):
        '''
        年龄筛选
        :return:
        '''
        try:
            age = input('请输入期望对方年龄,如:25:')         # int类型的输入
        except Exception as e:
            age = 0

        try:
            if 21 <= age <=30:
                self.stargage = 21
                self.endgage = 30
            elif 31<=age<=40:
                self.stargage = 31
                self.endgage = 40
            elif 41<=age<=50:
                self.stargage = 41
                self.endgage = 50
            else:
                self.stargage = 0
                self.endgage = 0
        except Exception as e:
            self.stargage = 0
            self.endgage = 0

    def query_sex(self):
        '''性别筛选'''
        try:
            sex = raw_input('请输入期望对方性别,如:女:')  # 字符串的输入
        except Exception as e:
            sex = '女'

        try:
           if sex == '男':
               self.gender = 1
           else:
               self.gender = 2

        except Exception as e:
           self.gender = 2

    def query_height(self):
        '''身高筛选'''
        try:
            height = input('请输入期望对方身高,如:162:')
        except Exception as e:
            height = 0

            try:
                if 151 <= height <= 160:
                    self.startheight = 151
                    self.endheight = 160
                elif 161 <= height <= 170:
                    self.startheight = 161
                    self.endheight = 170
                elif 171 <= height <= 180:
                    self.startheight = 171
                    self.endheight = 180
                elif 181 <= height <= 190:
                    self.startheight = 181
                    self.endheight = 190
                else:
                    self.startheight = 0
                    self.endheight = 0
            except Exception as e:
                self.startheight = 0
                self.endheight = 0

    def query_money(self):
        '''待遇筛选'''
        try:
            money = input('请输入期望的对方月薪,如:8000:')
        except Exception as e:
            money = 0


        try:
            if 2000 <= money <5000:
               self.salary = 2
            elif 5000 <= money < 10000:
                self.salary = 3
            elif 10000 <= money <= 20000:
                self.salary = 4
            elif 20000 <= money :
                self.salary = 5
            else:
                self.salary = 0
        except Exception as e:
            self.salary = 0

    def store_info(self, nick,age,height,address,heart,education,img_url):
        '''
        存照片,与他们的内心独白
        '''
        if age < 22:
            tag = '22岁以下'
        elif 22 <= age < 28:
            tag = '22-28岁'
        elif 28 <= age < 32:
            tag = '28-32岁'
        elif 32 <= age:
            tag = '32岁以上'
        filename = u'{}岁_身高{}_学历{}_{}_{}.jpg'.format(age,height,education, address, nick)

        try:
            # 补全文件目录
            image_path = u'E:/store/pic/{}'.format(tag)
            # 判断文件夹是否存在。
            if not os.path.exists(image_path):
                os.makedirs(image_path)
                print image_path + ' 创建成功'

            # 注意这里是写入图片，要用二进制格式写入。
            with open(image_path + '/' + filename, 'wb') as f:
                f.write(urllib.urlopen(img_url).read())

            txt_path = u'E:/store/txt'
            txt_name = u'内心独白.txt'
            # 判断文件夹是否存在。
            if not os.path.exists(txt_path):
                os.makedirs(txt_path)
                print txt_path + ' 创建成功'

            # 写入txt文本
            with open(txt_path + '/' + txt_name, 'a') as f:
                f.write(heart)
        except Exception as e:
            e.message

    def store_info_execl(self,nick,age,height,address,heart,education,img_url):
        person = []
        person.append(self.count)   #正好是数据条
        person.append(nick)
        person.append(u'女' if self.gender == 2 else u'男')
        person.append(age)
        person.append(height)
        person.append(address)
        person.append(education)
        person.append(heart)
        person.append(img_url)

        for j in range(len(person)):
            self.sheetInfo.write(self.count, j, person[j])

        self.f.save(u'我主良缘.xlsx')
        self.count += 1
        print '插入了{}条数据'.format(self.count)

    def parse_data(self,response):
        '''数据解析'''
        persons = json.loads(response).get('data').get('list')
        if persons is None:
            print '数据已经请求完毕'
            return

        for person in persons:
            nick = person.get('username')
            gender = person.get('gender')
            age = 2018 - int(person.get('birthdayyear'))
            address = person.get('city')
            heart = person.get('monolog')
            height = person.get('height')
            img_url = person.get('avatar')
            education = person.get('education')
            print nick,age,height,address,heart,education
            self.store_info(nick,age,height,address,heart,education,img_url)
            self.store_info_execl(nick,age,height,address,heart,education,img_url)

    def craw_data(self):
        '''数据抓取'''
        headers = {
            'Referer': 'http://www.lovewzly.com/jiaoyou.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4620.400 QQBrowser/9.7.13014.400'
        }
        page = 1
        while True:

            query_data = {
                'page':page,
                'gender':self.gender,
                'starage':self.stargage,
                'endage':self.endgage,
                'stratheight':self.startheight,
                'endheight':self.endheight,
                'marry':self.marry,
                'salary':self.salary,
            }
            url = 'http://www.lovewzly.com/api/user/pc/list/search?'+urllib.urlencode(query_data)
            print url
            req = urllib2.Request(url, headers=headers)
            response = urllib2.urlopen(req).read()
            # print response
            self.parse_data(response)
            page += 1


if __name__ == '__main__':
   wz = wzly()
   wz.query_data()




