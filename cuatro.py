from nicegui import ui
import asyncio
import uuid
messages = []
user_info = {'name': None, 'avatar': None, 'session_id': 0, 'user_id': 0}



@ui.page('/')
def main_page():

    def send_message_1():
        print('send_message_1')

    ui.label('Pagina cuatro').classes('text-2xl font-bold my-4')
    spinner = ui.spinner('dots', size='lg').classes('text-primary absolute bottom-4 left-1/2 transform -translate-x-1/2 z-50')
    spinner.visible = False


    spinner1 = ui.spinner('dots', size='lg').classes('text-primary absolute bottom-10 left-1/4 transform -translate-x-1/2 z-50')
    spinner1.visible = True



    button_flag = ui.button('Send', on_click=send_message_1).props('color=primary').classes('fixed bottom-12 left-1/2 transform -translate-x-1/2 z-[100] bg-primary text-white')
    button_flag.visible = True

 # Fixed spinner (independent of structure)
    spinner2 = ui.spinner('audio', size='lg').classes('fixed bottom-1/2 left-1/2 transform -translate-x-1/2 translate-y-1/2 z-50')
    spinner2.visible = True

    # App structure
    with ui.header().classes('bg-blue-500 text-white w-full'):
        ui.label('My Application')

    # Main content (scrollable area)
    with ui.column().classes('w-full overflow-auto flex-grow'):
        for i in range(20):
            ui.label(f'Content item {i}')

    # Footer
    with ui.footer().classes('bg-gray-200 p-4 w-full'):
        with ui.row().classes('w-full items-center gap-2'):
            ui.input(placeholder='Type message...').classes('flex-grow')
            button_flag = ui.button('Send', on_click=send_message_1).props('color=primary')
            button_flag.visible = True

   

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title='NiceGUI Chat Example', storage_secret='a_secret_key_for_storage', port=8080, reload=False)