import json
import yaml
from kubernetes import client, config, watch
import os

# Source: https://github.com/karmab/samplecontroller

class controller():

    def daemon_controller(squirrel):
        print(squirrel.domain_api)
        print(squirrel.squirrel_controller)
        config.load_incluster_config()

        definition = '%s/nuts.yml' % squirrel.squirrel_controller
        print(definition)
        configuration = client.Configuration()
        configuration.assert_hostname = False
        api_client = client.api_client.ApiClient(configuration=configuration)
        v1 = client.ApiextensionsV1beta1Api(api_client)
        print(configuration)
        print(v1.list_custom_resource_definition())
        current_crds = [x['spec']['names']['kind'].lower() for x in v1.list_custom_resource_definition().to_dict()['items']]
        if 'nuts' not in current_crds:
            print("Creating nuts definition")
            with open(definition) as data:
                body = yaml.load(data)
            v1.create_custom_resource_definition(body)
        crds = client.CustomObjectsApi(api_client)

        print("Start...")
        resource_version = ''
        while True:
            stream = watch.Watch().stream(crds.list_cluster_custom_object, squirrel.domain_api, "v1", "nuts", resource_version=resource_version)
            for event in stream:
                obj = event["object"]
                operation = event['type']
                spec = obj.get("spec")
                if not spec:
                    continue
                metadata = obj.get("metadata")
                resource_version = metadata['resourceVersion']
                name = metadata['name']
                print("Handling %s on %s" % (operation, name))
                done = spec.get("review", False)
                if done:
                    continue
                #review_guitar(crds, obj)
