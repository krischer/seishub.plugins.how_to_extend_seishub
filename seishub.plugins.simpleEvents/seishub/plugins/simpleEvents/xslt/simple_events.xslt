<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:output method="xml" indent="yes" encoding="UTF-8"/>
    
    <xsl:template match="/seismic_event">      
        <kml xmlns="http://www.opengis.net/kml/2.2">
            <Document>
                <Placemark>
                    <name>Event</name>
                    <description>Magnitude: <xsl:value-of select="magnitude" />, Time: <xsl:value-of select="time" /></description>
                    <Point>
                        <coordinates><xsl:value-of select="latitude" />, <xsl:value-of select="longitude" /></coordinates>
                    </Point>
                </Placemark>
            </Document>
        </kml>  
    </xsl:template>
    
</xsl:stylesheet>