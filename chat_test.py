#!/usr/bin/env python3
import asyncio
from datetime import datetime
from typing import List, Tuple, Dict, Any
import uuid

from nicegui import ui, app, Client
from nicegui.events import KeyEventArguments

# In-memory storage for messages
messages: List[Tuple[str, str, str, str]] = []
spinner_sw = None

# Store user-specific data
user_data: Dict[str, Dict[str, Any]] = {}

@ui.page('/chat_test')
async def main(client: Client):
    # Assign unique ID and avatar to each client
    client_id = str(uuid.uuid4())
    avatar = f'https://robohash.org/{client_id}?bgset=bg2'
    user_data[client.id] = {'client_id': client_id, 'avatar': avatar}

    # Ensure client is connected
    await client.connected()



    # Function to handle key presses
    def handle_key(e):
        if e.args.get('key') == 'Enter' and not e.args.get('shiftKey'):
            text = text_input.value.strip()
            if text:
                text_input.value = ''
                asyncio.create_task(send_message(text))

    # Function to send message
    async def send_message(text: str) -> None:
        print(f"Sending message: {text}")
        if not text:
            return

        # Show spinner
        spinner_sw.visible = True
        print( "spinner_sw.visible", spinner_sw.visible)

        # Add message to storage
        stamp = datetime.now().strftime('%X')
        messages.append((client_id, avatar, text, stamp))

        # Refresh chat messages
        chat_messages.refresh()

        # Hide spinner
        spinner_sw.visible = False

        # Add CSS for scrolling
        ui.add_css('''
            .scroll::-webkit-scrollbar { width: 8px; }
            .scroll::-webkit-scrollbar-track { background: #f1f1f1; border-radius: 10px;}
            .scroll::-webkit-scrollbar-thumb { background: #888; border-radius: 10px;}
            .scroll::-webkit-scrollbar-thumb:hover { background: #555; }
            .scroll { scroll-behavior: smooth; }
        ''')

    # Main UI layout
    # Header
    with ui.header().classes('bg-blue-500 text-white p-4'):
        ui.label('Chat Room').classes('text-xl font-bold')

    with ui.scroll_area().classes('flex-grow p-4 border-2 border-black overflow-auto').props('id="frame"'):
        ui.label('Hello').classes('text-2xl')
        ui.input(placeholder='Enter text here').classes('w-full mt-2')

    with ui.column().classes('flex flex-col items-center justify-center flex-grow h-full'):
        ui.label('Loading...').classes('text-2xl')
        xx = ui.spinner(size='50px')

    # Message Area (Scrollable)
    with ui.scroll_area().classes('flex-grow p-10 border-2 border-red-500 color=blue overflow-auto').props('id="chat-scroll-area"'):
        # Refreshable container for chat messages
        @ui.refreshable
        def chat_messages() -> None:
            if not messages:
                ui.label('No messages yet. Start chatting!').classes('text-center text-gray-900')
                return

            current_client_id = user_data.get(client.id, {}).get('client_id', '')

            for msg_client_id, msg_avatar, msg_text, msg_stamp in messages:
                ui.chat_message(
                    text=msg_text,
                    stamp=msg_stamp,
                    avatar=msg_avatar,
                    sent=(msg_client_id == current_client_id)
                ).classes('w-full bg-gray-100 border-20 border-black rounded-lg p-2 mb-2 overflow-auto animate-slide-up')
    # Initial rendering of messages
    chat_messages()

    # Footer for Input
    with ui.footer().classes('bg-gray-100 p-4 border-t'):
        #with ui.row().classes('w-full no-wrap items-center'):
        #    ui.spinner(size='50px')

        with ui.row().classes('w-full no-wrap items-center'):
            spinner_sw = ui.spinner(size='50px')
            spinner_sw.visible = True
            #spinner = ui.spinner(type='dots', size='md', color='primary').classes('mx-2')

            with ui.avatar():
                ui.image(avatar)

            # Text Input Area
            text_input = ui.textarea(placeholder='Type your message...') \
                .classes('flex-grow mx-2') \
                .props('rounded outlined dense rows=1 auto-grow') \
                .on('keydown', handle_key)

            # Send button
            def on_send_click():
                text = text_input.value.strip()
                if text:
                    text_input.value = ''
                    asyncio.create_task(send_message(text))

            send_button = ui.button('Send', on_click=on_send_click) \
                .classes('bg-blue-500 text-white') \
                .props('rounded dense')


# Run the NiceGUI app
ui.run(title='NiceGUI Chat Example', storage_secret='a_secret_key_for_storage', port=8080, reload=False)
