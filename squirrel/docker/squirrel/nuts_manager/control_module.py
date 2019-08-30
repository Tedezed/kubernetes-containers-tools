import psycopg2, base64, sys, os, ast, importlib
from passlib.hash import pbkdf2_sha512

class app_update_pass():

    def __init__(self,
                squirrel_service,
                squirrel_namespace,
                squirrel_user,
                squirrel_pass,
                squirrel_type_frontend,
                squirrel_type_backend,
                secret_annotations,
                mode,
                random_pass,
                squirrel_nuts_manager,
                debug):

        app_pass_version="v0.1"
        self.squirrel_mode = mode
        self.squirrel_service = squirrel_service
        self.squirrel_namespace = squirrel_namespace
        self.squirrel_user = base64.b64decode(\
            squirrel_user + '=' * (-len(squirrel_user) % 4)).decode()
        self.squirrel_pass = base64.b64decode(\
            squirrel_pass + '=' * (-len(squirrel_pass) % 4)).decode()
        self.squirrel_type_frontend = squirrel_type_frontend
        self.squirrel_type_backend = squirrel_type_backend
        self.secret_annotations = secret_annotations
        self.random_pass = random_pass
        self.host = "%s.%s.svc.cluster.local" % \
          (squirrel_service, squirrel_namespace)
        self.squirrel_nuts_manager = squirrel_nuts_manager
        self.debug_mode = debug

        # Get list of modules
        self.manifestname = '__manifest__.py'
        self.name_dir_modules = "modules"
        self.path_modules = "%s/%s" % (squirrel_nuts_manager ,self.name_dir_modules)
        self.relative_path_modules = "nuts_manager/%s" % (self.name_dir_modules)
        if os.path.isdir(self.path_modules):
            self.modules = []
            obj_modules = os.walk(self.path_modules)
            for mod in obj_modules:
                if mod[0] == self.path_modules:
                    print("[INFO] Load Modules..")
                    self.modules = mod[1]
                    print("[INFO] Load: %s" % self.modules)
        else:
            raise Exception("[ERROR] Dir modules not found: %s "% self.path_modules)

    def load_manifest(self, mod):
        manifest_file = "%s/%s/%s" % (self.path_modules, mod, self.manifestname)
        if os.path.isfile(manifest_file):
            m = open(manifest_file,"rb")
            try:
                manifestmod = ast.literal_eval(m.read().decode('utf-8'))
            finally:
                m.close()
            return manifestmod
        else:
            return False
                
    def load_module(self, mod):
        mod_to_load = '%s.%s' % (self.relative_path_modules.replace("/", "."), mod)
        #mod_to_load = '%s.%s' % (self.path_modules[1:].replace("/", "."), mod)
        importmod = importlib.import_module(mod_to_load)
        return importmod.main.squirrel_module(self)

    def conditional_app(self):
        for mod in self.modules:
            # Load Manifest
            manifestmod = self.load_manifest(mod)
            if manifestmod:
                if manifestmod["executable"]:
                    print("[INFO] Module '%s' is executable" % manifestmod["name"])
                    if self.squirrel_type_frontend == manifestmod["frontend"] \
                      and self.squirrel_type_backend == manifestmod["backend"]:
                        print("[INFO] Execute module '%s' for " % (manifestmod["name"]))
                        # Load Module
                        sm = self.load_module(mod)
                        if sm:
                            if self.squirrel_mode == "update_app_password" \
                              and manifestmod["update_app_password"]:
                                sm.update_app()
                            if self.squirrel_mode == "update_secret" \
                              and manifestmod["update_secret"]:
                                sm.update_secret()
                        else:
                            print("[ERROR] Impossible to load the module: %s" % manifestmod["name"])
            manifestmod = False