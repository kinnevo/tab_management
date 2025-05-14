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

    async def call_chatgpt_api():

    # def call_chatgpt():
        print('call_chatgpt')
        print(dialog)
        print(dialog_messages)
        print("\n")

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
            print(f'response: {response}')

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
            #with ui.column().classes('w-full'):
            assistant_response = response.choices[0].message.content or ''
            #ui.label(assistant_response).style('font-size: 12px; padding: 8px; margin: 4px; background-color: white; border-radius: 4px; word-break: break-word;')


            print(assistant_message)
            print("\n")

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

    #Header
    with ui.header().classes('bg-primary text-white'):
        ui.label('Reference Chat').classes('text-2xl font-bold')

    with ui.row().classes('w-full no-wrap items-center'):
        # Create a scroll area for messages
        scroll = ui.scroll_area().classes('w-[95%] mx-auto h-64 bg-white border-[20px] border-green-500 rounded-lg')

    #footer
    with ui.footer().classes('bg-gray-200 text-white'):

            # User Avatar (optional)
            with ui.avatar():
                ui.image(avatar)

            def handle_key(e):
                if e.args.get('key') == 'Enter':
                    if e.args.get('shiftKey'):
                        return
                    if message_input.value.strip():
                        asyncio.create_task(send_message())
                        # e.prevent_default()
 
            message_input = ui.textarea(placeholder='Type your message...') \
               .classes('flex-grow mx-2') \
               .props('rounded outlined dense rows=3 auto-grow')
            
            # send a message to the chat
            
            async def send_message():
                print(f'send: {message_input.value}')

                user_message = {
                    'role': 'user',
                    'content': message_input.value,
                    'timestamp': None,
                    'message_id': None,
                    'status': ''
                }
            
                dialog_messages.append(user_message)
                with scroll.classes('bg-gray-200'):
                    ui.label(message_input.value).style('font-size: 12px; padding: 8px; margin: 4px; background-color: white; border-radius: 4px; word-break: break-word;')

                scroll.scroll_to(percent=1e6)
                message_input.value = ''
                await call_chatgpt_api()

            # Send button with delayed sending
            send_button = ui.button('Send', on_click=lambda: asyncio.create_task(send_message())) \
                .classes('bg-primary text-white') \
                .props('rounded dense')
            message_input.on('keydown', handle_key)

            

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title='Reference Chat', storage_secret='a_secret_key_for_storage', port=8080, reload=True)