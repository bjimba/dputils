<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:dp="http://www.datapower.com/schemas/management"
    xmlns:dpm="http://www.datapower.com/schemas/management"
    xmlns:env="http://schemas.xmlsoap.org/soap/envelope/"
    exclude-result-prefixes="dp dpm env"
    >

    <xsl:template match="/">
        <xsl:apply-templates select="env:Envelope/env:Body/dp:response/dp:diff"/>
    </xsl:template>

    <xsl:template match="dp:diff">
        <diff>
            <new>
                <xsl:apply-templates select="node()[@new = 'true']"/>
            </new>
            <modified>
                <xsl:apply-templates select="node()[@modified = 'true']"/>
            </modified>
            <removed>
                <xsl:apply-templates select="node()[@removed = 'true']"/>
            </removed>
        </diff>
    </xsl:template>

    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>

    <!-- element nodes -->
    <xsl:template match="*">
        <xsl:element name="{name()}" namespace="{namespace-uri()}">
            <xsl:apply-templates select="@*|node()"/>
        </xsl:element>
    </xsl:template>

    <!--
    <xsl:template match="text()">
        <xsl:value-of select="."/>
    </xsl:template>

    <xsl:template match="@*">
        <xsl:copy/>
    </xsl:template>
    -->

</xsl:stylesheet>
