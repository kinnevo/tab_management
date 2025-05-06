from nicegui import ui

def create_navigation():
    """Creates navigation links visible on all pages."""
    ui.add_head_html('<style>a { margin-right: 1em; }</style>') # Basic styling for spacing
    ui.link('Go to Page 1', '/')
    ui.link('Go to Page 2', '/page2')
    ui.link('Go to Page 3', '/page3')
    ui.separator()

# You can also put helper functions that modify storage here if they are used across pages,
# but for this example, we'll keep them in the respective page files for clarity.
# If helper functions were truly shared, they would go here or in another common file.