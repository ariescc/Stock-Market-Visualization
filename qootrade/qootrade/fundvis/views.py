import calendar
import csv
import json
import math

import requests
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

BASE_DIR = 'D:\python_scripts\qootrade\qootrade\static\dat\\'
FILE_DIR = ''

'''
HttpResponse属性
    content:返回内容，字符串类型
    charset: 相应的编码字符集
    status_code: Http响应的状态码
'''

'''
hello 为一个视图函数，每个视图函数第一个参数必须为request，即使用不到
request是django.http.HttpRequest的一个实例
'''
def hello(request):
    # context = {}
    # context['hello'] = 'hello,world' # 将模板中的hello替换为hello,world
    return render(request, 'hello.html', context=None)

def msg(request, name, age):
    return HttpResponse('My name is' + name + 'i am ' + age + 'years old!')


def hw1(request):

    # 读取world.csv数据
    cnod = {} # 累计确诊人数
    with open('D:\python_scripts\qootrade\qootrade\\fundvis\\templates\world.csv', 'r') as f:
        peos = []
        cnod = {} # 各国累计确诊人数
        xdata = []
        data = f.readlines()
        peos.append(data[0].split(',')[2])
        for idx in range(1, len(data)):
            if data[idx].split(',')[1] == data[idx-1].split(',')[1]:
                peos.append(data[idx].split(',')[2])
            else: # 之后的数据为新的国家
                cnod[data[idx-1].split(',')[1]] = peos
                peos = []
                peos.append(data[idx].split(',')[2])
        print(cnod)

        for idx in range(1, len(data)):
            if data[idx].split(',')[1] == data[idx-1].split(',')[1]:
                xdata.append(data[idx].split(',')[0])
            else:
                break

    return render(request, 'hw1.html', {'cnod': json.dumps(cnod), 'xdata': json.dumps(xdata) } )

def hw2(request):
    # 读取world.csv数据
    cnod = {} # 累计确诊人数
    with open('D:\python_scripts\qootrade\qootrade\\fundvis\\templates\world.csv', 'r') as f:
        peos = []
        cnod = {} # 各国累计确诊人数
        xdata = []
        data = f.readlines()
        peos.append(data[0].split(',')[2])
        for idx in range(1, len(data)):
            if data[idx].split(',')[1] == data[idx-1].split(',')[1]:
                peos.append(data[idx].split(',')[2])
            else: # 之后的数据为新的国家
                cnod[data[idx-1].split(',')[1]] = peos
                peos = []
                peos.append(data[idx].split(',')[2])
        print(cnod)

        for idx in range(1, len(data)):
            if data[idx].split(',')[1] == data[idx-1].split(',')[1]:
                xdata.append(data[idx].split(',')[0])
            else:
                break

    return render(request, 'hw2.html', {'cnod': json.dumps(cnod), 'xdata': json.dumps(xdata) } )

def MASystem(request, fundcode):
    
    with open('D:\python_scripts\qootrade\qootrade\\fundvis\\templates\dat\\' + fundcode + 'MA.csv', 'r') as f:
        xdata = [] # 时间轴
        dwjz = [] # 单位净值
        ma5 = []
        ma10 = []
        ma30 = []
        ma60 = []
        bias5 = []
        bias10 = []
        bias30 = []
        bias60 = []
        data = f.readlines()

        for idx in range(1, len(data)):
            blocks = data[idx].split(',')
            xdata.append(blocks[0])
            dwjz.append(blocks[1])
            ma5.append(blocks[4])
            bias5.append(blocks[5])
            ma10.append(blocks[6])
            bias10.append(blocks[7])
            ma30.append(blocks[8])
            bias30.append(blocks[9])
            ma60.append(blocks[10])
            bias60.append(blocks[11])
            

    return render(request, 'MASystem.html', {'xdata': json.dumps(xdata), 'dwjz': json.dumps(dwjz), 'ma5': json.dumps(ma5), 'ma10': json.dumps(ma10), 'ma30': json.dumps(ma30), 'ma60': json.dumps(ma60), \
        'bias5': json.dumps(bias5), 'bias10': json.dumps(bias10), 'bias30': json.dumps(bias30), 'bias60': json.dumps(bias60)})


def sectorFunds(request):
    # 今日板块资金流入数据
    url = 'http://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=500&po=1&np=1&fields=f14,f62&fid=f62&fs=m:90+t:2'
    # 5日板块资金流入数据
    url5 = 'http://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=500&po=1&np=1&fields=f14,f164&fid=f62&fs=m:90+t:2'
    # 10日板块资金流入数据
    url10 = 'http://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=500&po=1&np=1&fields=f14,f174&fid=f62&fs=m:90+t:2'
    res = requests.get(url)
    res5 = requests.get(url5)
    res10 = requests.get(url10)
    dt = json.loads(res.text)
    dt5 = json.loads(res5.text)
    dt10 = json.loads(res10.text)
    # print(dt['data']['diff'])

    print(dt5)
    print(dt10)

    # 将数据存入字典中
    dicz = {} # 当日正流入
    dicf = {} # 当日负流入
    dic5z = {} # 5日正流入
    dic5f = {} # 5日负流入
    dic10z = {} # 10日正流入
    dic10f = {} # 10日负流入
    
    for item in dt['data']['diff']:
        if item['f62'] >= 0:
            dicz[item['f14']] = item['f62']
        else:
            dicf[item['f14']] = item['f62']
        
    for item in dt5['data']['diff']:
        if item['f164'] >= 0:
            dic5z[item['f14']] = item['f164']
        else:
            dic5f[item['f14']] = item['f164']
    
    for item in dt10['data']['diff']:
        if item['f174'] >= 0:
            dic10z[item['f14']] = item['f174']
        else:
            dic10f[item['f14']] = item['f174']
    
    print(dicz)

    return render(request, 'sectorfunds.html', {'dicz': json.dumps(dicz), 'dicf': json.dumps(dicf), \
        'dic5z': json.dumps(dic5z), 'dic5f': json.dumps(dic5f), 'dic10z': json.dumps(dic10z), \
            'dic10f': json.dumps(dic10f)})


def movieClassification(request):
    with open('D:\python_scripts\qootrade\qootrade\\fundvis\imdb.csv', 'r') as f:
        data = []
        names = f.readline().split(',')[-28:-1] # 截取电影类型字段
        # print(names)
        countlist = [0 for col in range(len(names))]  # 各类型计数
        lines = f.readlines()
        for line in lines:
            blocks = line.split(',')[-28:-1]
            print(blocks)
            # 类别为1/0
            for idx in range(len(blocks)):
                if int(blocks[idx]) == 1:
                    countlist[idx] = countlist[idx] + 1
                else:
                    continue
        for idx in range(len(countlist)):
            dict = {}
            dict['name'] = names[idx]
            dict['value'] = countlist[idx]
            data.append(dict)
        print(data)

    return render(request, 'movieclassification.html', { 'data': json.dumps(data), 'names': json.dumps(names) })

def movieBar(request):
    with open('D:\python_scripts\qootrade\qootrade\\fundvis\imdb.csv', 'r') as f:
        names = f.readline().split(',')
        xdate = []
        start = 1881 # 起始年份
        lines = f.readlines()
        data = []
        tmp = [0 for col in range(len(names))]  # 指定年份区间内各类型影片的数量
        xdate.append(str(start)+'-'+str(start+9))
        for line in lines:
            end = start + 9
            blocks = line.split(',')[-36:-1]

            if start > 2020:
                break

            if int(blocks[0]) >= start and int(blocks[0]) <= end:
                for idx in range(8, len(blocks)):
                    if int(blocks[idx]) == 1:
                        tmp[idx-8] = tmp[idx-8] + 1
                        # print('bingo')
            else:
                # print(tmp)
                xdate.append(str(start)+'-'+str(end))
                data.append(tmp)
                tmp = [0 for col in range(len(names))]
                start = start + 10
                for idx in range(8, len(blocks)):
                    if int(blocks[idx]) == 1:
                        tmp[idx-8] = tmp[idx-8] + 1
        movieDict = []
        for y in range(len(data[0][:27])):
            temp = []
            dict = {}
            for x in range(len(data)):
                temp.append(data[x][y])
            dict['name'] = names[y]
            dict['type'] = 'bar'
            dict['stack'] = '影片'
            dict['data'] = temp
            movieDict.append(dict)

        # print(movieDict)
    return render(request, 'moviebar.html', { 'movieDict': json.dumps(movieDict), 'names': json.dumps(names[-28:-1]), \
                                              'xdate': json.dumps(xdate)})

def worldmap(request):
    return render(request, 'worldmap.html')

# 失业率
# def unemploymentRate(request):
#     data = [3.7,3.7,3.7,3.9,4,3.8,3.8,3.6,3.6,3.7,3.7,3.7,3.5,3.6,3.5,3.5,3.6,3.5,4.4,14.7]
#
#     return render(request, 'unemploymentRate.html', {'data': json.dumps(data)} )

# home首页
def home(request):
    return render(request, 'home.html')

def vix(request):
    # VIX数据
    data = [3.7, 3.7, 3.7, 3.9, 4, 3.8, 3.8, 3.6, 3.6, 3.7, 3.7, 3.7, 3.5, 3.6, 3.5, 3.5, 3.6, 3.5, 4.4, 14.7]

    with open(BASE_DIR + 'vix.csv', 'r') as f:
        line = f.readline()
        lines = f.readlines()
        xdata = []
        vals = []
        for line in lines:
            blocks = line.split(',')
            xdata.append(blocks[0])
            vals.append(blocks[1])

        print(xdata)
        print(vals)

    # 黄金ETF数据
    with open(BASE_DIR + '002611.csv', 'r') as f:
        lines = f.readlines()
        xAu = []
        valAu = []
        for line in lines:
            blocks = line.split(',')
            xAu.append(blocks[0])
            valAu.append(float(blocks[1])*40)


    return render(request, 'vix.html', { 'xdata': json.dumps(xdata[::-1]), 'vals': json.dumps(vals[::-1]), 'xAu': json.dumps(xAu), \
                                         'valAu': json.dumps(valAu), 'data': json.dumps(data)})


def globalData(request):
    # 读取各国股指数据
    # xAxis
    xAxis = [] # 日期轴
    china = []
    with open(BASE_DIR + 'index\china.csv') as f:
        lines = f.readlines()
        for line in lines:
            blocks = line.split(',')
            xAxis.append(blocks[0][5:])
            china.append(float('%.5f' % float(blocks[-1][:-2])))
    china = china[::-1]

    brazil = []
    with open(BASE_DIR + 'index\\brazil.csv') as f:
        lines = f.readlines()
        for line in lines:
            blocks = line.split(',')
            brazil.append(float('%.5f' % float(blocks[-1][:-2])))
    brazil = brazil[::-1]


    canada = []
    with open(BASE_DIR + 'index\\canada.csv') as f:
        lines = f.readlines()
        for line in lines:
            blocks = line.split(',')
            canada.append(float('%.5f' % float(blocks[-1][:-2])))
    canada = canada[::-1]

    eng = []
    with open(BASE_DIR + 'index\\eng.csv') as f:
        lines = f.readlines()
        for line in lines:
            blocks = line.split(',')
            eng.append(float('%.5f' % float(blocks[-1][:-2])))
    eng = eng[::-1]

    france = []
    with open(BASE_DIR + 'index\\france.csv') as f:
        lines = f.readlines()
        for line in lines:
            blocks = line.split(',')
            france.append(float('%.5f' % float(blocks[-1][:-2])))
    france = france[::-1]

    german = []
    with open(BASE_DIR + 'index\\german.csv') as f:
        lines = f.readlines()
        for line in lines:
            blocks = line.split(',')
            german.append(float('%.5f' % float(blocks[-1][:-2])))
    german = german[::-1]

    australia = []
    with open(BASE_DIR + 'index\\australia.csv') as f:
        lines = f.readlines()
        for line in lines:
            blocks = line.split(',')
            australia.append(float('%.5f' % float(blocks[-1][:-2])))
    australia = australia[::-1]

    italy = []
    with open(BASE_DIR + 'index\\italy.csv') as f:
        lines = f.readlines()
        for line in lines:
            blocks = line.split(',')
            italy.append(float('%.5f' % float(blocks[-1][:-2])))
    italy = italy[::-1]

    japan = []
    with open(BASE_DIR + 'index\\japan.csv') as f:
        lines = f.readlines()
        for line in lines:
            blocks = line.split(',')
            japan.append(float('%.5f' % float(blocks[-1][:-2])))

    korea = []
    with open(BASE_DIR + 'index\\korea.csv') as f:
        lines = f.readlines()
        for line in lines:
            blocks = line.split(',')
            korea.append(float('%.5f' % float(blocks[-1][:-2])))
    japan = japan[::-1]

    nsdk = []
    with open(BASE_DIR + 'index\\nsdk.csv') as f:
        lines = f.readlines()
        for line in lines:
            blocks = line.split(',')
            nsdk.append(float('%.5f' % float(blocks[-1][:-2])))
    nsdk = nsdk[::-1]

    russia = []
    with open(BASE_DIR + 'index\\russia.csv') as f:
        lines = f.readlines()
        for line in lines:
            blocks = line.split(',')
            russia.append(float('%.5f' % float(blocks[-1][:-2])))
    russia = russia[::-1]

    india = []
    with open(BASE_DIR + 'index\\india.csv') as f:
        lines = f.readlines()
        for line in lines:
            blocks = line.split(',')
            india.append(float('%.5f' % float(blocks[-1][:-2])))
    india = india[::-1]

    southafrica = []
    with open(BASE_DIR + 'index\\southafrica.csv') as f:
        lines = f.readlines()
        for line in lines:
            blocks = line.split(',')
            southafrica.append(float('%.5f' % float(blocks[-1][:-2])))
    southafrica = southafrica[::-1]

    inni = []
    with open(BASE_DIR + 'index\\inni.csv') as f:
        lines = f.readlines()
        for line in lines:
            blocks = line.split(',')
            inni.append(float('%.5f' % float(blocks[-1][:-2])))
    inni = inni[::-1]

    data = [] # 按日期存储，每一组为各国当天的股指数据
    for idx in range(len(xAxis)):
        tmp = []
        dict = {
            'name': '巴西',
            'value': brazil[idx]
        }
        tmp.append(dict)
        dict = {
            'name': '加拿大',
            'value': canada[idx]
        }
        tmp.append(dict)
        dict = {
            'name': '中国',
            'value': china[idx]
        }
        tmp.append(dict)
        dict = {
            'name': '英国',
            'value': eng[idx]
        }
        tmp.append(dict)
        dict = {
            'name': '法国',
            'value': france[idx]
        }
        tmp.append(dict)
        dict = {
            'name': '德国',
            'value': german[idx]
        }
        tmp.append(dict)
        dict = {
            'name': '澳大利亚',
            'value': australia[idx]
        }
        tmp.append(dict)
        dict = {
            'name': '意大利',
            'value': italy[idx]
        }
        tmp.append(dict)
        dict = {
            'name': '日本',
            'value': japan[idx]
        }
        tmp.append(dict)
        dict = {
            'name': '韩国',
            'value': korea[idx]
        }
        tmp.append(dict)
        dict = {
            'name': '美国',
            'value': nsdk[idx]
        }
        tmp.append(dict)
        dict = {
            'name': '俄罗斯',
            'value': russia[idx]
        }
        tmp.append(dict)
        dict = {
            'name': '印度',
            'value': india[idx]
        }
        tmp.append(dict)
        dict = {
            'name': '南非',
            'value': southafrica[idx]
        }
        tmp.append(dict)
        dict = {
            'name': '印度尼西亚',
            'value': inni[idx]
        }
        tmp.append(dict)
        data.append(tmp)

    print(data)



    return render(request, 'globalData.html', { 'data': json.dumps(data), 'xAxis': json.dumps(xAxis[::-1]) })


'''
展示各国股指的详细走势
'''
def stockIndex(request):

    china = []
    with open(BASE_DIR+'stockindex\china.csv', 'r') as f:
        bt = f.readline()
        lines = f.readlines()
        for line in lines:
            blocks = line.split(',')
            tmp = [blocks[0], float(blocks[1]), float(blocks[2]), float(blocks[4]), float(blocks[3])]
            china.append(tmp)
    china = china[::-1]

    usa = []
    with open(BASE_DIR + 'stockindex\\usa.csv', 'r') as f:
        bt = f.readline()
        lines = f.readlines()
        for line in lines:
            blocks = line.split(',')
            tmp = [blocks[0], float(blocks[1]), float(blocks[2]), float(blocks[4]), float(blocks[3])]
            usa.append(tmp)
    usa = usa[::-1]

    brazil = []
    with open(BASE_DIR + 'stockindex\\brazil.csv', 'r') as f:
        bt = f.readline()
        lines = f.readlines()
        for line in lines:
            blocks = line.split(',')
            tmp = [blocks[0], float(blocks[1]), float(blocks[2]), float(blocks[4]), float(blocks[3])]
            brazil.append(tmp)
    brazil = brazil[::-1]

    japan = []
    with open(BASE_DIR + 'stockindex\japan.csv', 'r') as f:
        bt = f.readline()
        lines = f.readlines()
        for line in lines:
            blocks = line.split(',')
            tmp = [blocks[0], float(blocks[1]), float(blocks[2]), float(blocks[4]), float(blocks[3])]
            japan.append(tmp)
    japan = japan[::-1]

    italy = []
    with open(BASE_DIR + 'stockindex\italy.csv', 'r') as f:
        bt = f.readline()
        lines = f.readlines()
        for line in lines:
            blocks = line.split(',')
            tmp = [blocks[0], float(blocks[1]), float(blocks[2]), float(blocks[4]), float(blocks[3])]
            italy.append(tmp)
    italy = italy[::-1]

    australia = []
    with open(BASE_DIR + 'stockindex\\australia.csv', 'r') as f:
        bt = f.readline()
        lines = f.readlines()
        for line in lines:
            blocks = line.split(',')
            tmp = [blocks[0], float(blocks[1]), float(blocks[2]), float(blocks[4]), float(blocks[3])]
            australia.append(tmp)
    australia = australia[::-1]

    eng = []
    with open(BASE_DIR + 'stockindex\eng.csv', 'r') as f:
        bt = f.readline()
        lines = f.readlines()
        for line in lines:
            blocks = line.split(',')
            tmp = [blocks[0], float(blocks[1]), float(blocks[2]), float(blocks[4]), float(blocks[3])]
            eng.append(tmp)
    eng = eng[::-1]

    france = []
    with open(BASE_DIR + 'stockindex\\france.csv', 'r') as f:
        bt = f.readline()
        lines = f.readlines()
        for line in lines:
            blocks = line.split(',')
            tmp = [blocks[0], float(blocks[1]), float(blocks[2]), float(blocks[4]), float(blocks[3])]
            france.append(tmp)
    france = france[::-1]

    germany = []
    with open(BASE_DIR + 'stockindex\germany.csv', 'r') as f:
        bt = f.readline()
        lines = f.readlines()
        for line in lines:
            blocks = line.split(',')
            tmp = [blocks[0], float(blocks[1]), float(blocks[2]), float(blocks[4]), float(blocks[3])]
            germany.append(tmp)
    germany = germany[::-1]

    korea = []
    with open(BASE_DIR + 'stockindex\korea.csv', 'r') as f:
        bt = f.readline()
        lines = f.readlines()
        for line in lines:
            blocks = line.split(',')
            tmp = [blocks[0], float(blocks[1]), float(blocks[2]), float(blocks[4]), float(blocks[3])]
            korea.append(tmp)
    korea = korea[::-1]

    russia = []
    with open(BASE_DIR + 'stockindex\\russia.csv', 'r') as f:
        bt = f.readline()
        lines = f.readlines()
        for line in lines:
            blocks = line.split(',')
            tmp = [blocks[0], float(blocks[1]), float(blocks[2]), float(blocks[4]), float(blocks[3])]
            russia.append(tmp)
    russia = russia[::-1]

    canada = []
    with open(BASE_DIR + 'stockindex\canada.csv', 'r') as f:
        bt = f.readline()
        lines = f.readlines()
        for line in lines:
            blocks = line.split(',')
            tmp = [blocks[0], float(blocks[1]), float(blocks[2]), float(blocks[4]), float(blocks[3])]
            canada.append(tmp)
    canada = canada[::-1]


    return render(request, 'stockindex.html', { 'china': json.dumps(china), 'usa': json.dumps(usa), 'brazil': json.dumps(brazil), \
                                                'japan': json.dumps(japan), 'italy': json.dumps(italy), 'australia': json.dumps(australia), \
                                                'eng': json.dumps(eng), 'france': json.dumps(france), 'germany': json.dumps(germany), \
                                                'korea': json.dumps(korea), 'russia': json.dumps(russia), 'canada': json.dumps(canada)})

#行业日净流入
def industry(request):
    list = ['农业','石油化工','医药制造业','通用设备制造业','航空运输业','保险业','房地产业','黄金','货币金融服务','计算机']
    timeline = [] #存放三月每天日期的列表
    year = 2020
    month = 3
    #计算三月的所有日期，放入timeline中
    for i in range(calendar.monthrange(year, month)[1] + 1)[1:]:
        str1 = str(year) + str("-%02d" % month) + str("-%02d" % i)
        timeline.append(str1)
    remove_list = [1,7,8,14,15,21,22,28,29]
    for number in remove_list:
        timeline.remove('2020-03-%02d'%number)
    data = {key : [] for key in timeline}
    with open(BASE_DIR + 'industry.csv', 'r') as f:
        f.seek(1) #切换到第二行
        reader = csv.DictReader(f) #以字典形式读取
        for row in reader:
            if row['industryName'] in list:
                data[row['updateTime'].split(' ')[0]].append(int(float(row['netMoneyInflow']) / 100000000))
    return render(request, 'industryMoneyFlow.html', {'timeline' : json.dumps(timeline), 'data': json.dumps(data), 'xAxis' : json.dumps(list)})


#纳斯达克折线图
def nsdkMethod(request):
    xAxis = []
    data = []
    with open(BASE_DIR + '纳斯达克100指数历史数据.csv', 'r', encoding='utf-8', errors='ignore') as f:
        f.seek(1)
        reader = csv.DictReader(f)
        for row in reader:
            if row['日期'] == '2020年2月6日':
                break
            time = row['日期']
            closeSale = row['收盘']
            xAxis.append(time.split('年')[1].strip('日').replace('月','.'))
            data.append(float(closeSale.split(',')[0] + closeSale.split(',')[1]))
        print(data)
            # print(list[1].strip('"') +  list[2].strip('"'))
    return render(request, 'nsdk.html', {'xAxis' : json.dumps(xAxis[::-1]), 'data' : json.dumps(data[::-1])})