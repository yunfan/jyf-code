<?php
	require("lib/cls_sqlite_a.php");
	require("lib/cls_timer.php");
	
	$t = new timer('开始');
	
	/**/
	$db1 = new db(array('db' => 'db/user_group.db.php' , 'mode' => 0777));
	
	$t->click('创建user_group');
	
	$db1->exec("create table '<?php' (a)") or die ("Error at create table '<?php' <br/>" . $db1->error);
	
	$t->click('创建user_base表');
	
	$db1->exec("create table pin_user_base(
		id integer primary key,
		name varchar(32) not null,
		password char(32) not null,
		group_id integer not null,
		add_time integer not null,
		update_time integer not null)") or die('Error at create table pin_user_base<br/>' . $db1->error);
	
	$t->click('创建user_extra表');
	
	$db1->exec("create table pin_user_extra(
		id integer primary key,
		user_id integer not null,
		val_key varchar(32) not null, 
		val_value varchar(128) not null,
		add_time integer not null,
		update_time integer default 0 not null)") or die('Error at create table pin_user_extra' . $db1->error);
	
	$t->click('创建group_base表');
	
	$db1->exec("create table pin_group_base(
		id integer primary key,
		group_name varchar(32) not null
	)") or die ("Error at create table 'pin_group_base' <br/>" . $db1->error);
	
	$t->click('创建group_extra表');
	
	$db1->exec("create table pin_group_extra(
		id integer primary key,
		group_id integer not null,
		val_key varchar(32) not null, 
		val_value varchar(128) not null,
		add_time integer not null,
		update_time integer default 0 not null
	)") or die ("Error at create table 'pin_group_extra' <br/>" . $db1->error);
	
	$t->click('创建结束');
	
	$db1->close();
	
	$t->click('关闭');
	
	$db2 = new db(array('db' => 'db/forum.db.php' , 'mode' => 0777));
	
	$t->click('创建forum');
	
	$db2->exec("create table '<?php' (a)") or die ("Error at create table '<?php' <br/>" . $db2->error);
	
	$t->click('创建forum_base表');
	
	$db2->exec("create table pin_forum_base(
		id integer primary key,
		forum_name varchar(32) not null,
		forum_desc varchar(255) not null,
		topic_num integer not null,
		post_num integer not null,
		last_post_name varchar(32) not null,
		last_post_title varchar(255) not null,
		last_post_id integer not null,
		last_post_time integer not null,
		parent_id integer default 0 not null
	)") or die ("Error at create table 'pin_forum_base' <br/>" . $db2->error);
	
	$t->click('创建forum_extra表');
	
	$db2->exec("create table pin_forum_extra(
		id integer primary key,
		forum_id integer not null,
		val_key varchar(32) not null, 
		val_value varchar(128) not null,
		add_time integer not null,
		update_time integer default 0 not null
	)") or die ("Error at create table 'pin_forum_extra' <br/>" . $db2->error);
	
	$t->click('创建结束');
	
	$db2->close();
	
	$t->click('创建topic');
	
	$db3 = new db(array('db' => 'db/topic.db.php' , 'mode' => 0777));
	
	$t->click('创建开始');
	
	$db3->exec("create table '<?php' (a)") or die ("Error at create table '<?php' <br/>" . $db3->error);
	
	$t->click('创建topic_base表');
	
	$db3->exec("create table pin_topic_base(
		id integer primary key,
		subject varchar(255) not null,
		reply_num integer default 0 not null,
		view_num integer default 0 not null,
		add_user_id integer default 0 not null,
		add_user_name varchar(32) not null,
		add_time integer not null,
		last_user_id integer default 0 not null,
		last_user_name varchar(32),
		last_time integer not null,
		forum_id integer not null
	)") or die ("Error at create table 'pin_topic_base' <br/>" . $db3->error);
	
	$t->click('创建topic_extra表');
	
	$db3->exec("create table pin_topic_extra(
		id integer primary key,
		topic_id integer not null,
		val_key varchar(32) not null, 
		val_value varchar(128) not null,
		add_time integer not null,
		update_time integer default 0 not null
	)") or die ("Error at create table 'pin_topic_extra' <br/>" . $db3->error);
	
	$t->click('创建结束');
	
	$db3->close();
	
	$t->click('创建post');
	
	$db4 = new db(array('db' => 'db/post.db.php' , 'mode' => 0777));
	
	$t->click('创建开始');
	
	$db4->exec("create table '<?php' (a)") or die ("Error at create table '<?php' <br/>" . $db4->error);
	
	$t->click('创建post_base表');
	
	$db4->exec("create table pin_post_base(
		id integer primary key,
		topic_id integer not null,
		subject varchar(255) not null,
		content text not null,
		add_time integer not null,
		user_id integer default 0 not null,
		user_ip varchar(15) not null,
		forum_id integer not null,
		edit_name varchar(32),
		edit_time integer default 0 not null
	)") or die ("Error at create table 'pin_post_base' <br/>" . $db4->error);
	
	$t->click('创建post_extra表');
	
	$db4->exec("create table pin_post_extra(
		id integer primary key,
		post_id integer not null,
		val_key varchar(32) not null, 
		val_value varchar(128) not null,
		add_time integer not null,
		update_time integer default 0 not null
	)") or die ("Error at create table 'pin_post_extra' <br/>" . $db4->error);
	
	$t->click('创建结束');
	
	$db4->close();
	/**/
	
	$t->click('开始打开user_group插入');
	
	$db1 = new db(array('db' => 'db/user_group.db.php' , 'mode' => 0777));
	
	$t->click('插入用户组');
	
	$db1->exec("insert into pin_group_base(id , group_name) values ( 0 , '游客') ;insert into pin_group_base(id , group_name) values (1 , '普通用户') ;insert into pin_group_base(id , group_name) values ( 2, '管理员')") or die('插入组失败');
	
	$t->click('插入用户');
	
	$now = time();
	
	$db1->exec("insert into pin_user_base (name,password,group_id,add_time,update_time) values('root' , '".md5('90IO()')."' , 2 , ".$now." , 0 )") or die('插入用户失败');
	
	$t->click('关闭user_group');
	
	$db1->close();
	
	$t->click("开始打开forum");
	
	$db2 = new db(array('db' => 'db/forum.db.php' , 'mode' => 0777));
	
	$t->click("开始插入论坛");
	
	$db2->exec("insert into pin_forum_base (id , forum_name,forum_desc,topic_num,post_num,last_post_name,last_post_title,last_post_id,last_post_time,parent_id) values(1 , '测试分区一' , '' , 0 , 0 , '' , '' , 0 , 0 , 0)") or die('插入论坛失败');
	
	$db2->exec("insert into pin_forum_base (id , forum_name,forum_desc,topic_num,post_num,last_post_name,last_post_title,last_post_id,last_post_time,parent_id) values(2 , '测试版块' , '测试用的版块' , 1 , 2 , 'root' , 'RE:欢迎使用Pinbb论坛系统' , 2 , ".$now." , 1)") or die('插入论坛失败');

	$t->click("关闭forum");
	
	$db2->close();
	
	$t->click("开始打开topic");
	
	$db3 = new db(array('db' => 'db/topic.db.php' , 'mode' => 0777));
	
	$t->click("开始插入主题");
	
	$db3->exec("insert into pin_topic_base (id,subject,reply_num,view_num,add_user_id,add_user_name,add_time,last_user_id,last_user_name,last_time,forum_id) values(1,'欢迎使用Pinbb论坛系统',1,2,1,'root',".$now.",1,'root',".$now.",2)") or die("插入主题失败:<br/>".$db3->error."<br/>");
	
	$t->click('关闭topic');
	
	$db3->close();
	
	$t->click('开始打开post');
	
	$db4 = new db(array('db' => 'db/post.db.php' , 'mode' => 0777));
	
	$t->click('开始插入帖子');
	
	$db4->exec("insert into pin_post_base (id,topic_id,subject,content,add_time,user_id,user_ip,forum_id) values (1,1,'欢迎使用Pinbb论坛系统','欢迎使用Pinbb论坛系统\n作者:无限\n联系方式:jyf1987 at gmail dot com\n站点:[url]http://hi.baidu.com/jyf1987[/url]',".$now.",1,'*.*.*.*',2)");
	
	$db4->exec("insert into pin_post_base (id,topic_id,subject,content,add_time,user_id,user_ip,forum_id) values (2,1,'RE:欢迎使用Pinbb论坛系统','大家积极跟贴啊',".$now.",1,'*.*.*.*',2)");
	
	$t->click('关闭post');
	
	echo $t->dump('最后');