from channels.routing import ProtocolTypeRouter
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url

from .consumers import CustomConsumer

application = ProtocolTypeRouter({
    # 'websocket': AllowedHostsOriginValidator(
    #     AuthMiddlewareStack(
    #         URLRouter(
    #             [
    #                 url("articles/", CustomConsumer()),
    #             ]
    #         )
    #     )
    # )
})

channel_routing = {
}
