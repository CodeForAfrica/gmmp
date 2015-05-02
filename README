# Installation

## For ubuntu

```bash
sudo apt-get install libpq-dev
sudo apt-get install libpython-dev
```

Install a postgres db if you don't already have one

```bash
sudo apt-get install postgresql postgresql-contrib
sudo /etc/init.d/postgresql start
```

Install the Heroku toolbelt for deployment, database backup, etc

```bash
wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh
```

Grab a backup of the database.

```bash
pg_dump <Database URL> > /tmp/dump # You can get the url from the Heroku config. This seems to take a long time
sudo su - postgres
createuser gmmp -W # set password to gmmp
createuser c4saadmin -W # needed to prevent error in dump file
createdb gmmp --owner gmmp
psql U gmmp <  /tmp/dump # might get an error complaining the code4saadmin doesn't exist
```

You'll need to install postgres, psycopg as your development user

```bash
git clone https://github.com/Code4SA/gmmp.git
cd gmmp
mkdir env
virtualenv env
source env/bin/activate 
pip install -r requirements.txt
```
