import csv
import jieba
import re
import jieba.posseg as psg
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from scipy.misc import imread
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY, YEARLY
'''
matplotlib.pyplot中add_subplot(111, projection='3d')报错ValueError: Unknown projection '3d'时，检查matplotlib版本在1.0.x以上时导入from mpl_toolkits.mplot3d import Axes3D就解决问题了
'''
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib.collections import PolyCollection
import random
from matplotlib import animation


class wordItem:
    label = ''
    times = 0
    # 构造函数

    def __init__(self, l, t):
        self.label = l
        self.times = t
    # 用于比较

    def __lt__(self, other):
        return self.times < other.times


class Seg:
    def __init__(self, *args, **kwargs):
        pass

    def userDictAppend(self):
        with open('out/cqu_info_list.csv', 'r', encoding='utf-8') as cf:
            cr = csv.reader(cf, delimiter='\t')
            line = 0
            segArr = []
            with open('userdict.txt', 'a+', encoding='utf-8') as f:
                for row in cr:
                    if(line == 0):
                        line += 1
                        continue
                    for i in range(0, len(row)):
                        f.write(row[i] + ' 20 nz\n')
                        if i == 2:
                            segList = jieba.cut(row[i], cut_all=False)
                            for seg in segList:
                                if re.match('^[0-9’!"#$%&\'()*+,-./:：（）;<=>?@，。?★、…【】《》～；？“”‘’！[\\]^_`{|}~\s]+$', seg) != None:
                                    continue
                                try:
                                    index = segArr.index(seg)
                                except:
                                    if(seg == row[i]):
                                        continue
                                    segArr.append(seg)
                                    f.write(seg+' 10 nz\n')

    def segByMon(self):
        jieba.load_userdict('dict/userdict.txt')
        # jieba.enable_parallel(4)
        for y in range(6, 10):
            for m in range(1, 13):
                year = str(y)
                mon = ''
                if(m < 10):
                    mon = '0'+str(m)
                else:
                    mon = str(m)
                filename = '201'+year+'-'+mon
                try:
                    with open('out/'+filename+'.txt', 'r', encoding='utf-8') as f:
                        text = f.read()
                        # segList = jieba.cut(text, cut_all=False)
                        segList = psg.cut(text)
                        wordCount = {}
                        for segg in segList:
                            seg = segg.word
                            # 过滤字符，过滤连词、叹词、副词、方位词、数词、拟声词、介词、代词、助词、标点符号、语气词
                            if re.match('^[0-9’!"#$%&\'()*+,-./:：（）;<=>?@，。?★、…【】《》～；？“”‘’！[\\]^_`{|}~\s]+$', seg) != None or re.match('^[cedfmopruwy]', segg.flag) != None:
                                continue
                            if seg not in wordCount:
                                wordCount[seg] = 1
                            else:
                                wordCount[seg] += 1
                        wordItemArray = []
                        for key in wordCount:
                            wordItemArray.append(wordItem(key, wordCount[key]))
                            # 按词频由高到低倒序排列
                            wordItemArray.sort(reverse=True)

                        with open('out/stat/'+filename+'.csv', 'w', encoding='utf-8') as fs:
                            fs.write('word\tcount\n')
                            for item in wordItemArray:
                                fs.write(item.label+'\t'+str(item.times)+'\n')
                except IOError:
                    print('File Not Exists')

    def segAll(self):
        jieba.load_userdict('dict/userdict.txt')
        # jieba.enable_parallel(4)
        text = ''
        for y in range(6, 10):
            for m in range(1, 13):
                year = str(y)
                mon = ''
                if(m < 10):
                    mon = '0'+str(m)
                else:
                    mon = str(m)
                filename = '201'+year+'-'+mon
                try:
                    with open('out/'+filename+'.txt', 'r', encoding='utf-8') as f:
                        text += f.read()
                        # segList = jieba.cut(text, cut_all=False)
                except IOError:
                    print('File Not Exists')
                    continue
        segList = psg.cut(text)
        wordCount = {}
        for segg in segList:
            seg = segg.word
            # 过滤字符，过滤连词、叹词、副词、方位词、数词、拟声词、介词、代词、助词、标点符号、语气词
            if re.match('^[0-9’!"#$%&\'()*+,-./:：（）;<=>?@，。?★、…【】《》～；？“”‘’！[\\]^_`{|}~\s]+$', seg) != None or re.match('^[cedfmopruwy]', segg.flag) != None:
                continue
            if seg not in wordCount:
                wordCount[seg] = 1
            else:
                wordCount[seg] += 1
        wordItemArray = []
        for key in wordCount:
            wordItemArray.append(wordItem(key, wordCount[key]))
            # 按词频由高到低倒序排列
            wordItemArray.sort(reverse=True)

        with open('out/stat/allCount.csv', 'w', encoding='utf-8') as fs:
            fs.write('word\tcount\n')
            for item in wordItemArray:
                fs.write(item.label+'\t'+str(item.times)+'\n')

    def segAllSub(self):
        jieba.load_userdict('dict/userdict.txt')
        # jieba.enable_parallel(4)
        text = ''
        for y in range(6, 10):
            for m in range(1, 13):
                year = str(y)
                mon = ''
                if(m < 10):
                    mon = '0'+str(m)
                else:
                    mon = str(m)
                filename = '201'+year+'-'+mon
                try:
                    with open('out/'+filename+'.txt', 'r', encoding='utf-8') as f:
                        text += f.read()
                        # segList = jieba.cut(text, cut_all=False)
                except IOError:
                    print('File Not Exists')
                    continue
        segList = psg.cut(text)
        wordCount = {}
        for segg in segList:
            seg = segg.word
            # 过滤字符，过滤连词、叹词、副词、方位词、数词、拟声词、介词、代词、助词、标点符号、语气词
            if re.match('^[0-9’!"#$%&\'()*+,-./:：（）;<=>?@，。?★、…【】《》～；？“”‘’！[\\]^_`{|}~\s]+$', seg) != None:
                continue
            if(re.match('^nr', segg.flag) != None):
                if seg not in wordCount:
                    wordCount[seg] = 1
                else:
                    wordCount[seg] += 1
        wordItemArray = []
        for key in wordCount:
            wordItemArray.append(wordItem(key, wordCount[key]))
            # 按词频由高到低倒序排列
            wordItemArray.sort(reverse=True)

        with open('out/stat/allCountPerson.csv', 'w', encoding='utf-8') as fs:
            fs.write('word\tcount\n')
            for item in wordItemArray:
                fs.write(item.label+'\t'+str(item.times)+'\n')

    def cloudByMon(self):
        back_color = imread('back.png')

        for y in range(6, 10):
            for m in range(1, 13):
                year = str(y)
                mon = ''
                if(m < 10):
                    mon = '0'+str(m)
                else:
                    mon = str(m)
                filename = '201'+year+'-'+mon
                frequencies = {}
                try:
                    with open('out/stat/'+filename+'.csv', 'r', encoding='utf-8') as cf:
                        cr = csv.reader(cf, delimiter='\t')
                        line = -1
                        for row in cr:
                            line += 1
                            if(line) == 0:
                                continue
                            frequencies[row[0]] = int(row[1])
                        max_words = line
                        if(max_words > 200):
                            max_words = round(max_words / 2)
                        wc = WordCloud(background_color='#2980B9',  # 背景颜色
                                       max_words=max_words,  # 最大词数
                                       mask=back_color,
                                       max_font_size=200,  # 显示字体的最大值
                                       stopwords=STOPWORDS.add('—'),
                                       font_path="font.ttf",
                                       random_state=42,  # 为每个词返回一个PIL颜色
                                       collocations=False
                                       )
                        wc.fit_words(frequencies)
                        # 基于彩色图像生成相应彩色
                        image_colors = ImageColorGenerator(back_color)
                        recolor = wc.recolor(color_func=image_colors)
                        # # 显示图片
                        # plt.imshow(wc)
                        # # 关闭坐标轴
                        # plt.axis('off')
                        # # 绘制词云
                        # plt.figure()
                        # plt.imshow(recolor, cmap=plt.cm.gray)
                        # plt.axis('off')
                        # plt.show()
                        # 保存图片
                        wc.to_file('out/stat/wordcloud/'+filename+'.png')
                except IOError:
                    print('File Not Exists')

    def bubbleByMon():
        for y in range(6, 7):
            for m in range(1, 2):
                year = str(y)
                mon = ''
                if(m < 10):
                    mon = '0'+str(m)
                else:
                    mon = str(m)
                filename = '201'+year+'-'+mon
                frequencies = {}
                try:
                    with open('out/stat/'+filename+'.csv', 'r', encoding='utf-8') as cf:
                        cr = csv.reader(cf, delimiter='\t')
                        line = -1
                        for row in cr:
                            line += 1
                            if(line) == 0:
                                continue
                except IOError:
                    print(filename+'.csv Not Exists')

    def columnByMon(self):
        mpl.rcParams['font.size'] = 10  # 坐标轴标签的字体大小
        mpl.rcParams['font.sans-serif'] = ['simHei']
        mpl.rcParams['figure.figsize'] = (19.2, 10.8)
        # mpl.rcParams['savefig.dpi'] = 500  # 图片像素
        # mpl.rcParams['figure.dpi'] = 300 #分辨率
        for y in range(9, 10):
            date = []
            xs = []
            ys = []
            fig = plt.figure(figsize=(19.2, 10.8))  # 设置显示图形的大小
            ax = fig.add_subplot(111, projection='3d')  # 绘制3d图
            for m in range(1, 13):
                year = str(y)
                mon = ''
                if(m < 10):
                    mon = '0'+str(m)
                else:
                    mon = str(m)
                filename = '201'+year+'-'+mon
                try:
                    with open('out/stat/'+filename+'.csv', 'r', encoding='utf-8') as cf:
                        date.append(filename)
                        cr = csv.reader(cf, delimiter='\t')
                        line = -1
                        for row in cr:
                            line += 1
                            if(line == 0):
                                continue
                            count = int(row[1])
                            if(count < 10):
                                continue
                            xs.append(row[0])
                            ys.append(count)
                        # random.choice()从里面随机选出一个值，这样每次画的图形颜色就不一样了。
                        color = plt.cm.Set2(random.choice(range(8)))
                        zs = filename.split('-')
                        zs = int(zs[0]+zs[1])
                        ax.bar(xs, ys, zs=zs, zdir='y',
                               color=color, alpha=0.8)
                except IOError:
                    print(filename+'.csv Not Exists')
                    continue
            # 设置间隔的数字的大小，在前面我们使用过，还有没有印象？
            ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(10))
            locator = mdates.HourLocator(interval=1)
            locator.MAXTICKS = 10000
            ax.xaxis.set_minor_locator(locator)

            for label in ax.get_xticklabels():
                label.set_rotation(30)
                label.set_horizontalalignment('right')

            ax.set_yticklabels(date)
            # ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(3))  # 设置的y坐标的间隔为3。
            # ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(5))
            # ax.yaxis.set_minor_locator(locator)
            # z轴
            # dateFormatter = DateFormatter('%Y-%m')
            # ax.zaxis.set_major_formatter(dateFormatter)
            # ax.set_xlabel('Word')
            # ax.set_xticklabels(range(0,100))
            ax.set_ylabel('  Date')
            ax.set_zlabel('Count')
            plt.savefig('out/stat/bar/201'+str(y) +
                        '.jpg', dpi=600, format='jpg', transparent=False)
            # plt.show()

    def surfByMon(self):
        for y in range(9, 10):
            date = []
            xs = []
            ys = []
            zs = []
            # fig = plt.figure(figsize=(19.2, 10.8))  # 设置显示图形的大小
            # ax = fig.add_subplot(111, projection='3d')  # 绘制3d图
            fig = plt.figure()
            ax = fig.gca(projection='3d')
            for m in range(1, 13):
                year = str(y)
                mon = ''
                if(m < 10):
                    mon = '0'+str(m)
                else:
                    mon = str(m)
                filename = '201'+year+'-'+mon
                try:
                    with open('out/stat/'+filename+'.csv', 'r', encoding='utf-8') as cf:
                        date.append(filename)
                        cr = csv.reader(cf, delimiter='\t')
                        line = -1
                        for row in cr:
                            line += 1
                            if(line == 0):
                                continue
                            count = int(row[1])
                            if(count < 10):
                                continue
                            xs.append(row[0])
                            ys.append(count)
                        # random.choice()从里面随机选出一个值，这样每次画的图形颜色就不一样了。
                        # color = plt.cm.Set2(random.choice(range(8)))
                        z = filename.split('-')
                        z = int(z[0]+z[1])
                        zs.append(z)
                        # ax.bar(xs, ys, zs=z, zdir='y',
                        #        color=color, alpha=0.8)
                except IOError:
                    print(filename+'.csv Not Exists')
                    continue
            # surf = ax.plot_surface(
            #     xs, zs, , cmap=cm.coolwarm, linewidth=0, antialiased=False)

            # ax.set_zlim(-1.01, 1.01)
            # ax.zaxis.set_major_locator(LinearLocator(10))
            # ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

            # Add a color bar which maps values to colors.
            fig.colorbar(surf, shrink=0.5, aspect=5)

            plt.show()

    def cloudAll(self, textpath='out/stat/allCount.csv', path='out/stat/wordcloud/allCount.png', imgpath='back.png'):
        mpl.rcParams['figure.figsize'] = (19.2, 10.8)
        # mpl.rcParams['savefig.dpi'] = 500  # 图片像素
        mpl.rcParams['figure.dpi'] = 600  # 分辨率
        frequencies = {}
        back_color = imread(imgpath)
        with open(textpath, 'r', encoding='utf-8') as cf:
            cr = csv.reader(cf, delimiter='\t')
            line = -1
            for row in cr:
                line += 1
                if(line) == 0:
                    continue
                frequencies[row[0]] = int(row[1])
            max_words = line
            stop_words = STOPWORDS.copy()
            stop_words.add('—')
            stop_words.add('·')
            stop_words.add('a')
            wc = WordCloud(background_color='#2980B9',  # 背景颜色
                           max_words=max_words,  # 最大词数
                           mask=back_color,
                           max_font_size=250,  # 显示字体的最大值
                           stopwords=stop_words,
                           font_path="font.ttf",
                           random_state=42,  # 为每个词返回一个PIL颜色
                           collocations=False,
                           width=1920,
                           height=1080
                           )
            wc.fit_words(frequencies)
            # 基于彩色图像生成相应彩色
            image_colors = ImageColorGenerator(back_color)
            recolor = wc.recolor(color_func=image_colors)
            # # 显示图片
            # plt.imshow(wc)
            # # 关闭坐标轴
            # plt.axis('off')
            # # 绘制词云
            # plt.figure()
            # plt.imshow(recolor)
            # plt.axis('off')
            # plt.figure()
            # plt.imshow(back_color, cmap=plt.cm.gray)
            # plt.axis("off")
            # plt.show()
            # # 保存图片
            wc.to_file(path)
            # plt.savefig('out/stat/wordcloud/allCount_f.png',
            #             dpi=600, format='png')
            # plt.imsave('out/stat/wordcloud/allCount_f.png',
            #            recolor, dpi=600, format='png')
            # plt.imsave('out/stat/wordcloud/allCount_fg.png',
            #            wc, dpi=600, format='png')

    def cloudList(self, textpath='out/cqu_info_list_hits.csv', path='out/stat/wordcloud/countList.png', imgpath='back.png'):
        mpl.rcParams['figure.figsize'] = (19.2, 10.8)
        # mpl.rcParams['savefig.dpi'] = 500  # 图片像素
        mpl.rcParams['figure.dpi'] = 600  # 分辨率
        frequencies = {}
        back_color = imread(imgpath)
        with open(textpath, 'r', encoding='utf-8') as cf:
            cr = csv.reader(cf, delimiter='\t')
            line = -1
            for row in cr:
                line += 1
                if(line == 0 or int(row[5]) < 0):
                    continue
                frequencies[row[0]] = int(row[5])
            max_words = line
            stop_words = STOPWORDS.copy()
            stop_words.add('—')
            stop_words.add('·')
            stop_words.add('a')
            wc = WordCloud(background_color='#2980B9',  # 背景颜色
                           max_words=max_words,  # 最大词数
                           mask=back_color,
                           max_font_size=250,  # 显示字体的最大值
                           stopwords=stop_words,
                           font_path="font.ttf",
                           random_state=42,  # 为每个词返回一个PIL颜色
                           collocations=False,
                           width=1920,
                           height=1080
                           )
            wc.fit_words(frequencies)
            # 基于彩色图像生成相应彩色
            image_colors = ImageColorGenerator(back_color)
            recolor = wc.recolor(color_func=image_colors)
            # # 显示图片
            # plt.imshow(wc)
            # # 关闭坐标轴
            # plt.axis('off')
            # # 绘制词云
            # plt.figure()
            # plt.imshow(recolor)
            # plt.axis('off')
            # plt.figure()
            # plt.imshow(back_color, cmap=plt.cm.gray)
            # plt.axis("off")
            # plt.show()
            # # 保存图片
            wc.to_file(path)
            # plt.savefig('out/stat/wordcloud/allCount_f.png',
            #             dpi=600, format='png')
            # plt.imsave('out/stat/wordcloud/allCount_f.png',
            #            recolor, dpi=600, format='png')
            # plt.imsave('out/stat/wordcloud/allCount_fg.png',
            #            wc, dpi=600, format='png')

    def hitsCpByDate(self, textpath='out/cqu_info_list_hits.csv'):
        mpl.rcParams['font.sans-serif'] = ['simHei']
        hitss = []
        dates = []
        with open(textpath, 'r', encoding='utf-8') as cf:
            cr = csv.reader(cf, delimiter='\t')
            line = -1
            for row in cr:
                line += 1
                if(line == 0 or int(row[5]) < 0):
                    continue
                hitss.append(int(row[5]))
                dates.append(row[3])
        # fig = plt.figure()
        fig, ax = plt.subplots(figsize=(19.2, 10.8))
        plt.plot(dates, hitss)
        plt.xticks(rotation=30)
        # ax.set_xticklabels([], rotation=45)
        x_major_locator = mpl.ticker.MultipleLocator(10)
        y_major_locator = mpl.ticker.MultipleLocator(50)
        # ax = plt.gca()
        ax.xaxis.set_major_locator(x_major_locator)
        # 把x轴的主刻度设置为1的倍数
        ax.yaxis.set_major_locator(y_major_locator)
        # for label in ax.get_yticklabels():
        #     label.set_visible(False)
        # for label in ax.get_yticklabels()[::20]:
        #     label.set_visible(True)
        plt.title('时间/阅读量 变化')
        plt.xlabel(' Date')
        plt.ylabel(' hits')
        plt.savefig('out/stat/hitsByDate.png', format='png', dpi=600)
        plt.show()


seg = Seg()
# seg.userDictAppend()
# seg.segByMon()
# seg.cloudByMon()
# seg.columnByMon()

# x = range(0,10)
# y = range(0,10)
# plt.plot(x,y)
# plt.savefig('t.png')
# seg.surfByMon()
# seg.segAll()
# seg.cloudAll()
# 提取人名
# seg.segAllSub()
# 人名词云
# seg.cloudAll('out/stat/allCountPerson.csv','out/stat/wordcloud/allCountPerson.png', 'back3.png')
# seg.cloudList(imgpath='back.png')
seg.hitsCpByDate()
