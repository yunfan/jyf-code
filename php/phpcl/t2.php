<?php
	define(DB , 'sqlite') ;
	include_once( "lib/db/cls_" . DB . ".php") ;

	//$t1 = microtime();
	
	$db = new db(array('db' => "category.db"));

	if(!$db){
		die("error: " . $db->error . "<br/>");
	}
	
	
	echo "<hr/>";

	echo "connect to db : ok <br/>";
	
	/**
	if(!$db->query("create table category(cat_id integer primary key,cat_name varchar(255) not null , parent_id integer not null default 0)")){
		die("cant create table : <br/>" . $db->error . "<br/>");
	}
	
	echo "<hr/>";
	echo "create table : ok <br/>";
	

	$t1 = microtime();

	for($i=1;$i<100;$i++){
		$cat_name = "DIR_$i";
		$parent_id = rand(0,($i-1));
		if(!$db->query("insert into category(cat_name , parent_id) values( '$cat_name' , $parent_id)")){
			die("cant insert to table category : <br/>" . $db->error . "<br/>");
		}
	}

	$t2 = microtime();
	/**/

	$raw = $db->fetch("select * from category order by cat_id desc","*a","ASSOC");
	/**
	echo "<pre>";
	print_r($raw);
	echo "</pre>"
	/**/
	
	$getit = array();
	$ref = array();
	$tree = array();
	
	$ct = 0 ;

	while(!empty($raw)){
		$cat = array_shift($raw);
		$id = $cat['cat_id'];
		$pid = $cat['parent_id'];
		//print_r($cat);
		//echo "\r\nTREE:";
		//print_r($tree);
		if($pid == 0){
			$tree[$id] = array('name' => $cat['cat_name'] , 'parent_id' => $pid , 'child' => array());
			$getit[] = $id;
			$ref[$id] =& $tree[$id];
		}
		elseif(in_array($pid , $getit)){
			//print_r($ref);
			$ref[$pid]['child'][$id] = array('name' => $cat['cat_name'] , 'parent_id' => $pid , 'child' => array());
			$getit[] = $id;
			$ref[$id] =& $ref[$pid]['child'][$id];
		}
		else{
			array_push($raw , $cat);
		}
		$ct = $ct + 1 ; 
	}
	echo "CT == $ct \r\n<br/>";
	/**/
	echo "<pre>";
	print_r($tree);
	echo "</pre>"
	/**/

?>
