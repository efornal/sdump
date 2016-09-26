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
python manage.py migrate

pip freeze > requirements.txt
pip install -r requirements.txt
```

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

