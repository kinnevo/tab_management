from nicegui import ui

# Header
with ui.header().classes('bg-blue-100'):
    ui.label("My Awesome Header").classes('text-2xl font-bold')

# Main content
with ui.column().classes('w-full p-4'):
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
with ui.footer().classes('bg-gray-100'):
    ui.label("© 2023 My Website").classes('text-lg text-black')

ui.run()
