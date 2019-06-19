#!/usr/bin/python3

import json
import yaml
from kubernetes import client, config, watch
import os

# Source: https://github.com/karmab/samplecontroller

class controller():

    def __init__(self, squirrel):
        self.squirrel= squirrel
        config.load_incluster_config()
        self.configuration = client.Configuration()
        self.configuration.assert_hostname = False
        self.api_client = client.api_client.ApiClient(configuration=self.configuration)
        self.v1 = client.ApiextensionsV1beta1Api(self.api_client)
        print("Creating definition")
        for d in ["nuts.yml", "nutcrackers.yml"]:
            self.definition = '%s/%s' % (squirrel.squirrel_controller, d)
            with open(self.definition) as data:
                body = yaml.load(data)
            try:
                self.v1.create_custom_resource_definition(body)
            except Exception as e:
                print("Ignoring error: %s" % e)
        self.crds = client.CustomObjectsApi(self.api_client)

    def daemon_controller(self):
        print("Start...")
        self.resource_version = ''
        while True:
            self.streams("nuts")
            self.streams("nutcrackers")

    def streams(self, kind):
        stream = watch.Watch().stream(self.crds.list_cluster_custom_object, \
            self.squirrel.domain_api, self.squirrel.api_version, kind, resource_version=self.resource_version)
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
