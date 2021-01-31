#Installing postgres
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get -y install postgresql-12 postgresql-contrib-12
sudo apt-get -y install binutils libproj-dev gdal-bin   #Postgis extension
sudo apt-get -y install postgis postgresql-12-postgis-3-scripts

sed -i '1s/^/local globechaintest globechaintest md5\n/' /etc/postgresql/12/main/pg_hba.conf

sudo systemctl start postgresql.service

sudo -u postgres psql -c "CREATE USER globechaintest WITH PASSWORD 'globechaintest';"
sudo -u postgres psql -c "CREATE DATABASE globechaintest";

sudo systemctl restart postgresql.service

apt-get install -y python3-pip
pip3 install -r requirements.txt

sudo -u postgres psql -c "ALTER ROLE globechaintest superuser;"

python3 manage.py migrate

sudo -u postgres psql -c "ALTER ROLE globechaintest nosuperuser;"

python3 manage.py runserver