vmware_deploy_vro
=========

Deploys the vRealize Orchestrator Appliance from OVA and allows for the following configuration:
- Hostname (appliance hostname or VIP)
- SSL Certificate
- Authentication Provider (vSphere or vRealize Automation)
- Log Rotation Settings and Log Integration (LogInsight)
- NTP Configuration
- Install Plugins
- Import Packages
- Add Plugin Endpoints (SOAP, REST, vRA, vCenter, PowerShell, vAPI)

Supported vRealize Orchestrator Appliances
------------

- vRealize Orchestrator 7.5
- vRealize Orchestrator 7.6

Requirements
------------

- python >= 2.6
- PyVmomi

Role Variables
--------------

### The following parameters need to be defined in host_vars:

#### Network Configuration

Set Network Configuration for the appliance.
```
network_label: "VM Network"
network_ip_address: "x.x.x.x"
network_mask: "x.x.x.x"
network_gateway: "x.x.x.x"
```

#### Credentials and Access

Set the root username and password for this appliance.
```
vro_root_username: "root"
vro_root_password: "VMwar3!!"
```

The following credentials are used for BASIC auth to the vco API. Note that this API user must be a member of the vro_auth_adminGroup group.
```
vro_api_username: vro_api_user@sgroot.local
vro_api_password: VMwar3!!
```

Set the Ansible connection variables (use exactly as shown)
```
ansible_user: "{{ vro_root_username }}"
ansible_password: "{{ vro_root_password }}"
ansible_host: "{{ network_ip_address }}"
```

### The following mandatory parameters need to be defined, as extra vars, or in group_vars or host_vars:

#### OVA Deployment Variables

Set the OVA deployment variables.
```
ova_deployment_hostname: "vcenter/esxi hostname"
ova_deployment_username: "vcenter/esxi username"
ova_deployment_password: "vcenter/esxi password"
```

Set the target datastore. Datastore clusters are not supported by the module.
```
ova_deployment_datastore: "datastore"
```

The following are only required when deploying to vCenter Server. If folder is not defined then the appliance will deploy to the default folder.
```
ova_deployment_datacenter: "vcenter datacenter"
ova_deployment_cluster: "vcenter cluster"
ova_deployment_folder: "vcenter folder"
```

#### DNS Configuration

Set the DNS domain that should be used.
```
dns_domain: "example.com"
```

Provide a list of available DNS Servers.
```
dns_servers:
  - "x.x.x.x"
  - "x.x.x.x"
```

#### OVA Configuration

Set the OVA file name.
```
ova_file: "ova_file.ova"
```

Set the local path to the OVA file (do not use a leading /).
```
ova_path: "/path/to/ova_file"
```

#### Configure Authentication Provider

Set the auth provider to use for vRO authentication.

Auth provider is one of '**CAFE**' or '**VSPHERE**'.
```
vro_auth_provider: VSPHERE
vro_auth_hostname: host.example.com
vro_auth_username: administrator@vsphere.local
vro_auth_password: VMwar3!!
vro_auth_adminGroup: "vro-admins"
vro_auth_adminGroupDomain: "{{ dns_domain }}"
vro_auth_default_tenant: "vsphere.local"
```

### The following optional parameters can be defined, as extra vars, or in group_vars or host_vars:

#### OVA Download Configuration

Set the URL to the OVA file if '**ova_source**' is set to '**http**' (do not use a leading /). The '**ova_source**' variable defaults to '**local**' in the **vmware_deploy_ova** role and can be overridden.
```
ova_url: "http[s]://example.com/ova"
```

#### Load Balancer VIP

Set VIP hostname if using a load balancer. This will default to using the inventory hostname.
```
vro_vip_hostname: "vro.example.com"
```

#### Import CA Signed Certificates

Set '**vro_use_signed_certificate**' to '**yes**' if you would like to import CA signed certificates. The default setting is '**no**'.
```
vro_use_signed_certificate: no
```

If '**vro_use_signed_certificate**' is set to '**yes**', provide the certificate file in PEM format using the host name, as it has been defined in the hosts file (fqdn), with the extension .pem. The host certificate file should be placed in the '**files/certs**' directory. The PEM file must include the host certificate and CA chain.

#### System Logging

Provide the VMware LogInsight server details to send system logs to.

Valid protocol options are '**syslog**' and '**cfapi**'. Note that the '**cfapi**' protocol would typically use port 9000.
```
loginsight_server:
  host: "loginsight.example.com"
  port: 514
  protocol: syslog
```

Set log rotation parameters. The values displayed are the default.

Valid log levels are: '', '**ALL**', '**TRACE**', '**DEBUG**', '**INFO**', '**WARN**', '**ERROR**', '**FATAL**', '**OFF**'
```
vro_logging_globalLevel: "INFO"
vro_logging_maxFileCount: 10
vro_logging_maxFileSizeMb: 5
vro_logging_scriptingLevel: "INFO"
```

#### Install Plugins

Provide a list of plugins that should be installed. The plugin packages should be placed in the '**files/plugins**' folder.
```
vro_plugins:
  - plugin1.dar
  - plugin2.vmoapp
```

If a plugin is already installed, set the following variable to '**yes**' to force the plugin to be installed. The default value for this variable is '**no**'.
```
vro_force_plugin_install: no
```

#### Install Packages

Set the following variable to '**yes**' to allow vRO packages to be imported. The default value for this variable is '**no**'.
```
vro_install_packages: no
```

If '**vro_install_packages**' is set to '**yes**' then provide a list of packages that should be installed. The packages should be placed in the '**files/packages**' folder for the '**vmware_deploy_vro**' role.
```
vro_packages:
 - package1.package
 - package2.package
 ```

If a package version is already installed, set the following variable to '**yes**' to force the package to be installed. The default value for this variable is '**no**'.
```
vro_force_install_packages: no
```

#### Configure Plugin Endpoints

Set the following variable to '**yes**' to allow plugin endpoints to be added/configured. The default value for this variable is '**no**'. This will have a dependency on an authentication provider being configured and the API user a member of the specified adminGroup.
```
vro_configure_plugin_endpoints: no
```

If '**vro_configure_plugin_endpoints**' is set to '**yes** then provide a required plugin endpoint variables.

Add vCenter Server Endpoints. If you also want to add the vAPI endpoint, ensure this service has been started.
```
vcenter_plugin_endpoints:
  - hostname: "vcenter hostname"
    username: "vcenter username"
    password: "vcenter password"
    domain: "{{ dns_domain }}"
    add_vapi_endpoint: no
```

Add vRealize Automation Cafe Endpoints.
```
cafe_plugin_endpoints:
  - name: "Tenant A"
    hostname: "vra.example.com"
    tenant: "vsphere.local"
    username: "vra admin username"
    password: "vra admin password"
```

Add HTTP Restful API Endpoints. Supported authentication types are: '**Basic**' and '**OAuth2**'.

Uncomment and set proxy section if rest host is behind a proxy.
```
rest_plugin_endpoints:
  - name: Rest Host
    url: https://rest.example.com/api
    auth_type: Basic
    ## Username and Password is required when auth type is set to 'Basic'.
    username: "rest username"
    password: "rest password"
    ## OAuth2 Token is required when auth type is set to 'OAuth2'.
    # oauth2_token: "token"
    # proxy_host: proxy.example.com
    # proxy_port: 8080
    ## Proxy username and password can be left commented if proxy doesn't require authentication.
    # proxy_username: "{{ rest_plugin_endpoint_proxy_username }}"
    # proxy_password: "{{ rest_plugin_endpoint_proxy_password }}"
    host_verification: no
```

Add PowerShell Host Endpoints. Supported authentication types are: '**Basic**' and '**Kerberos**'.
```
powershell_plugin_endpoints:
  - name: PowerShell Host
    hostname: pshost.example.com
    port: 443
    auth_type: Basic
    username: "host username"
    password: "host password"
```

Add SOAP API Endpoints. Supported Authentication types are: '**Basic**', '**Digest**' and '**Kerberos**'.

Uncomment and set proxy section if SOAP host is behind a proxy.
```
soap_plugin_endpoints:
  - name: Soap Host
    wsdl_uri: soapuri.example.com
    auth_type: Basic
    ## Username and Password is required when auth type is set to 'Basic' or 'Digest'.
    username: "soap username"
    password: "soap password"
    ## Kerberos SPN is required when auth type is set to 'Kerberos'.
    # kerberos_spn: user@example.local
    # proxy_host: proxy.example.com
    # proxy_port: 8080
```

Set the following variable to '**yes**' if you would like to ignore any errors when adding plugin endpoints. This can be useful if re-running the playbook fails due to duplicate endpoints. The default value for this variable is '**no**'.
```
vro_ignore_plugin_endpoint_errors: no
```

### Additional default variables

The following additional default variables have also been set and can be overridden by setting them in a group_var.

#### Default list of NTP Servers that will be used.
```
ntp_servers:
  - "0.pool.ntp.org"
  - "1.pool.ntp.org"
  - "2.pool.ntp.org"
  - "3.pool.ntp.org"
```

#### HTTP REST API Variables
```
http_content_type: "application/json"
http_accept: "application/json"
http_validate_certs: no
http_body_format: "json"
```

Set the ports used by the vco and vco-controlcenter APIs.
```
vro_api_port: 8281
vro_cc_api_port: 8283
```

Enable SSH access to the appliance.
```
vro_enable_ssh: "True"
```

Enable Customer Experience Improvement Program.
```
vro_enable_telemetry: "False"
```

Dependencies
------------
  ```
  - { role: vmware_deploy_ova, tags: [ 'deploy' ] }
  ```
Example Playbook
----------------
    ```
    - hosts: vro_appliances
      become: no
      gather_facts: False
      roles:
        - nmshadey.vmware_deploy_vro
    ```

License
-------

MIT

Author Information
------------------

Gavin Stephens (https://www.simplygeek.co.uk)