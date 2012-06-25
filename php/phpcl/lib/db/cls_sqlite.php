<?php
	class db{
		private $handler;
		public $error;
		public $type = "sqlite";
	

		function __CONSTRUCT($setting = array()){
			if(!array_key_exists('db' , $setting)){
				$this->error = "You havent set the db name!";
				return false;
			}
			if(!array_key_exists('mode' , $setting)){
				$setting['mode'] = 0666;
			}
			if($this->handler = sqlite_open($setting['db'] , $setting['mode'] , $this->error)){
				return true;
			}else{
				return false;
			}
		}
		
		function check($sql){
			if(empty($sql)){
				$this->error = "SQL query is empty!";
				return false;
			}
		}

		function query($sql){
			$this->check($sql);
			
			if($rp = sqlite_exec($this->handler , $sql , $this->error)){
				return true;
			}else{
				return false;
			}
		}

		function fetch($sql , $type = "*a" , $result_type = "BOTH"){
			$this->check($sql);
			
			if(!in_array($type , array("*o" , "*l" , "*a"))){
				$this->error = "type is not support";
				return false;
			}
			
			if(!in_array($result_type , array("ASSOC" , "NUM" , "BOTH"))){
				$this->error = "sort type is not support";
				return false;
			}
			$sort_type = constant("SQLITE_".$result_type);


			$res = sqlite_query($this->handler , $sql , $this->error);
			
			if(!$res){
				return false;
			}
			
			if(sqlite_num_rows($res) == 0 ){
				$this->error = "empty return";
				return false;
			}

			switch($type){
				
				case "*o":
					return sqlite_fetch_single($res);
				case "*l":
					return sqlite_fetch_array($res , $sort_type);
				case "*a":
					return sqlite_fetch_all($res , $sort_type);
			}
		}
		
		function __DESTRUCT(){
			sqlite_close($this->handler);
		}
	}
?>
