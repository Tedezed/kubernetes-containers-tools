# Example Module

### Files

1. `__init__.py`
```
from . import main
```


2. `__manifest__.py`
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


3. `main.py`
```
class squirrel_module():

    def __init__(self, squirrel):
        self.squirrel = squirrel
        self.squirrel_service = squirrel.squirrel_service
        self.squirrel_namespace = squirrel.squirrel_namespace
        self.squirrel_user = squirrel.squirrel_user
        self.squirrel_pass = squirrel.squirrel_pass
        self.secret_annotations = squirrel.secret_annotations
        self.random_pass = squirrel.random_pass
        self.host = squirrel.host
        self.debug_mode = squirrel.debug_mode
        test = "OK WP Example module"
        print(test)
        
    def check_app(self):
        print("check app")
        # if is OK
        return True

    def update_app(self):
        print("update app")

    def update_secret(self):
        print("update secret")
```
