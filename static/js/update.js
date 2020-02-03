var chinamap = echarts.init(document.getElementById('ncov-map'), 'white', {renderer: 'canvas'});
var worldmap = echarts.init(document.getElementById('ncov-maps'), 'white', {renderer: 'canvas'});
var nkline = echarts.init(document.getElementById('ncov-kline'), 'white', {renderer: 'canvas'});
var nline = echarts.init(document.getElementById('ncov-line'), 'white', {renderer: 'canvas'});
var worldbar = echarts.init(document.getElementById('ncov-worldbar'), 'white', {renderer: 'canvas'});
var worldline = echarts.init(document.getElementById('ncov-worldline'), 'white', {renderer: 'canvas'});
var heal = echarts.init(document.getElementById('ncov-heal'), 'white', {renderer: 'canvas'});

$(
    function () {
        //updateOverall();
        updateNews();
        updateOnline(); //实时统计数据
        updateHotNews();    //热点更新
        fetchData(chinamap);
        fetchData2(worldmap);
        kline(nkline);
        line(nline);
        getworldbar(worldbar);
        getworldline(worldline);
        getheal(heal);
        setInterval(updateNews, 30 * 60 * 1000);    //半小时获取一次
        //setInterval(updateOverall, 60 * 1000);
        setInterval(fetchData, 30 * 60 * 1000);
        setInterval(fetchData2, 30 * 60 * 1000);
        setInterval(updateHotNews, 10 * 60 * 1000);
    }
);

function getHost() {
    return document.location.protocol + "//" +window.location.host;
}


function updateOnline(){
    $.ajax({
        type: "GET",
        url: getHost() + "/online",
        dataType: 'json',
        success: function (result) {
            online_html = '<li class="text-muted"><i class="fa fa-smile-o pr-2"></i>  更新时间：' + result['lastUpdateTime'] +'</li><li class="badge badge-primary"><i class="fa fa-bug pr-2"></i>全国确诊：' + result['chinaTotal']['confirm'] + '</li><br><li class="badge badge-success"><i class="fa fa-heartbeat pr-2"></i>治愈：' + result['chinaTotal']['heal'] + '</li><br><li class="badge badge-secondary"><i class="fa fa-hospital-o pr-2"></i>死亡：' + result['chinaTotal']['dead'] + '</li>'
            $('#online').html(online_html)
        }
    });
}

function updateHotNews(){
    $.ajax({
        type: "GET",
        url: getHost() + "/hotnews",
        dataType: 'json',
        success: function (result) {
            hotnews_html = ""
            for(var i = 0, len = result.length; i < len; i++){
                hotnews_html += "<li><div class='base-timeline-info'>" + result[i] + "</div></li>"
            }
            $('#hotnews').html(hotnews_html)
        }
    });
}

function updateNews(){
    $.ajax({
        type: "GET",
        url: getHost() + "/news",
        dataType: 'json',
        success: function (result) {
            news_html = ""
            for(var i = 0, len = result.length; i < len; i++){
                news_html += "<li><div class='base-timeline-info'><a href=" + result[i]['sourceUrl'] + ">" + result[i]['title'] + "</a></div><small class='text-muted'>" + result[i]['infoSource'] + '</small></li>'
            }
            $('#newslist').html(news_html)
        }
    });
}


//中国地图
function fetchData(chinamap) {
    $.ajax({
        type: "GET",
        url: getHost() + "/map",
        dataType: 'json',
        success: function (result) {
            chinamap.setOption(result);
        }
    });
}
//世界地图
function fetchData2(worldmap) {
    $.ajax({
        type: "GET",
        url: getHost() + "/maps",
        dataType: 'json',
        success: function (result) {
            worldmap.setOption(result);
        }
    });
}

//kline
function kline(data) {
    $.ajax({
        type: "GET",
        url: getHost() + "/kline",
        dataType: 'json',
        success: function (result) {
            data.setOption(result);
        }
    });
}
//line
function line(data) {
    $.ajax({
        type: "GET",
        url: getHost() + "/line",
        dataType: 'json',
        success: function (result) {
            data.setOption(result);
        }
    });
}

function getworldbar(data) {
    $.ajax({
        type: "GET",
        url: getHost() + "/worldbar",
        dataType: 'json',
        success: function (result) {
            data.setOption(result);
        }
    });
}

function getworldline(data) {
    $.ajax({
        type: "GET",
        url: getHost() + "/worldline",
        dataType: 'json',
        success: function (result) {
            data.setOption(result);
        }
    });
}

function getheal(data) {
    $.ajax({
        type: "GET",
        url: getHost() + "/heal",
        dataType: 'json',
        success: function (result) {
            data.setOption(result);
        }
    });
}

function getworldcloud(data) {
    $.ajax({
        type: "GET",
        url: getHost() + "/wordcloud",
        dataType: 'json',
        success: function (result) {
            data.setOption(result);
        }
    });
}