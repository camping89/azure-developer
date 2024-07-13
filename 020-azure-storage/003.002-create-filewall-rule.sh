Create Firewall rule
Next, we have to create two firewall rules. These are the same two rules we checked as yes when we used the portal.
The first one is to allow Azure services and resources to access the server we just created.

So, this command creates a firewall rule 
named "azureaccess" for 
the SQL Server "hello-world-server" 
in the resource group "resource-group-west". 
The rule allows access from all 
IP addresses (0.0.0.0 to 0.0.0.0).

az sql server firewall-rule create \
-g rg-udacity-azure-developer \
-s sql-helloworld \
-n sql-helloworld-access \
--start-ip-address 0.0.0.0 \
--end-ip-address 0.0.0.0 \
--verbose

➜  udacity-azure-developer git:(master) ✗ az sql server firewall-rule create \
-g rg-udacity-azure-developer \
-s sql-helloworld \
-n sql-helloworld-access \
--start-ip-address 0.0.0.0 \
--end-ip-address 0.0.0.0 \
--verbose
{
  "endIpAddress": "0.0.0.0",
  "id": "/subscriptions/23e3decc-de90-484d-804a-809c69ecd709/resourceGroups/rg-udacity-azure-developer/providers/Microsoft.Sql/servers/sql-helloworld/firewallRules/sql-helloworld-access",
  "name": "sql-helloworld-access",
  "resourceGroup": "rg-udacity-azure-developer",
  "startIpAddress": "0.0.0.0",
  "type": "Microsoft.Sql/servers/firewallRules"
}
Command ran in 1.542 seconds (init: 0.094, invoke: 1.448)