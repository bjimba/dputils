<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <!--
  List config objects
  -->

  <xsl:strip-space elements="*"/>

  <xsl:template match="/">
    <xsl:apply-templates/>
  </xsl:template>

  <!-- copy everything (identity transform) -->
  <xsl:template match="/datapower-configuration">
    <xsl:copy>
      <xsl:apply-templates select="@* | node()" />
    </xsl:copy>
  </xsl:template>

  <xsl:template match="/datapower-configuration/configuration">
    <xsl:copy>
      <xsl:apply-templates select="@* | node()" />
    </xsl:copy>
  </xsl:template>

  <!-- shallow copy, dropping namespace -->
  <xsl:template match="node()">
    <xsl:element name="{local-name()}">
      <xsl:apply-templates select="@*" />
    </xsl:element>
  </xsl:template>
  <xsl:template match="@*">
    <xsl:copy/>
  </xsl:template>

  <!-- whitespace -->
  <xsl:template match="text()">
    <xsl:value-of select="normalize-space(.)"/>
  </xsl:template>

  <!-- nodes to drop -->
  <xsl:template match="/datapower-configuration/files"/>
  <xsl:template match="@read-only"/>

</xsl:stylesheet>
