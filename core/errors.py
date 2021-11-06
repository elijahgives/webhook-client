class WebhookError(Exception):
    """Base error class for the module"""
    pass


class InvalidWebhook(WebhookError):
    """ Raised when an invalid webhook is provided for the WebhookClient instance. """
    pass