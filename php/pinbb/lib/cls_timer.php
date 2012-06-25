<?php
	/**
		utf-8 编码
	/**/
	class timer{
		private $_time;
		
		function __CONSTRUCT($desc=''){
			$this->_time = array();
			$this->_time[] = array(
				'desc'	=>	$desc,
				'time'	=>	microtime(true)
			);
		}
		
		function click($desc=''){
			$this->_time[] = array(
				'desc'	=>	$desc,
				'time'	=>	microtime(true)
			);
		}
		
		function clear(){
			$this->_time = array();
			return true;
		}
		
		function dump($desc=''){
			$this->_time[] = array(
				'desc'	=>	$desc,
				'time'	=>	microtime(true)
			);
			if(count($this->_time) < 2){
				return false;
			}
			$st = array_shift($this->_time);
			$result = <<<EOF
<table border="1">
	<tr>
		<td>段开始</td>
		<td>时间</td>
		<td>段结束</td>
		<td>时间</td>
		<td>耗时</td>
	</tr>
EOF;
			while($nt = array_shift($this->_time)){
				$result = $result . '<tr><td>' . $st['desc'] . "</td><td>".$st['time']."</td><td>" . $nt['desc'] . "</td><td>".$nt['time']."</td><td>" . ($nt['time']-$st['time']) . "</td></tr>";
				$st = $nt;
			}
			$result = $result . '</table>' ;
			return $result;
		}
	}