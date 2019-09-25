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

    def update_app(self):
        print("update app")
        # if is OK
        return True

    def update_secret(self):
        print("update secret")
        return True