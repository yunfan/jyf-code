<?php
	//mail:	jyf1987@gmail.com
	//url:		http://hi.baidu.com/jyf1987
	//单文件多输出
	//error_reporting(0);
	/////////////////////////////////////////////////////////////////////
	////主程序
	$admin_pass="wuxian";                  //管理员密码
	$board_title="无限的留言板";       //留言本标题
	$board_page=10;                       //每页显示留言个数
	$mod=(!isset($_GET['mod']))?'show':$_GET['mod'];
	$page=$_SERVER['PHP_SELF'];
	$page=array_pop(explode('/',$page));
	//echo $page;
	switch($mod){
		case 'show':show_note();return;
		case 'add':add_note();return;
		case 'del':del_note();return;
		case 'reply':reply_note();return;
		case 'install':install();return;
		case 'css':show_css();return;
	}
	
	/////////////////////////////////////////////////////////////////////
	///一些函数库
	function chk(){
		$res=true;
		$argnum = func_num_args();
		if($argnum>=2){
			$v=func_get_args();
		}else{
			$v=func_get_arg(0);
		}
		if(is_array($v)){
			foreach($v as $a){
				if(!isset($a) || ($a=="")){
					$res=false;
					break;
				}
			}
			return $res;
		}else{
			if(!isset($v) || ($v=="")){
				return false;
			}else{
				return true;
			}
		}
	}
	class sqlitedb{
		private $sqlerror,$rs;
		public $handle;
		//构建函数
		function __construct($fp){
			if($this->handle=sqlite_open($fp,0666,$this->sqlerror)){
				return true;
			}else{
				die($this->sqlerror);
			}
		}

		//执行sql语句函数
		function exec($sql){
			if($this->rs=sqlite_query($this->handle,$sql)){
				return true;
			}else{
				die($this->sqlerror);
			}
		}
		
		//或许结果行数函数
		function get_num(){
			return sqlite_num_rows($this->rs);
		}
		
		//获取单行
		function get_single(){
			return sqlite_fetch_single($this->rs);
		}
		
		//执行查询返回数据
		function qfetch($sql){
			$this->rs=sqlite_query($this->handle,$sql,SQLITE_BOTH,$sqlerror);
			if(isset($sqlerror)){
				$this->sqlerror=$sqlerror;
				return false;
			}else{
				return sqlite_fetch_all($this->rs);
			}
		}
		
		//返回最后一次插入的id
		function insert_id(){
			return sqlite_last_insert_rowid($this->handle);
		}
	}
	
	/////////////////////////////////////////////////////////////////////////
	///模块功能
	function show_note(){
		global $page,$board_title,$board_page;
		$s=(int)(!isset($_GET['s']))?0:$_GET['s'];
		$cmd1="select count(*) from notes where show=0";
		$db=new sqlitedb("notes.db.php");
		$r1=$db->exec($cmd1);
		if(!$r1){
			$linkpage="对不起,无法统计留言数量";
		}else{
			$total=(int)($db->get_single());
			if($total<$board_page){
				$linkpage="";
			}else{
				$s1=$s*$board_page;
				if($s1<$total && $total-$s1>$board_page){
					$p1=$s-1;
					$p2=$s+1;
					if($p1<0){
						$linkpage=<<<EOF
					<div class="link"><a href="{$page}?mod=show&s={$p2}">下一页</a></div>
EOF;
					}else{
						$linkpage=<<<EOF
					<div class="link"><a href="{$page}?mod=show&s={$p1}">上一页</a>&nbsp;&nbsp;<a href="{$page}?mod=show&s={$p2}">下一页</a></div>
EOF;
}
				}else{
					if($s1<$total && $total-$s1<$board_page){
						$p1=$s-1;
						if($p1<0){
							$linkpage="";
						}else{
							$linkpage=<<<EOF
<div class="link"><a href="{$page}?mod=show&s={$p1}">上一页</a></div>
EOF;
}
					}
				}
			}
		}
		//$cmd2='select * from notes where show=0 order by id desc limit '.$board_page.' offset '.$s1;
		$s1=$s*$board_page;
		$cmd2='select * from notes where show=0 order by id desc limit '.$s1.','.$board_page;
		$r2=$db->qfetch($cmd2);
		if(!r2){
			$str="对不起,查询发生错误<br/>";
		}else{
			if($db->get_num()<1){
				$str="对不起,查询不到结果<br/>";
			}else{
				$line_1='<div class="bigdiv">';
				$line_2='<div class="c1"><font color="silver">呢称:</font>';
				$line_3='</div><div class="c2"><font color="silver">内容:</font><br>';
				$line_4='</div></div>';            //定义模块单位内容
				$str='';
				foreach($r2 as $item){
					$str.=$line_1;
					$str.=$line_2;
					$str.=$item['name']."  提交于  ".$item['time']."&nbsp;&nbsp;&nbsp;&nbsp;"."<a href=".$page."?mod=del&id=".$item['id'].">x</a>";
					$str.=$line_3;
					$str.=$item['content'];
					$str.=$line_4;
				}
			}
		}
		header("Content-Type:text/html; charset=UTF-8");
		print <<<EOF
<html>
	<head>
		<title>{$board_title}</title>
		<link href="{$page}?mod=css" type="text/css" rel="stylesheet">
	</head>
	<body>
		<div class="title">
			<center>{$board_title}</center>
		</div>
		{$str}
		<div>{$linkpage}</div>
		<div class="senddiv">
<form name="myform" action="{$page}?mod=add" method="POST" style="margin:0px;width:795px;">
用户名:<input type="text" name="n" style="border-style:solid;">&nbsp;&nbsp;&nbsp;&nbsp;悄悄话:<input name='s' type='checkbox'><br>
内&nbsp;&nbsp;容:<br>
<textarea name="c" style="border-style:solid;width:790px;margin:0px;height:80px;">
</textarea>
<input type="submit" value="提&nbsp;&nbsp;交">
<input type="reset" value="重&nbsp;&nbsp;填">
</FORM>
</div>
<div>
<CENTER>
powered by <A HREF="http://hi.baidu.com/jyf1987">创亿无限</A></CENTER>
</div>
</body>
</html>
	</body>
</html>
EOF;
	}
	function add_note(){
		//print 'this is add_note';
		global $page;
		$time=date('Y:m:d H:i:s');
		$n=htmlspecialchars($_POST['n']);
		$s=htmlspecialchars($_POST['s']);
		$c=nl2br(htmlspecialchars($_POST['c']));
		if(!chk($n)){
			$n='匿名用户@'.$_SERVER['REMOTE_ADDR'];
		}
		if(!chk($c)){
			header("Content-Type:text/html; charset=utf-8");
			print <<<EOF
对不起，没有您还没有输入内容!<br/>
<a href="{$page}?mod=show">点此返回</a>
EOF;
			exit;
		}
		if(!chk($s)){
			$cmd1="insert into notes(name,content,show,time) values('".$n."','".$c."',0,'".$time."')";
		}else{
			$cmd1="insert into notes(name,content,show,time) values('".$n."','".$c."',1,'".$time."')";
		}
		$db=new sqlitedb("notes.db.php");
		$r1=$db->exec($cmd1);
		if(!$r1){
			header("Content-Type:text/html; charset=utf-8");
			print <<<EOF
对不起，由于未知的错误无法添加留言到数据库中!<br/>
<a href="{$page}?mod=show">点此返回</a>
EOF;
			exit;
		}
		header("Content-Type:text/html; charset=utf-8");
		print <<<EOF
恭喜，留言已成功添加到数据库中!<br/>
<a href="{$page}?mod=show">点此返回</a>
EOF;
	}
	function del_note(){
		//print 'this is del_note';
		global $page,$admin_pass;
		session_start();
		if(!chk($_SESSION['is_admin'])){
			$did=(int)htmlspecialchars($_GET['id']);
			if(!chk($did) || $did<0){
				header("Content-Type:text/html; charset=utf-8");
				print <<<EOF
对不起,您输入的id不正确<br/>
<a href="{$page}?mod=show">返回</a>
EOF;
			exit;
			}
			$pass=htmlspecialchars($_GET['pass']);
			if(chk($pass)){
				if($pass==$admin_pass){
					$_SESSION['is_admin']=true;
					header("location:".$page."?mod=del&id=".$did);
				}else{
					header("Content-Type:text/html; charset=utf-8");
					print <<<EOF
对不起,您输入的密码不正确<br/>
<a href="{$page}?mod=show">返回</a>
EOF;
				}
			}else{
				header("Content-Type:text/html; charset=utf-8");
				print <<<EOF
<center>请输入密码:</center>
<form method="GET" action="{$page}">
<input type="hidden" name="mod" value="del">
<input type="hidden" name="id" value="{$did}">
密码:<input type="password" name="pass"/><br/>
<input type="submit">
</form>
<a href="{$page}?mod=show">返回</a>
EOF;
			}
		}else{
			$did=(int)htmlspecialchars($_GET['id']);
			$cmd1="delete from notes where id=".$did;
			$db=new sqlitedb("notes.db.php");
			$r1=$db->exec($cmd1);
			if(!r1){
				header("Content-Type:text/html; charset=utf-8");
				print <<<EOF
对不起,未能删除成功!<br/>
<a href="{$page}?mod=show">返回</a>
EOF;
			exit;
			}
			header("Content-Type:text/html; charset=utf-8");
			print <<<EOF
删除成功!<br/>
<a href="{$page}?mod=show">返回</a>
EOF;
			exit;
			}
	}
	function reply_note(){
		print 'this is reply_note';
	}
	function install(){
		$ccmd="create table '<?php' (test integer)";
		$cmd1="create table notes(
			id integer primary key,
			name varchar(32) not null,
			content text not null,
			show integer not null,
			time varchar(19) not null
		)";
		$db=new sqlitedb("notes.db.php");
		$r1=$db->exec($ccmd);
		$r2=$db->exec($cmd1);
		unset($db);
		header("Content-Type:text/html; charset=utf-8");
		if(!$r1){
			echo "sorry 表1没有建立成功!";
			exit;
		}
		echo "表1建立成功!<br/>";
		if(!$r2){
			echo "sorry 表2没有建立成功!";
			exit;
		}
		echo "表2建立成功!<br/>";
		exit;
	}
	function show_css(){
		print <<<EOF
body{padding:0px 45px 0px 45px;
	  margin:0px 45px 0px 45px;
	  background-color:silver;
	 }
.title center{
	font-size:32px;
	margin-top:10px;
		}

.bigdiv{border-style:solid;
        border-color:black;
		border-width:1px;
		background-color:#7B87B7;
		margin:5px;
		color:white;
		width:805px;
		}
.link{border-style:solid;
        border-color:black;
		border-width:1px;
		background-color:#7B87B7;
		margin:5px;
		color:white;
		text-align:right;
		width:805px;
}
.bigdiv a{text-decoration:none;color:red;}
.c1{width:800px;margin:5px 0px 0px 5px;padding:0px;background-color:#7B87B7;position:relative;}
.c2{width:800px;margin:5px 0px 0px 5px;padding:0px;background-color:#7B87B7;position:relative;}

.senddiv{border-style:solid;border-width:1px;width:796px;*width:805px;margin:5px 0px 0px 5px;padding:5px;background-color:white;position:relative;font-size:15px;}
EOF;
	}
?>