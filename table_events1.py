from nicegui import ui

# Example columns and rows
columns = [
    {'name': 'id', 'label': 'ID', 'field': 'id'},
    {'name': 'name', 'label': 'Name', 'field': 'name'},
    {'name': 'action', 'label': 'Action', 'field': 'action'},
]
rows = [
    {'id': 1, 'name': 'Alice', 'action': 'Print Event'},
    {'id': 2, 'name': 'Bob', 'action': 'Print Row'},
    {'id': 3, 'name': 'Charlie', 'action': 'Show Notification'},
    {'id': 4, 'name': 'David', 'action': 'Open Dialog'},
    {'id': 5, 'name': 'Eve', 'action': 'Edit Form'},
]

table = ui.table(columns=columns, rows=rows, row_key='id')

def handle_cell_click(e):
    print(e)
    print(f'Cell clicked: {e.args}')

def handle_row_dblclick(e):
    print("Event args:", e.args)
    print("\n\n\n\n")

    print('--- Print Row Action ---\n')
    print('Row double-clicked:', {'id': 5, 'name': 'Eve', 'action': 'Edit Form'}, "\n")
    print('--- End of Print Row Action ---\n')

    row = getattr(e, 'row', None)
    if not row:
        return

    action = row['action']
    if action == 'Print Event':
        print('Double-click event:', e)
    elif action == 'Print Row':
        print('Row double-clicked:', row)
    elif action == 'Show Notification':
        ui.notify(f'Double-clicked row: {row["name"]}')
    elif action == 'Open Dialog':
        with ui.dialog() as dialog:
            ui.label(f'Details for {row["name"]}')
            ui.label(f'ID: {row["id"]}')
        dialog.open()
    elif action == 'Edit Form':
        with ui.dialog() as dialog:
            ui.label('Edit Row')
            name_input = ui.input('Name', value=row['name'])
            def save():
                row['name'] = name_input.value
                dialog.close()
            ui.button('Save', on_click=save)
        dialog.open()

table.on('cell-click', handle_cell_click)
table.on('row-dblclick', handle_row_dblclick)

ui.run(title='Table Events Example', port=8080)