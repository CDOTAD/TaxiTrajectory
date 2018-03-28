# -*-coding: utf-8 -*-

html = open('visualTraceWGS2BD.html','w')

htmlStr = """
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html"; charset=utf-8"/>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
    <style  type="text/css">
        body,html,#allmap{
            width: 100%;
            height: 100%;
            overflow: hidden;
            margin: 0;
            font-family:"微软雅黑";
        }
    </style>
    <script type="text/javascript" src="http://api.map.baidu.com/api?v=2.0&ak=Lcm5jrXRtoBmVZ8bB24G2j4v9pC6LQYQ"></script>
    <title>出租车数据投影</title>
</head>
<body>
    <div id="allmap"></div>
</body>
</html>
<script type="text/javascript">
    
    var map = new BMap.Map("allmap");
    map.centerAndZoom("上海",15);
    setTimeout(function(){
        map.setZoom(14);
    },2000);
    map.enableScrollWheelZoom(true);
    
    if(document.createElement('canvas').getContext){
    
        var options = {
        
            size: BMAP_POINT_SIZE_NORMAL,
            shape: BMAP_POINT_SHAPE_CIRCLE,
            color: 'blue'       
        }
    
        var points=[]
    
"""

pointsStr=""

with open('taxiTrajectoryWGS2BD_14948.txt','r') as openFile:

    i = 1

    for line in openFile :

        line=line.split(',')

        longitude = float(line[4])

        latitude = float(line[5])

        pointsStr += "      points.push(new BMap.Point("+line[4]+','+line[5]+"));\n"


        i += 1

pointsStr += "      var pointCollection = new BMap.PointCollection(points, options);\n"

pointsStr += "      map.addOverlay(pointCollection);\n"

pointsStr += "   }\n";

htmlStr += pointsStr

htmlStr += "</script>"

html.write(htmlStr)

html.close()

