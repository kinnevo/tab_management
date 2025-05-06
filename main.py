from nicegui import ui

# Import the page modules - this registers the pages with NiceGUI
import page1
import page2
import page3

# Run the app
# We enable storage by providing a storage_secret
ui.run(storage_secret='my-secret-key')