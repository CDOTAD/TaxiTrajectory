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

这是一个VSCODE更新实验



