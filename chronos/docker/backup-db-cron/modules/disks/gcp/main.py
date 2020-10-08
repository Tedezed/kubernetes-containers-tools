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
