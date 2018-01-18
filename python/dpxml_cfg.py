# config file for dpxml

#svn_base = "http://slda325d.corpads.local/svn/DataPower/"

class env:
    def __init__(self, host, domain, creds, xmlport):
        self.host = host
        self.domain = domain
        self.creds = creds
        self.xmlport = xmlport

envs = {
    'sandbox': env(
        host='10.124.30.30',
        domain='sandbox',
        creds='jimr:markcare',
        xmlport='10550'),
    'dock10': env(
        host='10.124.30.30',
        domain='DBPL',
        creds='jimr:markcare',
        xmlport='10550'),
    'dock09': env(
        host='10.124.30.30',
        domain='DBPL',
        creds='jimr:altcare',
        xmlport='5550'),
    'null': env(
        host='',
        domain='',
        creds='',
        xmlport='')}
