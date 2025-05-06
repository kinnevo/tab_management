from nicegui import ui

@ui.page('/index')
def index():
    ui.label('Hello World')

    # Create a text area with scrolling capability
    with ui.card().classes('w-96').style('text-green-500 background-color: grey-500; border: 10px solid green; border-radius: 0; padding: 0;'):
        ui.textarea(
            value="This is a scrollable text area with a green border, white background, and 12px font size. You can add more text here to test the scrolling functionality.\n\n" + "Sample text. " * 50,
        ).props('readonly').classes('w-full h-64').style('font-size: 24px; background-color: white; color: black;')

    with ui.card().classes('w-96').style('text-green-100  border: 10px solid green; border-radius: 0; padding: 0;'):
        ui.textarea(
            value="This is a scrollable text area with a green border, grey background, and 12px font size. You can add more text here to test the scrolling functionality.\n\n" + "Sample text. " * 50,
        ).props('readonly').classes('w-full h-64').style('font-size: 12px; background-color: grey; color: black;')

    # Add buttons for scrolling
    with ui.row().classes('w-96 justify-between'):
        ui.button('Scroll to Top', on_click=lambda: ui.run_javascript('''
            const textareas = document.getElementsByTagName('textarea');
            if (textareas.length > 0) {
                textareas[textareas.length-1].scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            }
        ''')).classes('bg-blue-500 text-white')
        
        ui.button('Scroll to Bottom', on_click=lambda: ui.run_javascript('''
            const textareas = document.getElementsByTagName('textarea');
            if (textareas.length > 0) {
                const textarea = textareas[textareas.length-1];
                textarea.scrollTo({
                    top: textarea.scrollHeight,
                    behavior: 'smooth'
                });
            }
        ''')).classes('bg-blue-500 text-white')

# Create a text area with scrolling capability
with ui.card().classes('w-96').style('background-color: grey; border: 20px solid green; border-radius: 0; padding: 0;'):
    ui.textarea(
        value="This is a scrollable text area with a green border, grey background, and 12px font size. You can add more text here to test the scrolling functionality.\n\n" + "Sample text. " * 50,
    ).props('readonly').classes('w-full h-64').style('font-size: 12px; background-color: grey; color: black;')

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title='NiceGUI Chat Example', storage_secret='a_secret_key_for_storage', port=8080, reload=False)
