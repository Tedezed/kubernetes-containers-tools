# Example Module

### Files

`__init__.py`
```
from . import main
```


`__manifest__.py`
```
{
"name": "Module Example Wordpess Mysql",
"author": "You",
"version": "0.1",
"frontend": "wordpress",
"backend": "mysql",
"update_app_password": True,
"update_secret": True,
"executable": False,
}
```


`main.py`
```
class squirrel_module():

    def __init__(self):
        test = "OK WP Example module"
        print(test)

    def update_app(self):
        print("update app")

    def update_secret(self):
        print("update secret")
```
