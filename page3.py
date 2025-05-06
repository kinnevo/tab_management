from nicegui import ui, app
from layout import create_navigation # Import the common navigation

@ui.page('/page3')
async def page3(): # Marked as async
    """Page 3 content."""
    # WAIT for the client connection before accessing app.storage.tab
    await ui.context.client.connected()

    # Access or initialize tab-specific storage
    if 'page3_status' not in app.storage.tab:
        app.storage.tab['page3_status'] = False
    if 'shared_message' not in app.storage.tab:
        app.storage.tab['shared_message'] = 'Hello from Tab!'

    create_navigation()

    ui.label('This is Page 3').classes('text-h4')

    # Display and modify page3's tab-specific status
    ui.checkbox('Page 3 Status', value=app.storage.tab['page3_status'],
                on_change=lambda e: update_status(e.value))

    # Display the shared tab-specific variable
    ui.label('Shared Tab Message:')
    message_label = ui.label(app.storage.tab['shared_message'])

    # Create a dialog with spinner
    with ui.dialog() as dialog, ui.card():
        ui.spinner('ball').classes('text-5xl text-primary')
        ui.button('Close', on_click=dialog.close).classes('w-full')

    # Button to open the dialog
    ui.button('Show Loading', on_click=dialog.open).classes('w-full')

def update_status(value):
    """Updates a boolean status in tab storage."""
    app.storage.tab['page3_status'] = value

# The update_message function is not strictly needed in page3.py
# if page3 only displays the shared message and doesn't modify it.
# Keeping it here for completeness if you were to add an input later.
def update_message(value):
    """Updates the shared message in tab storage."""
    app.storage.tab['shared_message'] = value

# Note: layout.py and main.py remain the same.
