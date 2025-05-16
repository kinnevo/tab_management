from nicegui import ui

# Header
with ui.header().classes('h-[10vh] bg-blue-100 flex items-center justify-center'):
    ui.label("My Awesome Header").classes('text-2xl font-bold')

# Content (1/3 of the screen height)
with ui.element('div').classes('h-[75vh] bg-white p-4 overflow-y-auto'):
    ui.label("This is the main content area.").classes('text-lg')
    ui.markdown("""
    ## Some Content

    You can add all your important information, interactive elements, and more here.

    - Lists
    - Buttons
    - Charts
    - Input fields
    - And much more!

    Feel free to scroll down to see more content.
    """)
    for i in range(50):
        ui.label(f"Content Item {i+1}")

# Footer
with ui.footer().classes('h-[10vh] bg-gray-100 flex items-center justify-center'):
    ui.label("© 2023 My Website").classes('text-sm text-black')

ui.run()
