# Senior Design Lab 3

## Table of Contents
 - Dev Stuff
 - Setting Up Dev Environment
    - MySql
    - Python
    - Database

## Dev Stuff
Before you run the app, make sure you activate your virtual environment. See the set up stuff below if you haven't made your virtual envrionment yet.
```
venv\Scripts\activate.bat
```

If you added any packages, add them to *requirements.txt*. You can do this with the command:
```
pip freeze > requirements.txt
```

To make changes to the database, update the database files in python then run the following commands to commit them to the database.
```
flask db migrate -m <any message here>      # this saves your changes
flask db upgrade                            # this actually commits them to your database
```

## Setting Up Dev Environment
### MySql

Official Installation guide [here](https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/installing.html).

Quick setup
- Download the installer [here](https://dev.mysql.com/downloads/installer/). (Not the community one).
- Run the installer, select >Full to get all the products.
- Once they're done installing, click next.
- Leave the default options.
- Set a password. This is what you use to log into your server.
- Finish installing, leave everything default.

### Python

Create virtual environment.
```
python -m venv venv
```

Activate virtual environment and install packages
```
venv\Scripts\activate.bat
pip install -r requirements.txt
```

Create secrets.json file with your sql database password.
```
{
    "password": "<your_password_here>"
}
```

Finally, run *./app.py*

#### Notes

In *./app.py*, SQLALCHEMY_DATABASE_URI should be in the format: 
```
mysql+pymysql://{db_username}:{db_password}@{db_string}/{database/schema_name}
```

So, for example:
```
mysql+pymysql://root:mypass123@localhost:3306/elections
```

The default url for your local database is typically localhost:3306 unless you changed something while installing.

### Database

Now, to initilize the database run the command:

```
flask db upgrade
flask seed-data
```
