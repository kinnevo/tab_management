from nicegui import ui, app
from layout import create_navigation # Import the common navigation

@ui.page('/')
async def page1(): # Marked as async
    """Page 1 content."""
    # WAIT for the client connection before accessing app.storage.tab
    await ui.context.client.connected()

    # Access or initialize tab-specific storage
    if 'page1_counter' not in app.storage.tab:
        app.storage.tab['page1_counter'] = 0
    if 'shared_message' not in app.storage.tab:
        app.storage.tab['shared_message'] = 'Hello from Tab!'

    create_navigation()

    ui.label('This is Page 1').classes('text-h4')

    # Display tab-specific counter
    counter_label = ui.label(f'Page 1 Counter: {app.storage.tab["page1_counter"]}')

    def increment_counter():
        """Increments a counter in tab storage and updates the UI."""
        app.storage.tab['page1_counter'] += 1
        counter_label.set_text(f'Page 1 Counter: {app.storage.tab["page1_counter"]}')

    ui.button('Increment Counter', on_click=increment_counter)

    # Display and modify a shared tab-specific variable
    ui.label('Shared Tab Message:')
    ui.input(value=app.storage.tab['shared_message'],
             on_change=lambda e: update_message(e.value)).classes('w-full')

def update_message(value):
    """Updates the shared message in tab storage."""
    # This function is called from an event handler, which is generally fine
    # as the client is connected when events are triggered.
    app.storage.tab['shared_message'] = value

# Note: layout.py and main.py remain the same.