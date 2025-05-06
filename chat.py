#!/usr/bin/env python3
import asyncio
from datetime import datetime
from typing import List, Tuple, Dict, Any
import uuid

from nicegui import ui, app, Client
from nicegui.events import KeyEventArguments

# In-memory storage for messages (for simplicity)
# Format: List[Tuple[str, str, str, str]]
messages: List[Tuple[str, str, str, str]] = []

# Store user-specific data like avatar URL per client connection
user_data: Dict[str, Dict[str, Any]] = {}

@ui.page('/')
async def main(client: Client):
    # Assign a unique ID and avatar to each connecting client
    client_id = str(uuid.uuid4())
    avatar = f'https://robohash.org/{client_id}?bgset=bg2'
    user_data[client.id] = {'client_id': client_id, 'avatar': avatar}

    # Ensure client is connected before potentially running JS
    await client.connected()

    # Function to handle key presses in the textarea
    def handle_key(e):
        """Handles Enter vs Shift+Enter."""
        if e.args.get('key') == 'Enter' and not e.args.get('shiftKey'):
            # Enter pressed without Shift: send message
            text = text_input.value.strip()
            if text:
                text_input.value = ''
                asyncio.create_task(send_message(text))
        # No 'else' needed: Shift+Enter allows default newline behavior

    # Add JavaScript function to handle message sending
    ui.run_javascript('''
        window.sendMessage = async function(text) {
            await window.nicegui_handle_event('send_message', {text: text});
        }
    ''')

    # Function to handle message sending logic
    async def send_message(text: str) -> None:
        """Sends the message, shows spinner, updates UI, and scrolls."""
        if not text:
            ui.notify('Message cannot be empty!', type='warning')
            return

        # Show spinner
        spinner.visible = True
        # Simulate network delay/processing
        await asyncio.sleep(1.0)

        # Add message to storage
        stamp = datetime.now().strftime('%X')
        messages.append((client_id, avatar, text, stamp))

        # Refresh the chat messages display for all clients
        chat_messages.refresh()

        # Hide spinner
        spinner.visible = False

        # Scroll to bottom using JavaScript (more reliable)
        # A small delay ensures the DOM has likely updated
        await asyncio.sleep(0.1)
        ui.run_javascript('''
            const chatArea = document.getElementById("chat-scroll-area");
            if (chatArea) {
                const scrollContent = chatArea.getElementsByClassName("scroll")[0];
                if (scrollContent) {
                    scrollContent.scrollTo({
                        top: scrollContent.scrollHeight,
                        behavior: 'smooth'
                    });
                }
            }
        ''')

    # Register the send_message handler
    ui.on('send_message', lambda e: send_message(e.args.get('text', '')))

    # Main UI layout
    ui.add_css(r'''
       .scroll::-webkit-scrollbar { width: 8px; }
       .scroll::-webkit-scrollbar-track { background: #f1f1f1; border-radius: 10px;}
       .scroll::-webkit-scrollbar-thumb { background: #888; border-radius: 10px;}
       .scroll::-webkit-scrollbar-thumb:hover { background: #555; }
    ''')

    # Anchor for scrolling
    ui.add_css('''
       .scroll {
             scroll-behavior: smooth;
        }
    ''')

    # Message Area (Scrollable)
    with ui.scroll_area().classes('flex-grow p-4').props('id="chat-scroll-area"'):
        # Refreshable container for chat messages
        @ui.refreshable
        def chat_messages() -> None:
            """Displays the chat messages."""
            if not messages:
                ui.label('No messages yet. Start chatting!').classes('text-center text-gray-500')
                return

            # Get the current client's ID for determining 'sent' status
            current_client_id = user_data.get(client.id, {}).get('client_id', '')

            for msg_client_id, msg_avatar, msg_text, msg_stamp in messages:
                ui.chat_message(
                    text=msg_text,
                    stamp=msg_stamp,
                    avatar=msg_avatar,
                    sent=(msg_client_id == current_client_id)
                ).classes('w-full')

        # Initial rendering of messages
        chat_messages()

    # Footer for Input
    with ui.footer().classes('bg-gray-200 p-4'):
        with ui.row().classes('w-full no-wrap items-center'):
            # User Avatar (optional)
            with ui.avatar():
                ui.image(avatar)

            # Text Input Area
            text_input = ui.textarea(placeholder='Type your message...') \
               .classes('flex-grow mx-2') \
               .props('rounded outlined dense rows=1 auto-grow') \
               .on('keydown', handle_key, throttle=0.05) # Handle keydown events
            # Add a timer function to simulate delay
            async def send_with_delay():
                spinner.visible = True
                text = text_input.value
                text_input.value = ''
                await asyncio.sleep(5)  # 5 second delay
                await send_message(text)
                spinner.visible = False

            # Send button with delayed sending
            send_button = ui.button('Send', on_click=send_with_delay) \
                .classes('bg-primary text-white') \
                .props('rounded dense')

            # Spinner (initially hidden)
            spinner = ui.spinner(type='dots', size='md', color='primary').classes('mx-2')
            spinner.visible = False

# Run the NiceGUI app
ui.run(title='NiceGUI Chat Example', storage_secret='a_secret_key_for_storage', port=8080, reload=False)