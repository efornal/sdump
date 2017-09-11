# sdump
Dumps administration. To manage information databases and dumps to make each of them. To this generates a configuration file which is used by a cron script to perform the dumps using the configuration specified in those files.

### Package Installation
```bash
sudo apt-get install python2.7
sudo apt-get install postgresql-9.3
sudo apt-get install python-psycopg2
sudo apt-get install python-pip

pip install -r app/requirements.txt
```

### Application configuration
```bash
cp sdump/settings.tpl.py sdump/settings.py
```

### Util commands
```bash
python manage.py migrate --database=sdump_owner

pip freeze > requirements.txt
pip install -r requirements.txt
```

### Api request format
Api requests require authentication through [Basic access authentication](https://en.wikipedia.org/wiki/Basic_access_authentication). An https connection is required.
The answers try to match the preset codes:
```bash
200 file_name

400 Bad request
401 Unauthorized
404 Not Found
500 Internal Server Error
```

##### Make dump
```bash
echo $(curl -kv https://hostname/api/make_dump?database_id=id -u username:password)

200 /dumpspath/server_base-dbname_2017-02-16-09_33.sql.gz
```
##### Check if the dump exists
```bash
echo $(curl -kv https://hostname/api/dump_exists?filename=/dumpspath/server_base-dbname_2017-02-16-09_33.sql.gz -u username:password)" 

true
```
##### Download dump
```bash
curl -kv -X GET -u usuario:password https://hostname/api/download?filename=/dumpspath/server_base-dbname_2017-02-16-09_33.sql.gz > /tmp/server_base-dbname_2017-02-16-09_33.sql.gz

```
##### Get the name of the last dump of a given database
```bash
echo $(curl -kv https://hostname/api/last_dump?database_id=id -u username:password)

200 /dumpspath/server_base-dbname_2017-02-16-09_33.sql.gz
```
##### Get id from names
The group can be omitted if multiple results are not obtained
```bash
echo $(curl -kv 'https://hostname/api/get_database_id?database=dbname&server=server&group=migroup' -u username:password)

200 database_id database_name
```

##### Creates or updates the server specified in name parameter.
If the indicated engine version does not exist, create it.
Parameters: 
    nombre, ip, puerto, motor (postgresql/mysql), description, version(9.4, 8.4,..)
responses (code, message):
    401: '401 Unauthorized'
    200: '200 server_id'           # created or updated!
    404: '404 Request not found'   # another thing


##### Creates or updates the database specified in name parameter.
If the server name or group name is not indicated it is not updated,
if they are indicated and do not exist it gives an error.
Parameters: 
   nombre,usuario,contrasenia,password_id, descripcion,
   servidor(nombre), grupo(nombre), 
responses (code, message):
    401: '401 Unauthorized'
    200: '200 database_id'           # created or updated!
    404: '404 Request not found'     # another thing


### Postgres configuration
```bash
createdb sdump_db;
createuser sdump_owner -P;

/etc/postgresql/9.3/main/pg_hba.conf
hostssl  sdump_db     sdump_owner        ::1/128                 password
/etc/init.d/postgresql restart
psql -h localhost -U sdump_owner -p 5432 -d sdump_db
```

### Change the name of the application
Requiere modificar la configuración de django

migrations.RunSQL("update django_content_type set app_label='app' \
 where app_label='dumpserver'"),

migrations.RunSQL("update django_migrations set app='app' \
 where app='dumpserver'")

