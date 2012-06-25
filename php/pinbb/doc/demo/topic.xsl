<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
	<html xmlns="http://www.w3.org/1999/xhtml">
		<head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" /> 
		<title><xsl:value-of select="page/title"/></title>
		<link rel="stylesheet" type="text/css" href="common.css" charset="utf-8"/>
		<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.3.1/jquery.min.js"></script>
		<script>
		</script>
	</head>
	<body>
		<div id="header">
			<div id="h-1"></div>
			<div id="h-2">
				<p class="h3"><xsl:value-of select="page/title"/></p>
				<p><xsl:value-of select="page/desc"/></p>
			</div>
			<xsl:apply-templates select="page/menu"/>
		</div>
		<div id="main">
			<xsl:apply-templates select="page/topic"/>
			<xsl:call-template name="form"/>
		</div>
		<div id="footer">
			<xsl:apply-templates select="page/message"/>
		</div>
	</body>
	</html>
</xsl:template>

<xsl:template name="form">
	<div xmlns="http://www.w3.org/1999/xhtml" class="form">
		<p class="formhead">发布新的帖子</p>
		<form method="post" action="index.php?act=thread.create">
			<input type="hidden" name="forum_id"><xsl:attribute name="value"><xsl:value-of select="/page/forum/id"/></xsl:attribute></input>
			<table cellspacing="0">
				<tbody>
				<tr>
					<td class="fsttd"><p>标题</p></td>
					<td class="lsttd"><input type="text" name="subject" style="width:60%;"/></td>
				</tr>
				<tr>
					<td class="fsttd"><p>内容</p></td>
					<td class="lsttd"><textarea name="content" cols="80" rows="5"></textarea></td>
				</tr>
				<tr>
					<td class="fsttd"><span></span></td>
					<td class="lsttd"><input type="submit"/><input type="reset"/></td>
				</tr>
				</tbody>
			</table>
		</form>
	</div>
</xsl:template>

<xsl:template match="page/menu">
	<div id="h-3" xmlns="http://www.w3.org/1999/xhtml">
		<ul>
			<xsl:for-each select="item">
				<li><a><xsl:attribute name="href"><xsl:value-of select="href"/></xsl:attribute><xsl:value-of select="name"/></a></li>
			</xsl:for-each>
		</ul>
	</div>
</xsl:template>

<xsl:template match="page/topic">
	<div class="box" xmlns="http://www.w3.org/1999/xhtml"> 
    	<p class="boxhead"><xsl:value-of select="/page/forum/name"/></p> 
    	<table cellspacing="0"> 
    		<thead> 
    			<tr> 
    				<td class="fsttd">标题</td> 
    				<td>浏览</td> 
    				<td>回复</td> 
    				<td class="lsttd">最后发表</td> 
    			</tr> 
    		</thead> 
    		<tbody>
    			<xsl:for-each select="item">
					<tr> 
						<td class="fsttd"><a><xsl:attribute name="href">index.php?act=thread&amp;id=<xsl:value-of select="id"/></xsl:attribute><xsl:value-of select="subject"/></a><br/>by <xsl:value-of select="user"/></td> 
						<td><xsl:value-of select="view"/></td> 
						<td><xsl:value-of select="reply"/></td> 
						<td class="lsttd"><a><xsl:attribute name="href">index.php?act=thread&amp;id=<xsl:value-of select="id"/>&amp;page=last</xsl:attribute><xsl:value-of select="last/time"/></a><br/>by <xsl:value-of select="last/user"/></td> 
					</tr> 
				</xsl:for-each>
    		</tbody> 
    	</table> 
		<xsl:apply-templates select="pages"/>
    	</div> 
</xsl:template>

<xsl:template match="pages">
	<p class="boxbottom text-align-right" xmlns="http://www.w3.org/1999/xhtml">
		<xsl:for-each select="item">
			<a class="no-under-line split"><xsl:attribute name="href">index.php?act=topic&amp;forum=<xsl:value-of select="/page/topic/id"/>&amp;page=<xsl:value-of select="page"/></xsl:attribute><xsl:value-of select="page"/></a>
		</xsl:for-each>
	</p>
</xsl:template>


<xsl:template match="page/message">
	<table style="width:100%;" xmlns="http://www.w3.org/1999/xhtml">
		<tr>
			<td style="padding-left:10px;">总共 用户/主题/帖子: <xsl:value-of select="total/user"/>/<xsl:value-of select="total/topic"/>/<xsl:value-of select="total/post"/> </td>
			<td>今日 用户/主题/帖子: <xsl:value-of select="today/user"/>/<xsl:value-of select="today/topic"/>/<xsl:value-of select="today/post"/></td>
			<td style="text-align:right;padding-right:10px;">Powered by <a><xsl:attribute name="href"><xsl:value-of select="author/href"/></xsl:attribute><xsl:value-of select="author/name"/></a><br/><xsl:value-of select="author/time"/></td>
		</tr>
	</table>
</xsl:template>

</xsl:stylesheet>