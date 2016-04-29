"""
Example InterDC SO providing multi-region L3 connectivity.

+------+       +------+
|Site A| <---> |Site B|
+------+       +------+

Site A is always a server side of the OpenVPN tunnel.
Site B is always a client side of the OpenVPN tunnel.

Currently it is possible to orchestrate the connection
on OpenStack and CloudStack platforms (os<->cs, cs<->cs, cs<->os)

Therefore platform types must be one of the following options:
cs - CloudStack platform
os - OpenStack platform
"""

import netaddr
import os
import time

from sdk.mcn import util
from sm.so import service_orchestrator
from sm.so.service_orchestrator import LOG

class SOE(service_orchestrator.Execution):

    def __init__(self, token, tenant):
        super(SOE, self).__init__(token, tenant)
        self.site_A_stack_id = None
        self.site_B_stack_id = None

        # TODO
        # CIDRs, platform types and regions will be provided
        # as input parameters.
        self.site_A_CIDR = '10.2.0.0/24'
        self.site_B_CIDR = '10.2.4.0/24'
        self.site_A_platform = 'cs'
        self.site_B_platform = 'os'
        self.site_A_region = 'CloudStack'
        self.site_B_region = 'RegionOne'

        self.site_A = netaddr.IPNetwork(self.site_A_CIDR)
        self.site_B = netaddr.IPNetwork(self.site_B_CIDR)
        self.site_A_net = str(self.site_A.ip)
        self.site_B_net = str(self.site_B.ip)
        self.site_A_gw = str(self.site_A.ip + 1)
        self.site_B_gw = str(self.site_B.ip + 1)
        self.site_A_mask = str(self.site_A.netmask)
        self.site_B_mask = str(self.site_B.netmask)

        self.site_A_deployer = util.get_deployer(
            token, url_type='public', tenant_name=tenant,
            region=self.site_A_region)
        self.site_B_deployer = util.get_deployer(
            token, url_type='public', tenant_name=tenant,
            region=self.site_B_region)

    def design(self):
        LOG.info('Entered design() - nothing to do here')
        pass

    def deploy(self):
        """Deploy L3 connection

        Note that all HOTs require providing your environment
        specific details such as VM flavours, available network
        offerings, management ssh & CloudStack APIs keys, etc.
        """
        LOG.info('Deploying...')
        path = os.path.dirname(os.path.abspath(__file__))
        cp = os.path.dirname(os.path.abspath(__file__))
        HOT_dir = os.path.abspath(os.path.join(cp, '../../../', 'HOT'))
        HOT_A_path = os.path.join(HOT_dir, str(self.site_A_platform) + '-server-keys.yaml')
        HOT_B_path = os.path.join(HOT_dir, str(self.site_B_platform) + '-client-keys.yaml')

        params = {
            'subnet_A': self.site_A_net,
            'subnet_B': self.site_B_net,
            'gateway_A': self.site_A_gw,
            'gateway_B': self.site_B_gw,
            'mask_A': self.site_A_mask,
            'mask_B': self.site_B_mask,
            'cidr_A': self.site_A_CIDR,
            'cidr_B': self.site_B_CIDR,
        }
        LOG.info('Params: %s' % params)

        if self.site_A_stack_id is None:
            """OpenVPN Server endpoint"""
            with open(HOT_A_path, 'r') as f:
                template = f.read()
            script_A_path = os.path.join(HOT_dir, 'scripts/setup_server.sh')
            with open(script_A_path, 'r') as f:
                script_A = f.read()
            params['script'] = script_A
            print script_A
            self.site_A_stack_id = self.site_A_deployer.deploy(
                template, self.token, parameters=params)
            LOG.info('Site A stack ID: ' + self.site_A_stack_id.__repr__())

        # Wait for server side to be created so server's public IP can
        # be passed to the client. This could be probably solved more elegantly
        # by applying configuration in the provisioning phase.
        # TODO: Modify HOT so they only inject SSH keys and proceed
        # with config using fabric in the next phase.
        while(self.site_A_deployer.details(
                self.site_A_stack_id, self.token)['state'] == 'CREATE_IN_PROGRESS'):
            time.sleep(10)

        # TODO handle possible failure
        # For now just expecting that stack A was created sucessfully.

        if self.site_B_stack_id is None:
            """OpenVPN Client endpoint"""
            print self.site_A_deployer.details(self.site_A_stack_id, self.token)
            vpn_server_external_ip = str(self.site_A_deployer.details(
                self.site_A_stack_id, self.token)['output'][0]['output_value'])
            params['vpn_server_external_ip'] = vpn_server_external_ip
            with open(HOT_B_path, 'r') as f:
                template = f.read()
            script_B_path = os.path.join(HOT_dir, 'scripts/setup_client.sh')
            with open(script_B_path, 'r') as f:
                script_B = f.read()
            params['script'] = script_B
            print script_B
            self.site_A_stack_id = self.site_B_deployer.deploy(
                template, self.token, parameters=params)
            LOG.info('Site B stack ID: ' + self.site_B_stack_id.__repr__())

    def provision(self):
        """
        Not much to do here. Just adjust routing on both sites.
        """
        LOG.info('Calling provision...')

    def dispose(self):
        """
        Dispose SICs
        """
        LOG.info('Calling dispose...')
        if self.site_A_stack_id is not None:
            LOG.debug('Deleting stack: %s' % self.site_A_stack_id)
            self.site_A_deployer.dispose(self.site_A_stack_id, self.token)
            self.site_A_stack_id = None
        if self.site_B_stack_id is not None:
            LOG.debug('Deleting stack: %s' % self.site_B_stack_id)
            self.site_B_deployer.dispose(self.site_B_stack_id, self.token)
            self.site_B_stack_id = None

    def state(self):
        """
        Report on state for both stacks in site_A and site_B
        """
        if self.site_A_stack_id is not None and self.site_B_stack_id is not None:
            tmp = self.site_A_deployer.details(self.site_A_stack_id, self.token)
            print tmp
            site_A_stack_state = tmp['state']
            LOG.info('Returning Stack output state of site_A')
            # XXX type should be consistent
            site_A_output = ''
            try:
                site_A_output = tmp['output']
            except KeyError:
                pass

            tmp = self.site_B_deployer.details(self.site_B_stack_id, self.token)
            print tmp
            site_B_stack_state = tmp['state']
            LOG.info('Returning Stack output state of site_B')
            site_B_output = ''
            try:
                site_B_output = tmp['output']
            except KeyError:
                pass

            return [
                site_A_stack_state, site_B_stack_state], [
                self.site_A_stack_id, self.site_B_stack_id], [
                site_A_output, site_B_output]
        else:
            LOG.info('Stack output: none - Unknown, N/A')
            return 'Unknown', 'N/A', None

    def update(self, old, new, extras):
        # TODO implement your own update logic - this could be a heat template
        # update call
        LOG.info('Calling update - nothing to do!')


class SOD(service_orchestrator.Decision):
    """
    Sample Decision part of SO.
    """

    def stop(self):
        pass

    def __init__(self, so_e, token, tenant):
        super(SOD, self).__init__(so_e, token, tenant)

    def run(self):
        """
        Decision part implementation goes here.
        """
        pass


class ServiceOrchestrator(object):
    """
    Sample SO.
    """

    def __init__(self, token, tenant):
        self.so_e = SOE(token, tenant)
        self.so_d = SOD(self.so_e, token, tenant)
        # so_d.start()
