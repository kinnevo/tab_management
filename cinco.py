#
# define la pantalla con la parte baja del chat
# captura el texto del usuario
# almacena el texto en memoria
# llama a la api de chatgpt cun una llamada asincrona
# muestra la respuesta de la api
# muestra el texto en el chat con markdown
#
# revisa que el scrolling de la pantalla este funcionando
# agrega el spinner de carga
# habilita/deshabilita el boton de enviar
#
#

from nicegui import ui
import uuid
import os
import openai
import asyncio


# Store messages with metadata for chat history
dialog_messages = []

""" 
    {
        'user_message': {
            'role': 'user',
            'content': '',
            'timestamp': None,
            'message_id': None,
            'status': '',
            'metadata': {
                'tokens_used': 0,
                'session_id': None
            }
        },
        'assistant_message': {
            'role': 'assistant', 
            'content': '',
            'timestamp': None,
            'message_id': None,
            'status': '',
            'metadata': {
                'tokens_used': 0,
                'model': '',
                'temperature': 0,
                'session_id': None,
                'parent_message_id': None
            }
        },
    }

"""
 
dialog = [
    {
        'dialog_id': None,  # Unique ID for the message pair
        'dialog_status': '', # Overall status of the exchange
        'dialog_messages': dialog_messages
    }
]

user_info = {'name': None, 'avatar': None, 'user_id': 0, 'session_id': 0, 'dialog_id': 0}

@ui.page('/')
def main_page():

    def print_dialog():
        # Create a dialog window to display conversation history
        dialog_window = ui.dialog()
        
        with dialog_window:
            with ui.card().classes('w-full max-w-3xl mx-auto'):
                ui.label('Conversation History').classes('text-2xl font-bold mb-4')
                
                # Display each message in the dialog
                for msg in dialog_messages:
                    with ui.card().classes('my-2 p-2'):
                        # Header with role and timestamp
                        with ui.row().classes('justify-between items-center'):
                            ui.markdown(f"Role: {msg['role'].capitalize()}").classes('font-bold')
                            if msg['timestamp']:
                                ui.markdown(f"Time: {msg['timestamp']}").classes('text-sm text-gray-500')
                        
                        # Message content
                        ui.markdown(msg['content']).classes('mt-2 break-words')
                        
                        # Metadata footer
                        with ui.expansion('Show details').classes('mt-2'):
                            ui.label(f"Message ID: {msg['message_id']}")
                            #ui.label(f"Status: {msg['status']}")
                            #ui.label(f"Tokens: {msg['metadata'].get('tokens_used', 'N/A')}")
                            if msg['role'] == 'assistant':
                                ui.label(f"Model: {msg['metadata'].get('model', 'N/A')}")
                                ui.label(f"Temperature: {msg['metadata'].get('temperature', 'N/A')}")
                
                # Close button at the bottom
                with ui.row().classes('w-full justify-end mt-4'):
                    ui.button('Close', on_click=dialog_window.close).props('outline')
        
        dialog_window.open()

    async def call_chatgpt_api():
        # Configure OpenAI API settings
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        try:
            # Extract conversation history in OpenAI format
            messages = []
            for msg in dialog_messages:
                if msg['role'] in ['user', 'assistant']:
                    messages.append({
                        'role': msg['role'],
                        'content': msg['content']
                    })

            # Call OpenAI API
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )

            # Extract assistant's response
            assistant_message = response.choices[0].message.content
            tokens_used = getattr(response.usage, 'total_tokens', 0)

            # Update dialog with assistant's response
            dialog_messages.append({
                'role': 'assistant',
                'content': assistant_message,
                'timestamp': None,
                'message_id': None,
                'status': 'completed',
                'metadata': {
                    'tokens_used': tokens_used,
                    'model': 'gpt-3.5-turbo',
                    'temperature': 0.7,
                    'session_id': user_info['session_id'],
                    'parent_message_id': None
                }
            })

            # Display assistant's response directly
            if assistant_message:
                with scroll.classes('bg-gray-200'):
                    ui.markdown(assistant_message).classes('text-2xl p-2 m-1 bg-gray-200 rounded-lg break-words')
                
                scroll.scroll_to(percent=1e6)
                message_input.value = ''

            spinner.visible = False
            send_button.visible = True

            return assistant_message

        except Exception as e:
            print(f"Error calling ChatGPT API: {str(e)}")
            return "I apologize, but I encountered an error processing your request."




    # Assign a unique ID and avatar to each connecting client
    client_id = str(uuid.uuid4())
    session_id = str(uuid.uuid4())
    avatar = f'https://robohash.org/{client_id}?bgset=bg2'
    user_info['name'] = 'John Doe'
    user_info['avatar'] = avatar
    user_info['user_id'] = client_id
    user_info['session_id'] = session_id
    user_info['dialog_id'] = 1

    spinner = ui.spinner('audio', size='lg').classes('fixed bottom-1/2 left-1/2 transform -translate-x-1/2 translate-y-1/2 z-50')
    spinner.visible = False

    #Header
    with ui.header().classes('h-[10vh] bg-primary text-white'):
        ui.label('Reference Chat').classes('text-2xl font-bold')
        ui.button('Print', on_click=print_dialog).classes('bg-white text-blue')

    #ui.add_head_html('<style>body, html { height: 100%; margin: 0; overflow: hidden; }</style>')

    #with ui.dialog(value=True) as dialog, ui.card().classes('w-full min-h-[100%]'):
    #with ui.row().classes('w-full h-[80%] no-wrap items-center'):

    with ui.row().classes('h-[75vh] w-[90%] h-screen[90%] text-2xl'):
        # Create a scroll area for messages
        #scroll = ui.label().classes('w-[95%] mx-auto h-1/2 bg-white border-[20px] border-green-500 rounded-lg')


        scroll = ui.scroll_area().classes('w-[95%] mx-auto h-full bg-white border-[10px] border-blue-500 rounded-lg')
        #scroll = ui.scroll_area().classes( 'h-screen[90%] w-1/2 border-4 border-blue-500 rounded-lg flex-grow')

    #with ui.row().classes('w-full h-[80%] no-wrap items-center'):
    #   scroll1 = ui.scroll_area().classes( 'h4 border-4 w-[15%] border-blue-500 rounded-lg')




    #footer
    with ui.footer().classes('h-[10vh] bg-gray-200 text-white'):

            # User Avatar (optional)
            with ui.avatar():
                ui.image(avatar)

            def handle_key(e):
                if e.args.get('key') == 'Enter':
                    if e.args.get('shiftKey'):
                        return
                    if message_input.value.strip():
                        asyncio.create_task(send_message(message_input.value, 'user'))
                        # e.prevent_default()
 
            message_input = ui.textarea(placeholder='Type your message...') \
               .classes('flex-grow mx-2 text-2xl') \
               .props('rounded outlined dense rows=3 auto-grow')
            
            # send a message to the chat
            
            async def send_message(input_text, role):
                spinner.visible = True
                send_button.visible = False

                user_message = {
                    'role': 'user',
                    'content': input_text,
                    'timestamp': None,
                    'message_id': None,
                    'status': ''
                }

                dialog_messages.append(user_message)
                with scroll.classes('bg-gray-200'):
                    with ui.row().classes('w-full'):
                        ui.markdown(user_message['content']).classes('ml-auto w-2/3 text-2xl p-2 m-1 bg-blue-500 text-white rounded-lg break-words')
        
                scroll.scroll_to(percent=1e6)
                message_input.value = ''
                await call_chatgpt_api()
                #spinner.visible = False


            # Send button with delayed sending
            send_button = ui.button('Send', on_click=lambda: asyncio.create_task(send_message(message_input.value, 'user'))) \
                .classes('bg-primary text-white') \
                .props('rounded dense')
            message_input.on('keydown', handle_key)

            

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title='Reference Chat', storage_secret='a_secret_key_for_storage', port=8080, reload=True)