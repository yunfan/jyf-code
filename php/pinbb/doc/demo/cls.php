<?php
	class Pinbb{
		function __CONSTRUCT(){
			echo "Class Pinbb<br/>";
		}
		
		function toxml(){
		
		}
		
		function tojson(){
		
		}
	}
	
	class thread extends Pinbb{
		function __CONSTRUCT(){
			parent::__CONSTRUCT();
			echo "Class thread<br/>";
		}
	}
	
	$t = new thread();
?>