#!/usr/bin/python
# -*- coding: utf-8 -*-

import googleapiclient.discovery, os
from googleapiclient import _auth
from google.oauth2 import service_account

class gcloud_tools:

    def __init__(self):
        # If credentials is None use Default credentials --> gcloud auth list
        if os.getenv("GCLOUD_DEFAULT_CREDENTIALS") != "False":
            print("Default credential: %s" % _auth.default_credentials().__dict__)
            self.compute = googleapiclient.discovery.build('compute', 'v1', credentials=None)
        else:
            credentials = service_account.Credentials.from_service_account_file(os.getenv("GCLOUD_SA_FILE"))
            print("Default credential: %s" % credentials.__dict__)
            self.compute = googleapiclient.discovery.build('compute', 'v1', credentials=credentials)

    def list_instances(self, project, zone):
        result = self.compute.instances().list(project=project, zone=zone).execute()
        return result.get('items', None)

    def list_disks(self, project, zone):
        result = self.compute.disks().list(project=project, zone=zone).execute()
        return result.get('items', None)

    def list_snapshot(self, project):
        result = self.compute.snapshots().list(project=project).execute()
        return result.get('items', None)

    def disk_to_snapshot(self, project, zone, disk_name, snapshot_name):
        body = {"name": snapshot_name, "storageLocations": [zone[:-2]]}
        return self.compute.disks().createSnapshot(project=project, zone=zone,
                                              disk=disk_name, body=body).execute()

    def delete_snapshot(self, project, name):
        return self.compute.snapshots().delete(project=project, snapshot=name).execute()