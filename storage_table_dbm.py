import string,random,time,azurerm,json
from azure.storage.table import TableService, Entity

# Define variables to handle Azure authentication
auth_token = azurerm.get_access_token_from_cli()
subscription_id = azurerm.get_subscription_from_cli()

# Define variables with random resource group and storage account names
resourcegroup_name = 'dbm'+''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
storageaccount_name = 'dbm'+''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
location = 'eastus'

###
# Create the a resource group for our demo
# We need a resource group and a storage account. A random name is generated, as each storage account name must be globally unique.
###
response = azurerm.create_resource_group(auth_token, subscription_id, resourcegroup_name, location)
if response.status_code == 200 or response.status_code == 201:
    print('Resource group: ' + resourcegroup_name + ' created successfully.')
else:
    print('Error creating resource group')

# Create a storage account for our demo
response = azurerm.create_storage_account(auth_token, subscription_id, resourcegroup_name, storageaccount_name,  location, storage_type='Standard_LRS')
if response.status_code == 202:
    print('Storage account: ' + storageaccount_name + ' created successfully.')
    time.sleep(2)
else:
    print('Error creating storage account')


###
# Use the Azure Storage Storage SDK for Python to create a Table
###

response = azurerm.get_storage_account_keys(auth_token, subscription_id, resourcegroup_name, storageaccount_name)
storageaccount_keys = json.loads(response.text)
storageaccount_primarykey = storageaccount_keys['keys'][0]['value']

# Create the Table with the Azure Storage SDK and the access key obtained in the previous step
table_service = TableService(account_name=storageaccount_name, account_key=storageaccount_primarykey)
response = table_service.create_table('itemstable')
if response == True:
    print('Storage Table: itemstable created successfully.\n')
else:
    print('Error creating Storage Table.\n')

time.sleep(1)


###
# Cars
###

car = Entity()
car.PartitionKey = 'carinventory'
car.RowKey = '001'
car.make   = 'Chrysler'
car.model  = 'Sebring'
car.year   = '2006'
car.color  = 'Burgendy'
car.price  = 6000
table_service.insert_entity('itemstable', car)
print('Created entry for Sebring...')

car = Entity()
car.PartitionKey = 'carinventory'
car.RowKey = '002'
car.make   = 'Triumph'
car.model  = 'TR8'
car.year   = '1980'
car.color  = 'Silver'
car.price  = 10000
table_service.insert_entity('itemstable', car)
print('Created entry for TR8...')

car = Entity()
car.PartitionKey = 'carinventory'
car.RowKey = '003'
car.make   = 'Chevrolet'
car.model  = 'Astro'
car.year   = '191989'
car.color  = 'Silver'
car.price  = 1000
table_service.insert_entity('itemstable', car)
print('Created entry for Astro...\n')

# Coffee store

coffee = Entity()
coffee.PartitionKey = 'coffeestore'
coffee.RowKey 		= '005'
coffee.brand 		= 'folgers'
coffee.flavor 		= 'original'
coffee.size 		= 'small'
coffee.price 		= 1.25
table_service.insert_entity('itemstable', coffee)
print('Created entry for small folgers...\n')
time.sleep(1)

coffee = Entity()
coffee.PartitionKey = 'coffeestore'
coffee.RowKey 		= '006'
coffee.brand 		= 'folgers'
coffee.flavor 		= 'original'
coffee.size 		= 'medium'
coffee.price 		= 1.75
table_service.insert_entity('itemstable', coffee)
print('Created entry for medium folgers...\n')
time.sleep(1)


coffee = Entity()
coffee.PartitionKey = 'coffeestore'
coffee.RowKey 		= '007'
coffee.brand 		= 'folgers'
coffee.flavor 		= 'original'
coffee.size 		= 'large'
coffee.price 		= 2.50
table_service.insert_entity('itemstable', coffee)
print('Created entry for large folgers...\n')
time.sleep(1)

