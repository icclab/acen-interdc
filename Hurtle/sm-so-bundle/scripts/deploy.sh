curl -v -X POST http://localhost:8051/orchestrator/default?action=deploy \
-H 'Content-Type: text/occi' \
-H 'Category: deploy; scheme="http://schemas.mobile-cloud-networking.eu/occi/service#"' \
-H 'X-Auth-Token: '$KID \
-H 'X-Tenant-Name: '$TENANT
