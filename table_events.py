from nicegui import ui

# Example columns and rows (using a list, which is mutable)
columns = [
    {'name': 'id', 'label': 'ID', 'field': 'id', 'sortable': True},
    {'name': 'name', 'label': 'Name', 'field': 'name', 'sortable': True},
    {'name': 'action', 'label': 'Action', 'field': 'action'},
]
rows = [
    {'id': 1, 'name': 'Alice', 'action': 'Print Event'},
    {'id': 2, 'name': 'Bob', 'action': 'Print Row'},
    {'id': 3, 'name': 'Charlie', 'action': 'Show Notification'},
    {'id': 4, 'name': 'David', 'action': 'Open Dialog'},
    {'id': 5, 'name': 'Eve', 'action': 'Edit Form'},
]

@ui.page('/table_events')  # Add this line to specify the root route
def main():
    # --- Event Handlers ---
    def handle_row_dblclick(e):
        """Handles the double-click event on a table row."""
        print("Row double-click event arguments:", e.args)  # Debug: See what's in the event


        print("\n\nNumber of args:", len(e.args))
        print("Arg 1:", e.args[0])
        print("Arg 2:", e.args[1]) 
        print("Arg 3:", e.args[2])

        # Iterate through the event arguments
        for i, arg in enumerate(e.args):
            print(f"Argument {i + 1}:")
            if isinstance(arg, dict):
                for key, value in arg.items():
                    print(f"  {key}: {value}")
            else:
                print(f"  {arg}")
        
        print("\n\n\n\n")

        print('--- Print Row Action ---\n')
        print('Row double-clicked:', {'id': 5, 'name': 'Eve', 'action': 'Edit Form'}, "\n")
        print('--- End of Print Row Action ---\n')


        if not e.args or 'row' not in e.args:
            ui.notify("Could not get row data from double-click event.", type='negative')
            print("Event arguments missing 'row' key:", e.args)
            return

        # The row data from the event
        event_row_data = e.args['row']
        action = event_row_data.get('action', 'Unknown Action') # Use .get for safety
        row_id = event_row_data.get('id')

        print(f"Double-clicked Row ID: {row_id}, Action: {action}")

        if action == 'Print Event':
            print('--- Print Event Action ---')
            print('Raw Double-click event args:', e.args)
            ui.notify(f'Printed event args for {event_row_data.get("name", "N/A")} to console.')

        elif action == 'Print Row':
            print('--- Print Row Action ---')
            print('Row double-clicked:', event_row_data)
            ui.notify(f'Printed row data for {event_row_data.get("name", "N/A")} to console.')

        elif action == 'Show Notification':
            print('--- Show Notification Action ---')
            ui.notify(f'Double-clicked row: {event_row_data.get("name", "N/A")} (ID: {row_id})', type='positive')

        elif action == 'Open Dialog':
            print('--- Open Dialog Action ---')
            dialog = ui.dialog()
            with dialog:
                with ui.card():
                    ui.label(f'Details for {event_row_data.get("name", "N/A")}').classes('text-h6')
                    ui.label(f'ID: {event_row_data.get("id", "N/A")}')
                    ui.label(f'Action: {event_row_data.get("action", "N/A")}')
                    ui.button('Close', on_click=dialog.close).classes('mt-4')
            dialog.open()

        elif action == 'Edit Form':
            print('--- Edit Form Action ---')
            dialog = ui.dialog().props('persistent') # Persistent prevents closing on outside click
            with dialog:
                with ui.card():
                    ui.label(f'Edit Row ID: {row_id}').classes('text-h6')
                    # Use the value from the event data for the initial input value
                    name_input = ui.input('Name', value=event_row_data.get('name', ''))

                    def save_changes():
                        # Find the original row in the main 'rows' list using its ID
                        original_row = next((r for r in rows if r['id'] == row_id), None)
                        if original_row:
                            print(f"Updating name for ID {row_id} from '{original_row['name']}' to '{name_input.value}'")
                            original_row['name'] = name_input.value  # Update the original data source
                            table.update()  # Crucial: Refresh the table UI
                            ui.notify(f'Updated name for ID {row_id}', type='positive')
                            dialog.close()
                        else:
                            print(f"Error: Could not find original row with ID {row_id} to update.")
                            ui.notify(f'Error updating row ID {row_id}', type='negative')

                    with ui.row().classes('mt-4 w-full justify-end'):
                        ui.button('Save', on_click=save_changes)
                        ui.button('Cancel', on_click=dialog.close)
            dialog.open()

        else:
            ui.notify(f"Unknown action '{action}' for row ID {row_id}", type='warning')

    # --- Table Creation and Event Binding ---
    ui.label('Double-click a row to trigger its action.').classes('text-subtitle1 mb-2')

    table = ui.table(columns=columns, rows=rows, row_key='id').classes('w-full') # Added row_key

    # Bind the CORRECT event name 'row-dblclick'
    table.on('row-dblclick', handle_row_dblclick)

    # Optional: Add single cell click handler for comparison/debugging
    # def handle_cell_click(e):
    #     print(f'Single cell clicked: {e.args}')
    # table.on('cell-click', handle_cell_click)

# --- Run the App ---
ui.run(title='Table Row Double-Click Events', port=8080, reload=False) # reload=False can be helpful during dev