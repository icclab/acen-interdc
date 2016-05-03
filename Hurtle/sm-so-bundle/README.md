InterDC connectivity Hurtle SO-SM bundle
========================================

Repository structure:

 * `./wsgi` contains WSGI application and SO implementation.
 * `./data` contains Heat orchestration templates (HOTs) describing infrastructual graph and basic scripts for initial resource setup.
 * `./scripts` contains request examples for service initialization, deployment, provisioning and deletion.

## RUN SM localy

```DESIGN_URI=http://keystone_url:35357/v2.0 OPENSHIFT_REPO_DIR=$PWD python ./wsgi/application```

## Service Attributes

Service instance configuration must be provided in the headers of the init PUT HTTP request.

Service instance requires following attributes:

 * `acen.interdc.site_A.cidr` server side network CIDR,
 * `acen.interdc.site_B.cidr` client side network CIDR,
 * `acen.interdc.site_A.platform` server side cloud platform type,
 * `acen.interdc.site_B.platform` client side cloud platform type,
 * `acen.interdc.site_A.region` server side region,
 * `acen.interdc.site_B.region` client side region,

which are specified in the header as follows:

```-H 'X-OCCI-Attribute: ATRIBUTE_NAME="ATTRIBUTE_VALUE"'```

e.g.:

```-H 'X-OCCI-Attribute: acen.interdc.site_A.cidr="10.2.0.0/24"'```

Both CIDRs must be valid non-conflicting CIDR ranges.

Currently OpenStack and CloudStack platforms are supported. Note that orchestration of CloudStack resources is not supported by Heat nativly. To change that, please install and configure [Heat CloudStack plugin](https://github.com/icclab/cloudstack-heat). Also note that platform values must be one of the following values: `os` for OpenStack regions and `cs`for CloudStack regions.

Regions must be valid OpenStack regions in your deployment. Always make sure that specified region and platform don't colide.

Other cloud environment specific values needs to be modified accordinglyto match your deployment in provided infrastructural templates.

## Sample requests

Before issuing following requests set `KID` and `TENANT` environment variables accordingly:
 * `KID` - Keystone token ID.
 * `TENANT` - Tenant name.

Initialize the SO:

    $curl -v -X PUT http://localhost:8051/orchestrator/default \
        -H 'Content-Type: text/occi' \
        -H 'Category: orchestrator; scheme="http://schemas.mobile-cloud-networking.eu/occi/service#"' \
        -H 'X-Auth-Token: '$KID \
        -H 'X-Tenant-Name: '$TENANT \
        -H 'X-OCCI-Attribute: acen.interdc.site_A.cidr="10.2.0.0/24"' \
        -H 'X-OCCI-Attribute: acen.interdc.site_B.cidr="10.2.4.0/24"' \
        -H 'X-OCCI-Attribute: acen.interdc.site_A.platform="cs"' \
        -H 'X-OCCI-Attribute: acen.interdc.site_B.platform="os"' \
        -H 'X-OCCI-Attribute: acen.interdc.site_A.region="CloudStack"' \
        -H 'X-OCCI-Attribute: acen.interdc.site_B.region="RegionOne"'

Get state of the SO + service instance:

    $ curl -v -X GET http://localhost:8051/orchestrator/default \
          -H 'X-Auth-Token: '$KID \
          -H 'X-Tenant-Name: '$TENANT

Trigger deployment of the service instance:

    $ curl -v -X POST http://localhost:8051/orchestrator/default?action=deploy \
          -H 'Content-Type: text/occi' \
          -H 'Category: deploy; scheme="http://schemas.mobile-cloud-networking.eu/occi/service#"' \
          -H 'X-Auth-Token: '$KID \
          -H 'X-Tenant-Name: '$TENANT

Trigger provisioning of the service instance:

    $ curl -v -X POST http://localhost:8051/orchestrator/default?action=provision \
          -H 'Content-Type: text/occi' \
          -H 'Category: provision; scheme="http://schemas.mobile-cloud-networking.eu/occi/service#"' \
          -H 'X-Auth-Token: '$KID \
          -H 'X-Tenant-Name: '$TENANT

Trigger delete of SO + service instance:

    $ curl -v -X DELETE http://localhost:8051/orchestrator/default \
          -H 'X-Auth-Token: '$KID \
          -H 'X-Tenant-Name: '$TENANT
