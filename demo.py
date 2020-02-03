import os
import json
import time
import requests
from flask import Flask
from jinja2 import Markup, Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig
from pyecharts.globals import ThemeType

from googletrans import Translator

# 关于 CurrentConfig，可参考 [基本使用-全局变量]
CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./templates"))

from pyecharts import options as opts
from pyecharts.charts import Bar,Line,Kline,Map,ThemeRiver
from pyecharts.commons.utils import JsCode  #高级绘图需要，默认不需要

app = Flask(__name__, static_folder="templates")


def get_chinaDayList():
    with open(os.path.join('data','data.json'),'r',encoding='utf-8') as f:
        data = json.load(f)
        chinaDayList = data['chinaDayList']     #结果为list,{'date': '01.13', 'confirm': '41', 'suspect': '0', 'dead': '1', 'heal': '0'}
        # date = [x['date'] for x in chinaDayList]
        # confirm = [x['confirm'] for x in chinaDayList]
        # suspect = [x['suspect'] for x in chinaDayList]
        # dead = [x['dead'] for x in chinaDayList]
        # heal = [x['heal'] for x in chinaDayList]
        #chinadata = data['areaTree'][0]['children']     #全国数据，结果为列表
        worlddata = data['areaTree']
    return chinaDayList,worlddata

def bar_base() -> Bar:
    chinaDayList = get_chinaDayList()   
    #计算趋势
    Dailyincrease = []
    a = [x['confirm'] for x in chinaDayList]
    for i in range(len(a)):
        if i == 0:
            Dailyincrease.append(0)
        else:
            Dailyincrease.append(int(a[i]) - int(a[i-1]))  
    #每日疑似
    Dailysuspect = []
    a = [x['suspect'] for x in chinaDayList]
    for i in range(len(a)):
        if i == 0:
            Dailysuspect.append(0)
        else:
            Dailysuspect.append(int(a[i]) - int(a[i-1]))        
    c = (
        Bar()
        .add_xaxis([x['date'] for x in chinaDayList])   #直接列表
        .add_yaxis('确诊',[x['confirm'] for x in chinaDayList])    #‘列表名，[]’
        .add_yaxis('疑似',[x['suspect'] for x in chinaDayList])
        .add_yaxis('治愈',[x['heal'] for x in chinaDayList])
        .add_yaxis('死亡',[x['dead'] for x in chinaDayList])
        .add_yaxis('每日确诊增加数',Dailyincrease)
        .add_yaxis('每日疑似增加数',Dailysuspect)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="2019-nCov疫情分析", subtitle=""),
            datazoom_opts=opts.DataZoomOpts(),
            # graphic_opts=[
            #     opts.GraphicImage(
            #         graphic_item=opts.GraphicItem(
            #             id_="logo",
            #             right=20,
            #             top=20,
            #             z=-10,
            #             bounding="raw",
            #             origin=[75, 75],
            #         ),
            #         graphic_imagestyle_opts=opts.GraphicImageStyleOpts(
            #             image="https://img.baiyue.one/upload/2019/07/5d1a0e774d812.png",
            #             width=395,
            #             height=179,
            #             opacity=0.4,
            #         ),
            #     )
            # ],
            )

    )
    return c

def line_connect_null() -> Line:
    chinaDayList,worlddata = get_chinaDayList()
    #每日确诊增加数
    Dailyincrease = []
    a = [x['confirm'] for x in chinaDayList]
    for i in range(len(a)):
        if i == 0:
            Dailyincrease.append(0)
        else:
            Dailyincrease.append(int(a[i]) - int(a[i-1]))  
    #每日疑似增加数
    Dailysuspect = []
    a = [x['suspect'] for x in chinaDayList]
    for i in range(len(a)):
        if i == 0:
            Dailysuspect.append(0)
        else:
            Dailysuspect.append(int(a[i]) - int(a[i-1]))        
    c = (
        Line()
        .add_xaxis([x['date'] for x in chinaDayList])   #直接列表
        .add_yaxis('确诊',[x['confirm'] for x in chinaDayList])    #‘列表名，[]’
        .add_yaxis('疑似',[x['suspect'] for x in chinaDayList])
        .add_yaxis('治愈',[x['heal'] for x in chinaDayList])
        .add_yaxis('死亡',[x['dead'] for x in chinaDayList])
        .add_yaxis('每日确诊增加数',Dailyincrease,areastyle_opts=opts.AreaStyleOpts(opacity=0.5))   #areastyle_opts=opts.AreaStyleOpts(opacity=0.5) 投射面积
        .add_yaxis('每日疑似增加数',Dailysuspect,is_smooth=True)    #is_smooth=True 代表平滑曲线
        .set_global_opts(
            title_opts=opts.TitleOpts(title="2019-nCov"),
            datazoom_opts=opts.DataZoomOpts(),
        )
    )
    return c

def world_bar() -> Bar:
    with open(os.path.join('data','data.json'),'r',encoding='utf-8') as f:
        data = json.load(f)
    country = []
    numbers = []
    for i in data['areaTree']:
        country.append(i['name'])
        numbers.append(i['total']['confirm'])
    country.reverse()
    numbers.reverse()
    c = (
        Bar()
        .add_xaxis(country[:-1])
        .add_yaxis("确诊人数", numbers[:-1])
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position="right",color="black"))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="海外国家统计数据"),
            yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45,font_size=11)),
            )
    
    )
    return c        


def other_line() -> Line:
    url = 'https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/cases_time/FeatureServer/0/query?f=json&where=Report_Date%3C%3D%272020-02-01%2015%3A59%3A59%27&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Report_Date%20asc&resultOffset=0&resultRecordCount=2000&cacheHint=true'
    r_data = json.loads(requests.get(url).text)
    data = r_data['features']    #初始化json数据，为dict ['chinaTotal']   

    dates = []
    numbers = []
    for i in data:
        date = time.strftime("%m.%d", time.localtime(i['attributes']['Report_Date'] / 1000))
        dates.append(date)
        numbers.append(i['attributes']['Other_Locations'])
  
    c = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.VINTAGE))    #设置主题
        
        .add_xaxis(dates)   #直接列表
        .add_yaxis('确诊',numbers)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="2019-nCov 海外国家疫情分析", subtitle=""),
            toolbox_opts = opts.ToolboxOpts(is_show = True),  # 
            
            )
        .set_series_opts(
                # 设置系列配置
                markpoint_opts=opts.MarkPointOpts(
                    data=[
                        opts.MarkPointItem(type_="max", name="最大值"),
                        opts.MarkPointItem(type_="min", name="最小值"),
                    ]
                ),
                areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
                label_opts=opts.LabelOpts(is_show=False),

            )            

    )
    return c


def world_line() -> Bar:
    with open(os.path.join('data','data.json'),'r',encoding='utf-8') as f:
        data = json.load(f)
    country = []
    numbers = []
    for i in data['areaTree']:
        country.append(i['name'])
        numbers.append(i['total']['confirm'])
    country.reverse()
    numbers.reverse()
    c = (
        Bar()
        .add_xaxis(country[:-1])
        .add_yaxis("确诊人数", numbers[:-1])
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position="right",color="black"))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="海外国家统计数据"),
            yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45,font_size=11)),
            )
    
    )
    return c        

def kline_base() -> Kline:
    chinaDayList,worlddata = get_chinaDayList()
    #每日确诊增加数
    a = []
    c = [x['confirm'] for x in chinaDayList]
    for i in range(len(c)):
        if i == 0:
            a.append(0)
        else:
            a.append(int(c[i]) - int(c[i-1]))      
    b = []
    for i in range(len(a)):
        if i == 0:
            b.append([0,0,0,a[i]])
        elif i == 1:
            b.append([0,0,a[i-1],a[i]])
        elif i == 2:
            b.append([0,a[i-2],a[i-1],a[i]])        
        else:
            b.append([a[i-3],a[i-2],a[i-1],a[i]])
    c = (
        Kline()
        .add_xaxis([x['date'] for x in chinaDayList])
        .add_yaxis("kline", b)
        .set_global_opts(
            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                splitarea_opts=opts.SplitAreaOpts(
                    is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                ),
            ),
            xaxis_opts=opts.AxisOpts(is_scale=True),
            title_opts=opts.TitleOpts(title="2019-nCov K线图"),
            datazoom_opts=[opts.DataZoomOpts(pos_bottom="-2%")],
        )
    )
    return c
def map_china() -> Map:
    chinaDayList,worlddata = get_chinaDayList()
    chinadata = worlddata[0]['children']
    provinces = []
    for i in chinadata:
        provinces.append(i['name'])
    #今日数据
    today_confirm = []
    for i in chinadata:
        today_confirm.append(i['today']['confirm'])    
    c = (
        Map()
        .add("商家A", [list(z) for z in zip(provinces, today_confirm)], "china")
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Map-世界地图"),
            visualmap_opts=opts.VisualMapOpts(min_=1,max_=200),
        )
    )
    return c

def map_world() -> Map:
    chinaDayList,worlddata = get_chinaDayList()
    country = []    #中文国家提取
    for i in worlddata:
        country.append(i['name'])
    translate = Translator()
    countryEN = []  #翻译
    for i in country:
        countryEN.append(translate.translate(i).text)
    #今日数据
    total_confirm = []
    for i in worlddata:
        total_confirm.append(i['total']['confirm'])    
    c = (
        Map()
        .add("商家A", [list(z) for z in zip(countryEN, total_confirm)], "world")
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Map-世界地图"),
            visualmap_opts=opts.VisualMapOpts(min_=1,max_=200),
        )
    )
    return c

def themeriver() -> ThemeRiver:
    a = [1,10,100,110,130,130]  #模拟确诊
    b = [0,2,20,50,100,102]     #模拟治愈
    c = [0,1,10,15,18,18]   #模拟死亡
    x = [1,2,3,4,5,6]   #模拟日期
    confirm = [list(z) for z in zip(x,a)]
    for i in confirm:
        i.append('确诊')
    heal = [list(z) for z in zip(x,b)]
    for i in heal:
        i.append('治愈')
    dead = [list(z) for z in zip(x,c)]
    for i in dead:
        i.append('死亡')    

    data = confirm + heal + dead
    #print(data)
    c = (
        ThemeRiver()
        .add(
            ["DQ", "TY", "SS"],
            data,
            singleaxis_opts=opts.SingleAxisOpts(type_="time", pos_bottom="10%"),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="ThemeRiver-基本示例"))
    )
    return c    


def heliu() -> Bar:

    a = [1,10,100,150,180,200]  #模拟确诊
    b = [0,2,20,50,100,102]     #模拟治愈
    c = [0,1,10,15,18,18]   #模拟死亡
    v = list(map(lambda x: x[0]-x[1]-x[2], zip(a, b, c)))   #等待治愈
    x = [0,1,2,3,4,5]   #模拟日  
    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.VINTAGE))    #设置主题
        
        .add_xaxis(x)   #直接列表
        #.add_yaxis('确诊',v,stack="stack1")
        .add_yaxis('死亡',c,stack="stack3")
        .add_yaxis('治愈',b,stack="stack3")
        .add_yaxis('确诊',v,stack="stack3")
        .set_global_opts(
            title_opts=opts.TitleOpts(title="2019-nCov 海外国家疫情分析", subtitle=""),
            toolbox_opts = opts.ToolboxOpts(is_show = True),  # 
            datazoom_opts=opts.DataZoomOpts(),
            
            )
        .set_series_opts(
                # 设置系列配置
                areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
                label_opts=opts.LabelOpts(is_show=False),
                singleaxis_opts=opts.SingleAxisOpts(max_=80)
            )            

    )
    return c    
@app.route("/")
def index():
    #c = bar_base()
    #c = line_connect_null()
    #c = kline_base()
    #c = map_china()
    #c = map_world()
    #c = world_bar()
    #c = other_line()
    #c = themeriver()
    c = heliu()
    return Markup(c.render_embed())


if __name__ == "__main__":
    app.run(debug=True)

# 确诊、治愈、死亡为一组；line
# 确诊新增、疑似新增为一组；bar
# 治愈新增、死亡新增为一组；bar
# 确证、死亡、治愈

#含有国内外，最近几日的数据变化
# https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/cases_time/FeatureServer/0/query?f=json&where=Report_Date%3C%3D%272020-01-31%2015%3A59%3A59%27&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Report_Date%20asc&resultOffset=0&resultRecordCount=2000&cacheHint=true

