# DP Build

Scripts to allow automated DataPower builds and configuration.

* Scripts named `dcm-*` need a working instance of IBM DCM
(DataPower Configuration Manager) to have been built in the
directory `~/dcm`.
* Scripts named `dp-*` directly call the SOMA interface of
a DataPower appliance.
* The scripts depend on the user setting and exporting a bash
environment varible called `dpenviron`.
* A DataPower environment is defined by a properties file in
a config directory, `$HOME/.dpbuild/$dpenviron.properties`.

Dependencies:
* java, ant (for DCM)
* xsltproc
* xmllint
* curl
* unzip
* docker
* groovy (binary in the path)
    - This specific path has to be used (and version), `/usr/share/groovy/groovy-2.4.12/bin/groovy` as this is hardwired in the code
    - Jenkins slave connection is not sourcing the bash_profile/bashrc as it is non-interactive and I dont want to update `/etc/profile` at this time.
