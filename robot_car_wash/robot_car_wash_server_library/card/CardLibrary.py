from robot_car_wash.robot_car_wash_server_library.common import CommonLibraryclass CardLibrary(CommonLibrary):    def post_card_by_(self, **kwargs):        url = "{SERVER_DOMAIN}/admin/cards".format(            SERVER_DOMAIN=self.SERVER_DOMAIN)        data = {}        for k, v in kwargs.items():            if k in ("card_name", "days", "grant_way", "price", "first_price", "recharge_price", "first_recharge_price", "auto_recharge", "coupons", "card_remark"):                data[k] = v        return self.client.post(url, json=data)    def put_card_by_card_id(self, card_id, **kwargs):        url = "{SERVER_DOMAIN}/admin/cards/{card_id}".format(            SERVER_DOMAIN=self.SERVER_DOMAIN, card_id=card_id)        data = {}        for k, v in kwargs.items():            if k in ("card_name", "days", "grant_way", "price", "first_price", "recharge_price", "first_recharge_price", "auto_recharge", "coupons", "card_remark"):                data[k] = v        return self.client.put(url, json=data)    def get_card_by_(self, **kwargs):        url = "{SERVER_DOMAIN}/admin/cards".format(            SERVER_DOMAIN=self.SERVER_DOMAIN)        data = {}        for k, v in kwargs.items():            if k in ("card_id", "page_num", "page_size"):                data[k] = v        return self.client.get(url, params=data)    def delete_card_by_card_id(self, card_id):        url = "{SERVER_DOMAIN}/admin/cards/{card_id}".format(            SERVER_DOMAIN=self.SERVER_DOMAIN, card_id=card_id)        return self.client.delete(url)