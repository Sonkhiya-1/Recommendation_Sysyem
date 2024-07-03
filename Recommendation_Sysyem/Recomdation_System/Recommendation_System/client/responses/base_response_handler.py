class BaseResponseHandler:
    @staticmethod
    def handle_response(response):
        raise NotImplementedError("Handle response method must be implemented by subclasses.")