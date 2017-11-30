rem arg is a captured filestore xml
REM cat %1 | xml sel -t -v "//*[local-name()='filestore']/location/directory[@name='local:/Esbf']/file/@name"
cat %1 | xml sel -t -v "//*[local-name()='filestore']/location/directory[@name='local:/Esbf']/directory[@name='local:/Esbf/Common']/file/@name"
