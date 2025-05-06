from nicegui import ui, app
from layout import create_navigation # Import the common navigation


@ui.page('/page2')
async def page2(): # Marked as async
    global_button = True


    def click_button(test_button, send_button, loading, label):
        nonlocal global_button
        print(f"Current global_button state: {global_button}")

        if global_button:
            print("Disabling button")
            test_button.disable()
            global_button = False
            loading.visible = False
            label.visible = True
        else:
            print("Enabling button")
            test_button.enable()
            global_button = True
            loading.visible = True
            label.visible = False

    """Page 2 content."""
    # WAIT for the client connection before accessing app.storage.tab
    await ui.context.client.connected()


    # Access or initialize tab-specific storage
    if 'page2_data' not in app.storage.tab:
        app.storage.tab['page2_data'] = 'Initial Data'
    if 'shared_message' not in app.storage.tab:
        app.storage.tab['shared_message'] = 'Hello from Tab!'

    create_navigation()

    ui.label('This is Page 2').classes('text-h4')

    # Display and modify page2's tab-specific data
    ui.label('Page 2 Specific Data:')
    ui.input(value=app.storage.tab['page2_data'],
             on_change=lambda e: update_data(e.value)).classes('w-full')

    # Display and modify the shared tab-specific variable
    ui.label('Shared Tab Message:')
    ui.input(value=app.storage.tab['shared_message'],
             on_change=lambda e: update_message(e.value)).classes('w-full')

    # Create a single row for all interactive elements
    with ui.row().classes('w-full justify-center'):
        with ui.dialog() as dialog, ui.card():
            ui.label('Test Dialog')
            with ui.row():
                ui.button('Accept', on_click=dialog.close)
                ui.button('Cancel', on_click=dialog.close)
        test_button = ui.button('Test', on_click=dialog.open).classes('w-full')
        send_button = ui.button('Send', on_click=lambda: click_button(test_button, send_button, loading, label)).classes('w-full')
        loading = ui.spinner('dots').classes('text-5xl text-primary')
        label = ui.label('Thinking...').classes('text-h6 q-mb-md')

    # Hide spinner and label initially
    loading.visible = False
    label.visible = True


def update_data(value):
    """Updates data in tab storage."""
    app.storage.tab['page2_data'] = value

def update_message(value):
    """Updates the shared message in tab storage."""
    app.storage.tab['shared_message'] = value

# Note: layout.py and main.py remain the same.