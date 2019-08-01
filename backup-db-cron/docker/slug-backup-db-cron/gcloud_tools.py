#!/usr/bin/python
# -*- coding: utf-8 -*-

import googleapiclient.discovery

class gcloud_tools:

    def __init__(self):
        self.compute = googleapiclient.discovery.build('compute', 'v1')

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
        body = {"name": snapshot_name}
        return self.compute.disks().createSnapshot(project=project, zone=zone,
                                              disk=disk_name, body=body).execute()

    def delete_snapshot(self, project, name):
        return self.compute.snapshots().delete(project=project, snapshot=name).execute()