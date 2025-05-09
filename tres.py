#
# there are a set of elements to consider to create a chat function
# 
# Graphic elements:
# 1. a scroll area to display messages
# 2. a text input to type messages
#    handle key presses
#    respond to click send button
# 3. a send button to send messages
# 4. a spinner to show that the message is being sent
#
# Function elements
# 1. a function to send messages to the server
# 2. a function to display messages from the server and from the client
# 3. a function to handle key presses
# 4. a function to respond to click send button
#
# Storage elements
# 1. a list to store messages
# 2. database to store messages
# 3. a list to store the user's name, avatar, and session id
#
#
#

from nicegui import ui
import asyncio
from database import DatabaseManager

messages = []
user_info = {'name': None, 'avatar': None, 'session_id': 0, 'user_id': 0}


# Now you can use the DatabaseManager
with DatabaseManager("my_database.db") as db:
    # Create a table
    db.create_table("users", [
        "id INTEGER PRIMARY KEY",
        "name TEXT NOT NULL",
        "email TEXT UNIQUE"
    ])
    
    # Add a user
    # user_id = db.insert("users", {
    #     "name": "John Doe",
    #     "email": "john@example.com"
    # })

    db.create_table("messages", [
        "id INTEGER PRIMARY KEY",
        "message TEXT NOT NULL",
        "user_id INTEGER NOT NULL",
        "session_id INTEGER NOT NULL",
        "timestamp DATETIME DEFAULT CURRENT_TIMESTAMP"
    ])


@ui.page('/')
def main_page():
    def send_message_1():
        print('send_message_1')

    ui.label('Pagina tres').classes('text-2xl font-bold my-4')
    spinner = ui.spinner('dots', size='lg').classes('text-primary absolute bottom-4 left-1/2 transform -translate-x-1/2 z-50')
    spinner.visible = False
    button_flag = ui.button('Send', on_click=send_message_1).props('color=primary').classes('text-primary absolute bottom-12 left-1/2 transform -translate-x-1/2 z-50')
    button_flag.visible = False

    # insert an empty message to be ready to receive messages
    db.insert("messages", {
        "message": "",
        "user_id": 0,
        "session_id": 0
    })

    # Create a scroll area for messages
    scroll = ui.scroll_area().classes('w-full h-64 my-chat-card').style('background-color: white; border: 20px solid green; border-radius: 0;')

    async def request_message():
        #await asyncio.sleep(0.01)
        messages.append('REQUEST: Message from server')
        ui.notify('Request issued')

    async def save_message_db():
        await asyncio.sleep(0.01)
        messages_str = '\n'.join(messages)  # Convert list to string
        rows = db.update("messages", {
            "message": messages_str,
            "user_id": user_info['user_id'],
            "session_id": user_info['session_id']   
        }, "user_id = ? AND session_id = ?", params=(user_info['user_id'], user_info['session_id']))
        messages.append('SAVE_MESSAGE_DB: Message from server')
        print("Number of rows updated: ", rows)
        #ui.notify('Message saved')


    def display_messages():
        spinner.visible = not spinner.visible
        #send_button.visible = not send_button.visible
        button_flag.visible = not button_flag.visible

        asyncio.create_task(save_message_db())
        scroll.clear()
        with scroll:
            if messages:
                with ui.column().classes('w-full'):
                    for message in messages:
                        ui.label(message).style('font-size: 12px; padding: 8px; margin: 4px; background-color: white; border-radius: 4px; word-break: break-word;')
            else:
                ui.label('No messages yet').classes('text-center').style('font-size: 12px; color: white; margin: 20px;')

    def send_message():
        if message_input.value:
            messages.append(message_input.value)
            message_input.value = ''
            display_messages()
            #await asyncio.sleep(0.01)
            #await request_message()
            scroll.scroll_to(percent=1e6)

    with ui.column().classes('w-full max-w-3xl mx-auto'):
        ui.label('Chat Box').classes('text-2xl font-bold my-4')
        display_messages()

        def handle_key(e):
            if e.args.get('key') == 'Enter':
                if e.args.get('shiftKey'):
                    return
                if message_input.value.strip():
                    send_message()
                    # e.prevent_default()

        with ui.row().classes('w-full mt-4'):
            message_input = ui.input(placeholder='Type your message...') \
                .props('outlined type=textarea rows=3') \
                .classes('flex-grow') \
                .style('width: calc(100% - 80px); min-height: 80px; resize: vertical;')
            send_button = ui.button('Send', on_click=send_message).props('color=primary')
            message_input.on('keydown', handle_key)


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title='NiceGUI Chat Example', storage_secret='a_secret_key_for_storage', port=8080, reload=False)