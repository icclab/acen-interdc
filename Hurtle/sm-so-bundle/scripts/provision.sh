curl -v -X POST http://localhost:8051/orchestrator/default?action=provision \
-H 'Content-Type: text/occi' \
-H 'Category: provision; scheme="http://schemas.mobile-cloud-networking.eu/occi/service#"' \
-H 'X-Auth-Token: '$KID \
-H 'X-Tenant-Name: '$TENANT
