from nicegui import ui
import asyncio # Import asyncio

# List to store chat messages
messages = []

# Define the main page using the @ui.page decorator
@ui.page('/')
def main_page():

    # Function to handle key presses
    def handle_key(e):
        if e.args.get('key') == 'Enter' and not e.args.get('shiftKey'):
            text = message_input.value.strip()
            if text:
                message_input.value = ''
                asyncio.create_task(send_message())

    # Create a refreshable component to display messages
    @ui.refreshable
    def display_messages():
        # Container for messages with scrolling capability
        # The card itself needs an ID or a class to target it reliably with JS
        # Ensure the card height is fixed and overflow is set
        with ui.card().classes('w-full h-64 overflow-auto my-chat-card').style('background-color: grey; border: 20px solid green; border-radius: 0;') as chat_card:
            if messages:
                # Use a column to stack messages vertically within the card
                # This helps ensure the scrollHeight is calculated correctly
                with ui.column().classes('w-full'):
                    for message in messages:
                        # Ensure messages are displayed as simple text labels
                        # Added word-break to handle long words
                        ui.label(message).style('font-size: 12px; padding: 8px; margin: 4px; background-color: white; border-radius: 4px; word-break: break-word;')
            else:
                # Added text-center class for centering
                ui.label('No messages yet').classes('text-center').style('font-size: 12px; color: white; margin: 20px;')
            return chat_card

    # Main layout within the defined page
    with ui.column().classes('w-full max-w-3xl mx-auto'):
        # Title
        ui.label('Chat Box').classes('text-2xl font-bold my-4')

        # Display messages area (top text area)
        chat_card = display_messages()

        # Define send_message BEFORE using it
        async def send_message():
            if message_input.value:
                # Add message to the list
                messages.append(message_input.value)

                # Clear input AFTER getting value
                message_input.value = ''

                # Refresh the messages display on the page
                chat_card = display_messages.refresh()

                # Add a small delay to allow the browser's DOM to update
                await asyncio.sleep(0.01)

                # Scroll to bottom using ui.scroll_to
                await ui.run_javascript(f'document.querySelector(".my-chat-card").scrollTo(0, document.querySelector(".my-chat-card").scrollHeight)')

        # Input area (bottom)
        with ui.row().classes('w-full mt-4'):
            # Set width hint to ensure flex-grow works predictably
            message_input = ui.input(placeholder='Type your message...').props('outlined').classes('flex-grow').style('width: calc(100% - 80px);')
            ui.button('Send', on_click=send_message).props('color=primary')

        # Also send message when pressing Enter key in the input field
        message_input.on('keydown.enter', send_message)

if __name__ in {"__main__", "__mp_main__"}:
    # ui.run starts the NiceGUI server
    # storage_secret is needed if you use ui.storage
    ui.run(title='NiceGUI Chat Example', storage_secret='a_secret_key_for_storage', port=8080, reload=False)
