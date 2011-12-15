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
	<title>csv�ϲ�����</title>
	<meta http-equiv="Content-Type" content="text/html;charset=gbk"/>
    </head>
    <body>
	<h1>csv�ϲ���������</h1>
	<form method="POST" enctype="multipart/form-data">
	    �Ա�����1: <input type="file" name="tbcsv1"/><br/>
	    �Ա�����2: <input type="file" name="tbcsv2"/><br/>
	    <input type="submit"/>
	</form>
    </body>
</html>
"""

    def POST(self):
	reqdata = web.input(tbcsv1={},tbcsv2={})
	if ('tbcsv1' not in reqdata.keys()) or ('tbcsv2' not in reqdata.keys()):
	    return reError("�ļ��ϴ�δ�ɹ�������ϸ�������ϴ�")

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
	ws = w.add_sheet(u'�����ϲ�')
	
	ws.write(0,0,u'�������')
	ws.write(0,1,u'��һ�Ա��')
	ws.write(0,2,u'����')
	ws.write(0,3,u'���֧�����˻�')
	ws.write(0,4,u'���ʵ��֧�����')
	ws.write(0,5,u'�ջ�������')
	ws.write(0,6,u'�ջ���ַ')
	ws.write(0,7,u'��ϵ�绰')
	ws.write(0,8,u'��ϵ�ֻ�')
	ws.write(0,9,u'��������ʱ��')
	ws.write(0,10,u'������ע')
	ws.write(0,11,u'�۸�')
	ws.write(0,12,u'��������')
	ws.write(0,13,u'�ⲿϵͳ���')
	ws.write(0,14,u'��Ʒ����')
	ws.write(0,15,u'�������')
	
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
	return reSucc("""�����ѳɹ����ϲ����ļ�Ϊ %s""" % fn)
#################################################################

def reError(reason="δ֪����"):
    return """<html>
    <head>
	<title>������</title>
	<meta http-equiv="Content-Type" content="text/html;charset=gbk"/>
	<style>
	    
	</style>
    </head>
    <body>
	<h2>%s</h2>
    </body>
</html>
""" % reason

def reSucc(tips="�����ѳɹ����"):
    return """<html>
    <head>
	<title>�����ɹ�</title>
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


