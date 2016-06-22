# sdump
backups administration

### Package Installation
```bash
sudo apt-get install python2.7
sudo apt-get install postgresql-9.3
sudo apt-get install python-psycopg2
sudo apt-get install python-pip
sudo pip install Django==1.9.7
sudo pip install django-auth-ldap==1.2.8
sudo pip install django-suit==0.2.18

```

### App configuration
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

