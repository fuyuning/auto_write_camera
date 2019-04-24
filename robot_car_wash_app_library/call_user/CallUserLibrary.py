from robot_car_wash_app_library.common import CommonLibrary


class CallUserLibrary(CommonLibrary):
    def post_car_wash_send_mobile_short_message(self, **kwargs):
        url = "{SERVER_DOMAIN}car_wash/send_mobile_short_message".format(
            SERVER_DOMAIN=self.SERVER_DOMAIN)
        data = {}
        for k, v in kwargs.items():
            if k in ("type", ):
                data[k] = v
        return self.client.post(url)

    def get_car_wash_get_virtual_mobile(self):
        url = "{SERVER_DOMAIN}car_wash/get_virtual_mobile".format(
            SERVER_DOMAIN=self.SERVER_DOMAIN)
        return self.client.get(url)

