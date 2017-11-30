<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:dp="http://www.datapower.com/schemas/management"
  xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
  >

  <!--
  Convert get-filestore to a SOMA request to remove all local files
  -->

  <xsl:param name="dpdomain" select="'unknown'"/>

  <xsl:template match="/">
    <xsl:apply-templates
      select="soapenv:Envelope/soapenv:Body
      /dp:response/dp:filestore/location"/>
  </xsl:template>

  <xsl:template match="location">
    <soapenv:Envelope>
      <soapenv:Body>
        <dp:request domain="{$dpdomain}">
          <dp:do-action>
            <xsl:apply-templates select="directory"/>
            <xsl:apply-templates select="file"/>
          </dp:do-action>
        </dp:request>
      </soapenv:Body>
    </soapenv:Envelope>
  </xsl:template>

  <xsl:template match="directory">
    <RemoveDir>
      <Dir>
        <xsl:value-of select="@name"/>
      </Dir>
    </RemoveDir>
  </xsl:template>

  <xsl:template match="file">
    <DeleteFile>
      <File>
        <xsl:value-of select="concat('local:///', @name)"/>
      </File>
    </DeleteFile>
  </xsl:template>

</xsl:stylesheet>
