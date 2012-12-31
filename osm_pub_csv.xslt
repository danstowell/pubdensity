<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
<!--
Converts OSM xml to CSV, designed to extract pub data. 
(c) Dan Stowell 2012.
NB, Currently the processing includes two unrealistic oversimplifications:
(1) "way" geolocations are chosen as a random one of their nodes' location, rather than centroid. No problem when using for country-scale analysis.
(2) "relation" items marked as pubs are not yet processed. At time of writing this only misses two pubs in whole dataset, so not too bad.
USAGE:
xsltproc osm_pub_csv.xslt data/overpass_allpubs.xml > data/overpass_allpubs.csv && less data/overpass_allpubs.csv
-->

    <!-- This "key" declaration speeds up by a million million times, the lookup from ways back to nodes -->
    <xsl:key name="nodeid" match="node" use="@id"/>

    <xsl:variable name="delim" select="'&#x9;'"/>

    <xsl:output method="text"/>
    <xsl:template match="/">

        <!-- Column headers -->
        <xsl:text>id</xsl:text>
        <xsl:value-of select="$delim"/>
        <xsl:text>lat</xsl:text>
        <xsl:value-of select="$delim"/>
        <xsl:text>lon</xsl:text>
        <xsl:value-of select="$delim"/>
        <xsl:text>datatype</xsl:text>
        <xsl:value-of select="$delim"/>
        <xsl:text>name</xsl:text>
        <xsl:value-of select="$delim"/>
        <xsl:text>real_ale</xsl:text>
        <xsl:value-of select="$delim"/>
        <xsl:text>toilets</xsl:text>
        <xsl:value-of select="$delim"/>
        <xsl:text>food</xsl:text>
        <xsl:value-of select="$delim"/>
        <xsl:text>wifi&#xa;</xsl:text>

        <!-- Node pubs -->
        <xsl:for-each select="osm/node">
          <xsl:choose>
          <xsl:when test="tag[@k='amenity'][@v='pub']">
	    <xsl:value-of select="@id"/>
	    <xsl:value-of select="$delim"/>
	    <xsl:value-of select="@lat"/>
	    <xsl:value-of select="$delim"/>
            <xsl:value-of select="@lon"/>
	    <xsl:value-of select="$delim"/>
            <xsl:text>n</xsl:text>
	    <xsl:value-of select="$delim"/>
	    <xsl:apply-templates select="tag[@k='name']"/>
	    <xsl:value-of select="$delim"/>
	    <xsl:apply-templates select="tag[@k='real_ale']"/>
	    <xsl:value-of select="$delim"/>
	    <xsl:apply-templates select="tag[@k='toilets']"/>
	    <xsl:value-of select="$delim"/>
	    <xsl:apply-templates select="tag[@k='food']"/>
	    <xsl:value-of select="$delim"/>
	    <xsl:apply-templates select="tag[@k='wifi']"/>
            <xsl:text>&#xa;</xsl:text>
          </xsl:when>
          </xsl:choose>
        </xsl:for-each>

        <!-- Way pubs -->
        <xsl:for-each select="osm/way">
          <xsl:choose>
          <xsl:when test="tag[@k='amenity'][@v='pub']">
            <xsl:variable name="nodeid" select="nd/@ref"/> <!-- Grab ONE (arbitrarily chosen) of the nodes referenced by this way. -->
	    <xsl:value-of select="@id"/>
	    <xsl:value-of select="$delim"/>
	    <xsl:value-of select="key('nodeid', $nodeid)/@lat"/>
	    <xsl:value-of select="$delim"/>
	    <xsl:value-of select="key('nodeid', $nodeid)/@lon"/>
	    <xsl:value-of select="$delim"/>
            <xsl:text>w</xsl:text>
	    <xsl:value-of select="$delim"/>
	    <xsl:apply-templates select="tag[@k='name']"/>
	    <xsl:value-of select="$delim"/>
	    <xsl:apply-templates select="tag[@k='real_ale']"/>
	    <xsl:value-of select="$delim"/>
	    <xsl:apply-templates select="tag[@k='toilets']"/>
	    <xsl:value-of select="$delim"/>
	    <xsl:apply-templates select="tag[@k='food']"/>
	    <xsl:value-of select="$delim"/>
	    <xsl:apply-templates select="tag[@k='wifi']"/>
            <xsl:text>&#xa;</xsl:text>
          </xsl:when>
          </xsl:choose>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="tag">
            <xsl:value-of select="@v"/>
    </xsl:template>

</xsl:stylesheet>

