# -*- coding: cp936 -*-
import web
import csv
import sqlite3
from pyExcelerator import *
import random
import time

urls = (
    '/merge','merge'
)

app = web.application(urls , globals())

web.config.debug=False
class merge:
    def GET(self):
	return """
<html>
    <head>
	<title>csv合并处理</title>
	<meta http-equiv="Content-Type" content="text/html;charset=gbk"/>
    </head>
    <body>
	<h1>csv合并处理流程</h1>
	<form method="POST" enctype="multipart/form-data">
	    淘宝导出1: <input type="file" name="tbcsv1"/><br/>
	    淘宝导出2: <input type="file" name="tbcsv2"/><br/>
	    <input type="submit"/>
	</form>
    </body>
</html>
"""

    def POST(self):
	reqdata = web.input(tbcsv1={},tbcsv2={})
	if ('tbcsv1' not in reqdata.keys()) or ('tbcsv2' not in reqdata.keys()):
	    return reError("文件上传未成功，请仔细检查后再上传")

	#try:
	t1 = csv.reader(reqdata['tbcsv1'].file)
	##return len(t1.next())
	
	#except:
	t2 = csv.reader(reqdata['tbcsv2'].file)
	

	conn = sqlite3.connect(":memory:")
	conn.text_factory = str
	cur = conn.cursor()
	
	############# create and init t1 ##################
	cur.execute("""create table csv1 (
		id integer primary key,
		order_id integer,
		custom_name varchar(255),
		alipay_id varchar(255),
		custom_pay decimal(12,2),
		remarks varchar(255),
		consignee varcahr(32),
		shipping_address varchar(255),
		phone varchar(16),
		mobile varchar(16),
		pay_time varchar(32),
		order_remarks varchar(255)
		)""")
	
	t1.next()
	for line in t1:
	    sql = """insert into csv1 (order_id,custom_name,alipay_id,custom_pay,remarks,consignee,shipping_address,phone,mobile,pay_time,order_remarks) values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")""" % (line[0],line[1],line[2],line[8],line[11],line[12],line[13],line[15],line[16],line[18],line[23])
	    try:
		cur.execute(sql)
	    except:
		return reError("""%s<br/>%s""" % (sql , repr(line)))

	conn.commit()

	############# create and init t2 ##################
	cur.execute("""create table csv2 (
		id integer primary key,
		order_id integer,
		title varchar(255),
		price decimal(12,2),
		order_count integer,
		out_sn varchar(32),
		property varcahr(255)
		)""")

	t2.next()
	for line in t2:
	    sql = """insert into csv2 (order_id,title,price,order_count,out_sn,property) values ("%s","%s","%s","%s","%s","%s")""" % (line[0],line[1],line[2],line[3],line[4],line[5])
	    cur.execute(sql)
	
	conn.commit()

	############# now merge and output ################
	f_sql = """select c1.order_id,c1.custom_name,c2.title,c1.alipay_id,c1.custom_pay,c1.consignee,c1.shipping_address,c1.phone,c1.mobile,c1.pay_time,c1.order_remarks, c2.price,c2.order_count,c2.out_sn,c2.property,c1.remarks from csv1 as c1 left join csv2 as c2 on c2.order_id=c1.order_id order by c1.order_id"""
	cur.execute(f_sql)
	
	w = Workbook()
	ws = w.add_sheet(u'订单合并')
	
	ws.write(0,0,u'订单编号')
	ws.write(0,1,u'买家会员名')
	ws.write(0,2,u'标题')
	ws.write(0,3,u'买家支付宝账户')
	ws.write(0,4,u'买家实际支付金额')
	ws.write(0,5,u'收货人姓名')
	ws.write(0,6,u'收货地址')
	ws.write(0,7,u'联系电话')
	ws.write(0,8,u'联系手机')
	ws.write(0,9,u'订单付款时间')
	ws.write(0,10,u'订单备注')
	ws.write(0,11,u'价格')
	ws.write(0,12,u'购买数量')
	ws.write(0,13,u'外部系统编号')
	ws.write(0,14,u'商品属性')
	ws.write(0,15,u'买家留言')
	
	idx = 0
	for line in cur:
	    idx = idx + 1
	    for i in range(16):
			try:
				ws.write(idx , i , unicode(line[i],"gbk"))
			except:
				ws.write(idx , i , line[i])
	    ##print line[15]			
	fn = gen_fileid()
	w.save(fn)
	return reSucc("""操作已成功，合并后文件为 %s""" % fn)
#################################################################

def reError(reason="未知错误"):
    return """<html>
    <head>
	<title>出错啦</title>
	<meta http-equiv="Content-Type" content="text/html;charset=gbk"/>
	<style>
	    
	</style>
    </head>
    <body>
	<h2>%s</h2>
    </body>
</html>
""" % reason

def reSucc(tips="操作已成功完成"):
    return """<html>
    <head>
	<title>操作成功</title>
	<meta http-equiv="Content-Type" content="text/html;charset=gbk"/>
	<style>
	    
	</style>
    </head>
    <body>
	<h2>%s</h2>
    </body>
</html>
""" % tips



def gen_fileid():
    return """%s_%d.xls""" % (time.strftime("%Y%m%d%H%M%S"),random.randint(1,65536))


if "__main__" == __name__:
    app.run()


