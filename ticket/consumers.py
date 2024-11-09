import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TicketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'ticket_updates'
        self.room_group_name = f'ticket_{self.room_name}'

        # Join the group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'ticket_activity',
                'message': message
            }
        )

    # Receive message from group
    async def ticket_activity(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
