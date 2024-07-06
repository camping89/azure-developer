Cleanup

If we no longer need a resource, we can delete them through the portal. The quickest way to do this from the CLI is to delete the resource group. This will delete all resources in that group

az group delete -n resource-group-west

Alternatively, if you want to just delete the App Service and App Service plan individually, you can do so with the following commands:

Delete an App Service bash az webapp delete \ --name hello-world1234 \ --resource-group resource-group-west

Delete an App Service plan bash az appservice plan delete \ --name [App Service Plan Name] \ --resource-group resource-group-west 