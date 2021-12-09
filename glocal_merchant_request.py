class GlocalMerchantRequest:
    def __init__(self, xgl_token_external, payload):
        self.xgl_token_external = xgl_token_external
        self.payload = payload

    def get_payload(self):
        return self.payload

    def get_xgl_token_external(self):
        return self.xgl_token_external

    def set_xgl_token_external(self, xgl_token_external):
        self.xgl_token_external = xgl_token_external

    def set_payload(self, payload):
        self.payload = payload
