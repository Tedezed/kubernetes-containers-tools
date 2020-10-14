    def date_drop_snapshot(self, now_datetime):
        drop_datetime = now_datetime - timedelta(days=int(self.dic_argv["subtract_days"]))
        print "[INFO] Checking snapshot that are on or out the erase date: %s" % drop_datetime
        list_snapshot = self.gtools.list_snapshot(self.dic_argv["project"])
        if list_snapshot != None:
            for s in list_snapshot:
                file_date = ""
                try:
                    if "---" in s["name"]:
                        name_split = s["name"].split("---")
                        name_date = name_split[1]
                        if datetime.strptime(name_date, "%Y-%m-%d").strftime("%Y-%m-%d") <= drop_datetime.strftime("%Y-%m-%d"):
                            logging.warning("[INFO] [%s] Drop snapshot %s" % (now_datetime, s["name"]))
                            print("[INFO] [%s] Drop snapshot %s" % (now_datetime, s["name"]))
                            self.gtools.delete_snapshot(self.dic_argv["project"],s["name"])
                except Exception as e:
                    key = False
                    print(e)
                    logging.error(e)
        else:
            print("[INFO] Not found snapshot that are on or out the erase date: %s" % drop_datetime)

    def snapshot_op(self, list_disk):
        now_datetime = datetime.now()
        for disk in list_disk:
            if len(disk["name_disk"]) > 45:
                name_snapshot = disk["name_disk"][0:45] + "---" + now_datetime.strftime("%Y-%m-%d")
            else:
                name_snapshot = disk["name_disk"] + "---" + now_datetime.strftime("%Y-%m-%d")

            logging.warning("[INFO] [%s] Create snapshot %s" % (now_datetime, name_snapshot))
            print("[INFO] [%s] Create snapshot %s" % (now_datetime, name_snapshot))
            try:
                self.gtools.disk_to_snapshot(self.dic_argv["project"], disk["zone"], disk["name_disk"], name_snapshot)
            except Exception as e:
                print(e)
                logging.error(e)
        self.date_drop_snapshot(now_datetime)

    def snapshot_filter_label(self):
        self.gtools = gcloud_tools()
        list_disk_gcp = self.gtools.list_disks(self.dic_argv["project"], self.dic_argv["zone"])

        list_disk = []
        for disk in list_disk_gcp:
            disk_labels = disk.get("labels", [])
            disk_label_backup = "false"
            for l in disk_labels:
                if l == "backup":
                    disk_label_backup = disk_labels[l]
            if disk["status"] == "READY" and disk_label_backup.lower() ==  "true":
                dict_disk = {"name_disk": disk["name"], "zone": self.dic_argv["zone"]}
                list_disk.append(dict_disk)

        if list_disk:
            self.snapshot_op(list_disk)
