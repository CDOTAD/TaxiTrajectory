# TaxiTrajectory

<li>PostgreSQL 9.6</li>
<li>PostGIS 2.4</li>
<li>osmosis</li>
<li>OpenStreetMap</li>

## PostGIS

<li>坐标转换</li>

竟然有内置的坐标系统转换函数，是我太菜还寻找SRID 4326转换SRID 900913的Python脚本，原来ST_transform 想转什么就转什么。

	ST_transform(zjuntaxitra.trajectory,900913)

<li>二进制，TXT WKT转换</li>

看不懂的二进制WKT，令人头大

![](https://i.imgur.com/Qh4gBCw.png)

	ST_AsEWKT(ST_transform(zjuntaxitra.trajectory,900913))

ST_AsEWKT 后

![](https://i.imgur.com/jYGSwpp.png)

<li> EWKT </li>

<strong>*The Well-Know Text*</strong> that i do not know.

PostGIS中的点，线，面的表达都要用这个EWKT，其中：

- 点长这个样子

		ST_GeomFromEWKT('SRID=4326;Point(121.58018 31.213618)')

- 线长这个样子

		ST_GeomFromEWKT('SRID=4326;LINESTRING(121.574432 31.195258,121.575758 31.195765)')

- 面长这个样子

		ST_GeomFromEWKT('SRID=900913;POLYGON((13466465.1 3592039.72,13466478.36 3592050.8,13466513.09 3592009.21,13466499.83 3591998.13,13466465.1 3592039.72))')

还可以通过ST_GeometryFromText,当然如果你想写 ST_GeomFromEWKB 那我也不拦着你。另外，这个SRID=4236一定要连在一起，**不能有空格**，否则报错！

<li>空间图形做交集</li>

PostGIS功能还是挺强大的，内置各种函数对空间数据进行操作。

[PostGIS常用函数简介](https://blog.csdn.net/xlxxcc/article/details/65629541 "PostGIS常用函数简介")

讲轨迹按照行政区域，栅格区域进行切割

	ST_Intersection(tra.trajectory, polygon.the_geom)

这个取交集好像对点的数量有一定限制，如果点太多，就会没有返回结果。
具体参见官方文档[ST_Intersection](http://postgis.net/docs/manual-2.4/ST_Intersection.html "ST_Intersection")

栅格切割后的非直线系数

![nonlinearcoe_raster](https://i.imgur.com/KB1uYht.png)

## PGRouting

作为路网分析的工具包，我认为它不太好用，反正我是没查询出来结果sad！[Pgrouting 官网](http://pgrouting.org/ "pgrouting")

主要运用Dijkstra算法计算路网中两点间的最短路径。

[Dijkstra算法家族](http://docs.pgrouting.org/2.5/en/pgr_dijkstra.html#pgr-dijkstra "Dijkstra")

	SELECT * FROM pgr_Dijkstra('
		SELECT id, source, target, cost, reverse_cost FROM edge_table',
		2,3
	);

[简单实例的简单数据集](http://docs.pgrouting.org/2.5/en/sampledata.html "sampledata")

数据很简单，算法在实例数据集上运行结果正确，然而应用到我从openstreetmap上下载下来的数据集后就没有结果。

## Kalman Filtering

- [filterpy 1.2.3](https://github.com/rlabbe/filterpy "filterpy")

滤波前的轨迹，存在漂移记录点

![drifting_tra](https://i.imgur.com/oCcrmsN.png)

简单过滤，随意修正（其实就是filterpy的文档还没看完，没用filterpy做滤波）后的效果，感觉还行

![filterpy](https://i.imgur.com/9gJfW9J.png)


