import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
