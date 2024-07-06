Steps to Create and Deploy an App Service Web App from a Directory using Azure CLI:

Sign in to Azure az login
cd to web directory
Run the following command:

az webapp up \
--resource-group resource-group-west \
--name hello-world1234 \
--sku F1 \
--verbose

If you visit the URL, you should see your site deployed.
If you want to update your app, make changes to your code, and then run (Note: this may not update new requirements you may have added):

az webapp up \
--name hello-world1234 \
--verbose