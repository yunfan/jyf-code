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
			<xsl:apply-templates select="page/block"/>
		</div>
		<div id="footer">
			<xsl:apply-templates select="page/message"/>
		</div>
	</body>
</html>

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

<xsl:template match="page/block">
	<div class="box" xmlns="http://www.w3.org/1999/xhtml">
	<p class="boxhead"><xsl:value-of select="name"/></p>
	<table cellspacing="0">
		<thead>
			<td class="fsttd">版块</td>
			<td>主题数</td>
			<td>帖子数</td>
			<td class="lsttd">最后发表</td>
		</thead>
		<tbody>
			<xsl:for-each select="forum">
				<tr>
					<td class="fsttd">
						<a><xsl:attribute name="href"><xsl:value-of select="href"/></xsl:attribute><xsl:value-of select="name"/></a><p><xsl:value-of select="desc"/></p>
					</td>
					<td><xsl:value-of select="topic"/></td>
					<td><xsl:value-of select="post"/></td>
					<td class="lsttd"><xsl:value-of select="last/time"/> by <xsl:value-of select="last/user"/></td>
				</tr>
			</xsl:for-each>
		</tbody>
	</table>
	</div>
</xsl:template>

<xsl:template match="page/message">
	<table style="width:100%;" xmlns="http://www.w3.org/1999/xhtml">
		<tr>
			<td style="padding-left:10px;">总共 用户/主题/帖子: <xsl:value-of select="total/user"/>/<xsl:value-of select="total/topic"/>/<xsl:value-of select="total/post"/> </td>
			<td>今日 用户/主题/帖子: <xsl:value-of select="today/user"/>/<xsl:value-of select="today/topic"/>/<xsl:value-of select="today/post"/></td>
			<td style="text-align:right;padding-right:10px;">Powered by <a><xsl:attribute name="href"><xsl:value-of select="author/href"/></xsl:attribute><xsl:value-of select="author/name"/></a><span class="split_4"></span><xsl:value-of select="author/time"/></td>
		</tr>
	</table>
</xsl:template>

</xsl:stylesheet>