from robot_car_wash_app_library.common import CommonLibrary


class WashRecordLibrary(CommonLibrary):
    def post_update_by_wash_record_id(self, wash_record_id, **kwargs):
        url = "{SERVER_DOMAIN}/car_wash/wash_records/{wash_record_id}/update".format(
            SERVER_DOMAIN=self.SERVER_DOMAIN, wash_record_id=wash_record_id)
        data = {}
        for k, v in kwargs.items():
            if k in ("status", "before_wash_images", "after_wash_images", "wash_tags", "description", "start_time", "end_time", "dirty_percent", "washer_remark", "mark"):
                data[k] = v
        return self.client.post(url, json=data)

    def post_upload_mark_by_wash_record_id(self, wash_record_id, **kwargs):
        url = "{SERVER_DOMAIN}/car_wash/wash_records/{wash_record_id}/upload_mark".format(
            SERVER_DOMAIN=self.SERVER_DOMAIN, wash_record_id=wash_record_id)
        data = {}
        for k, v in kwargs.items():
            if k in ("washer_remark", "mark"):
                data[k] = v
        return self.client.post(url, json=data)

    def post_upload_by_wash_record_id(self, wash_record_id, **kwargs):
        url = "{SERVER_DOMAIN}/car_wash/wash_records/{wash_record_id}/upload".format(
            SERVER_DOMAIN=self.SERVER_DOMAIN, wash_record_id=wash_record_id)
        data = {}
        for k, v in kwargs.items():
            if k in ("before_wash_images", "tags", "status", "description", "after_wash_images", "start_time", "end_time", "dirty_percent"):
                data[k] = v
        return self.client.post(url, json=data)

    def post_wash_by_wash_record_id(self, wash_record_id, **kwargs):
        url = "{SERVER_DOMAIN}/car_wash/wash_records/{wash_record_id}/wash".format(
            SERVER_DOMAIN=self.SERVER_DOMAIN, wash_record_id=wash_record_id)
        data = {}
        for k, v in kwargs.items():
            if k in ("before_wash_images", "tags", "description"):
                data[k] = v
        return self.client.post(url, json=data)

    def post_finish_by_wash_record_id(self, wash_record_id, **kwargs):
        url = "{SERVER_DOMAIN}/car_wash/wash_records/{wash_record_id}/finish".format(
            SERVER_DOMAIN=self.SERVER_DOMAIN, wash_record_id=wash_record_id)
        data = {}
        for k, v in kwargs.items():
            if k in ("after_wash_images", ):
                data[k] = v
        return self.client.post(url)

    def get_user_wash_records(self, **kwargs):
        url = "{SERVER_DOMAIN}/car_wash/user/wash_records".format(
            SERVER_DOMAIN=self.SERVER_DOMAIN)
        data = {}
        for k, v in kwargs.items():
            if k in ("section", "page_limit"):
                data[k] = v
        return self.client.get(url, params=data)

    def get_cars_in_parking(self, **kwargs):
        url = "{SERVER_DOMAIN}/car_wash/cars/in_parking".format(
            SERVER_DOMAIN=self.SERVER_DOMAIN)
        data = {}
        for k, v in kwargs.items():
            if k in ("parking_id", "car_ids"):
                data[k] = v
        return self.client.get(url, params=data)

    def get_wash_records_group_by_zone(self, **kwargs):
        url = "{SERVER_DOMAIN}/car_wash/wash_records/group_by_zone".format(
            SERVER_DOMAIN=self.SERVER_DOMAIN)
        data = {}
        for k, v in kwargs.items():
            if k in ("status", "parking_id", "wash_area_id"):
                data[k] = v
        return self.client.get(url, params=data)

    def get_wash_records_nearby(self, **kwargs):
        url = "{SERVER_DOMAIN}/car_wash/wash_records/nearby".format(
            SERVER_DOMAIN=self.SERVER_DOMAIN)
        data = {}
        for k, v in kwargs.items():
            if k in ("radius", "center", "status", "limit", "wash_area_id"):
                data[k] = v
        return self.client.get(url, params=data)

    def get_car_wash_wash_records(self, **kwargs):
        url = "{SERVER_DOMAIN}/car_wash/wash_records".format(
            SERVER_DOMAIN=self.SERVER_DOMAIN)
        data = {}
        for k, v in kwargs.items():
            if k in ("status", "car_id", "wash_group_id", "section", "page_limit", "wash_area_id", "order_by", "floor", "zone"):
                data[k] = v
        return self.client.get(url, params=data)

    def get_car_wash_wash_records_by_wash_record_id(self, wash_record_id):
        url = "{SERVER_DOMAIN}/car_wash/wash_records/{wash_record_id}".format(
            SERVER_DOMAIN=self.SERVER_DOMAIN, wash_record_id=wash_record_id)
        return self.client.get(url)

    def get_car_in_parking(self, **kwargs):
        url = "{SERVER_DOMAIN}/car_wash/car/in_parking".format(
            SERVER_DOMAIN=self.SERVER_DOMAIN)
        data = {}
        for k, v in kwargs.items():
            if k in ("parking_id", "car_id"):
                data[k] = v
        return self.client.get(url, params=data)

    def patch_washer_remark_by_wash_record_id(self, wash_record_id, **kwargs):
        url = "{SERVER_DOMAIN}/car_wash/wash_records/{wash_record_id}/washer_remark".format(
            SERVER_DOMAIN=self.SERVER_DOMAIN, wash_record_id=wash_record_id)
        data = {}
        for k, v in kwargs.items():
            if k in ("washer_remark", ):
                data[k] = v
        return self.client.patch(url)

    def patch_mark_by_wash_record_id(self, wash_record_id, **kwargs):
        url = "{SERVER_DOMAIN}/car_wash/wash_records/{wash_record_id}/mark".format(
            SERVER_DOMAIN=self.SERVER_DOMAIN, wash_record_id=wash_record_id)
        data = {}
        for k, v in kwargs.items():
            if k in ("mark", ):
                data[k] = v
        return self.client.patch(url)

    def patch_status_by_wash_record_id(self, wash_record_id, **kwargs):
        url = "{SERVER_DOMAIN}/car_wash/wash_records/{wash_record_id}/status".format(
            SERVER_DOMAIN=self.SERVER_DOMAIN, wash_record_id=wash_record_id)
        data = {}
        for k, v in kwargs.items():
            if k in ("status", ):
                data[k] = v
        return self.client.patch(url)

