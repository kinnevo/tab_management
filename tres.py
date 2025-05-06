from nicegui import ui
import asyncio

messages = []

@ui.page('/')
def main_page():
    ui.label('Pagina tres').classes('text-2xl font-bold my-4')

    # Create a scroll area for messages
    scroll = ui.scroll_area().classes('w-full h-64 my-chat-card').style('background-color: white; border: 20px solid green; border-radius: 0;')

    def display_messages():
        scroll.clear()
        with scroll:
            if messages:
                with ui.column().classes('w-full'):
                    for message in messages:
                        ui.label(message).style('font-size: 12px; padding: 8px; margin: 4px; background-color: white; border-radius: 4px; word-break: break-word;')
            else:
                ui.label('No messages yet').classes('text-center').style('font-size: 12px; color: white; margin: 20px;')

    async def send_message():
        if message_input.value:
            messages.append(message_input.value)
            message_input.value = ''
            display_messages()
            await asyncio.sleep(0.01)
            scroll.scroll_to(percent=1e6)

    with ui.column().classes('w-full max-w-3xl mx-auto'):
        ui.label('Chat Box').classes('text-2xl font-bold my-4')
        display_messages()

        def handle_key(e):
            if e.args.get('key') == 'Enter':
                if e.args.get('shiftKey'):
                    return
                if message_input.value.strip():
                    asyncio.create_task(send_message())
                    # e.prevent_default()

        with ui.row().classes('w-full mt-4'):
            message_input = ui.input(placeholder='Type your message...') \
                .props('outlined type=textarea rows=3') \
                .classes('flex-grow') \
                .style('width: calc(100% - 80px); min-height: 80px; resize: vertical;')
            ui.button('Send', on_click=send_message).props('color=primary')
            message_input.on('keydown', handle_key)

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title='NiceGUI Chat Example', storage_secret='a_secret_key_for_storage', port=8080, reload=False)