<?php
/**
$parser=xslt_create();
xslt_run($parser,'index.xsl','index.xml');
print xslt_fetch_result($parser);
xslt_free($parser);
**/
$xp = new XsltProcessor();
 $xsl = new DomDocument;
  $xsl->load('index.xsl');
  
  // import the XSL styelsheet into the XSLT process
  $xp->importStylesheet($xsl);
  
  // create a DOM document and load the XML datat
  $xml_doc = new DomDocument;
  $xml_doc->load('index.xml');
  
   if ($html = $xp->transformToXML($xml_doc)) {
      echo $html;
  } else {
      trigger_error('XSL transformation failed.', E_USER_ERROR);
  } // if 
?>