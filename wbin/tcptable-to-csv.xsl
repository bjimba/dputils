<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:dp="http://www.datapower.com/schemas/management"
    xmlns:dpm="http://www.datapower.com/schemas/management"
    xmlns:env="http://schemas.xmlsoap.org/soap/envelope/"
    exclude-result-prefixes="dp dpm env"
    >

    <xsl:output method="text"/>

    <xsl:variable name="nl" select="'&#10;'"/>

    <xsl:template match="/">
        <xsl:text>Local IP,Local port,Remote IP,Remote port,State,Service Domain,Service Class,Service Name</xsl:text>
        <xsl:value-of select="$nl"/>
        <xsl:apply-templates select="env:Envelope/env:Body/dp:response/dp:status/TCPTable"/>
    </xsl:template>

    <xsl:template match="TCPTable">
        <xsl:value-of select="concat(
            localIP,
            ',',
            localPort,
            ',',
            remoteIP,
            ',',
            remotePort,
            ',',
            state,
            ',',
            serviceDomain,
            ',',
            serviceClass,
            ',',
            serviceName,
            $nl)"/>
    </xsl:template>
</xsl:stylesheet>
