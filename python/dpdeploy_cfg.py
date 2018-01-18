# config file for dpdeploy

svn_base = "http://slda325d.corpads.local/svn/DataPower/"

class env:
    def __init__(self, svn_env, dp_domain, friendly_name, hosts):
        self.svn_env = svn_env
        self.dp_domain = dp_domain
        self.friendly_name = friendly_name
        self.hosts = hosts

envs = {
    'SB': env(
        svn_env='SB',
        dp_domain='SANDBOX',
        friendly_name='Sandbox',
        hosts=['10.71.6.239']),
    'DEV': env(
        svn_env='DEV',
        dp_domain='DEV',
        friendly_name='Dev',
        hosts=['10.71.6.239', '10.71.1.27']),
    'SIT': env(
        svn_env='SIT',
        dp_domain='SIT',
        friendly_name='SIT',
        hosts=['10.71.6.239']),
    'UAT': env(
        svn_env='UAT',
        dp_domain='SIT',
        friendly_name='UAT',
        hosts=['10.71.6.239']),
    'PP': env(
        svn_env='PREPROD',
        dp_domain='PREPROD',
        friendly_name='PreProd',
        hosts=['10.71.6.239']),
    'DMZ': env(
        svn_env='PROD',
        dp_domain='PROD',
        friendly_name='DMZ-Prod',
        hosts=['10.71.6.239']),
    'LAN': env(
        svn_env='PROD',
        dp_domain='PROD',
        friendly_name='LAN-Prod',
        hosts=['10.71.6.239']),
    'ESB': env(
        svn_env='PROD',
        dp_domain='PROD',
        friendly_name='ESB-Prod',
        hosts=['10.71.6.239'])}

class project:
    def __init__(self, dp_domains=None):
        self.dp_domains = {'SB':'', 'DEV':'','SIT':'','UAT':'','PREPROD':'','PROD':''}
        if dp_domains:
            for k, v in dp_domains.items():
                self.dp_domains[k] = v

projects = {
        'enpi': project(dp_domains={'SB': 'SANDBOX2'}),
        'EnterpriseMemberSearch': project(dp_domains={'SB': 'SANDBOX2'}),
        'enterpriseprovidersearch': project(dp_domains={'SB': 'SANDBOX2'}),
        'FEMS': project(dp_domains={'SB': 'SANDBOX2'}),
        'Framework': project(dp_domains={'SB': 'SANDBOX2'}),
        'MECHABroker': project(dp_domains={'SB': 'SANDBOX2'}),
        'MemberCreate': project(dp_domains={'SB': 'SANDBOX2'}),
        'MemberSearchBroker': project(dp_domains={'SB': 'SANDBOX2'}),
        'NASCOInterAct': project(dp_domains={'SB': 'SANDBOX2'}),
        'NCCT': project(dp_domains={'SB': 'SANDBOX2'}),
        'ProviderBrokerService': project(dp_domains={'SB': 'SANDBOX2'}),
        'null', project()}

def get_dp_domain(project, env):
    return projects[project].dp_domains[env] or envs[env].dp_domain

