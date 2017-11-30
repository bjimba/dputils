<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <!--
  Remove files section from XCFG
  -->

  <xsl:strip-space elements="*"/>

  <xsl:template match="/">
    <xsl:apply-templates/>
  </xsl:template>

  <!-- by default, copy everything (identity transform) -->

  <xsl:template match="@* | node()">
    <xsl:copy>
      <xsl:apply-templates select="@* | node()" />
    </xsl:copy>
  </xsl:template>

  <!-- whitespace -->
  <xsl:template match="text()">
    <xsl:value-of select="normalize-space(.)"/>
  </xsl:template>

  <!-- nodes to drop -->
  <xsl:template match="/datapower-configuration/files"/>

</xsl:stylesheet>
