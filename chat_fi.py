from nicegui import ui, app

# Initialize components

@ui.page('/chat_fi')
async def chat_fi_page():
    # Spinner for loading state - positioned absolute so it can be outside any container
    spinner = ui.spinner('dots', size='lg').classes('text-primary absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-50')
    spinner.visible = False
    
    # Chat messages container with bubble styling
    messages_container = ui.column().classes('w-full h-[73vh] overflow-y-auto p-4 gap-2 border border-solid border-gray-200 rounded-lg')
    
    # Store chat messages in this list to manage state
    chat_messages = []

    def send_message(e=None):
        text = message_input.value
        if text:
            # TODO: Process the message
            message_input.value = ''
        return text

    # Load previous messages
    @ui.refreshable
    async def load_conversation_history():
        empty_messages = []
        return empty_messages
        
        # Update the chat_messages list
    chat_messages.clear()
    
    # Display messages in the U
    for message in messages:
        chat_messages.append(message)
    
    # Scroll to bottom after loading history
    try:
        await ui.run_javascript('''
            setTimeout(() => {
                const container = document.querySelector('.h-\\\\[73vh\\\\]');
                if (container) {
                    container.scrollTop = container.scrollHeight;
                }
            }, 100);
        ''', timeout=5.0)
    except Exception as e:
        print(f"Error scrolling chat after loading history: {e}")
       
        # Scroll to bottom
        try:
            await ui.run_javascript('''
                setTimeout(() => {
                    const container = document.querySelector('.h-\\\\[73vh\\\\]');
                    if (container) {
                        container.scrollTop = container.scrollHeight;
                    }
                }, 100);
            ''', timeout=5.0)
        except Exception as e:
            print(f"Error scrolling chat: {e}")
        
        try:
            # Process message
            empty_messages = []

            # Scroll to bottom
            try:
                await ui.run_javascript('''
                    setTimeout(() => {
                        const container = document.querySelector('.h-\\\\[73vh\\\\]');
                        if (container) {
                            container.scrollTop = container.scrollHeight;
                        }
                    }, 100);
                ''', timeout=5.0)
            except Exception as e:
                print(f"Error scrolling chat: {e}")
            
        except Exception as e:
            ui.notify(f'Error processing message: {str(e)}', type='negative')
            
            # Add error message to chat interface
            with messages_container:
                with ui.element('div').classes('self-start bg-red-100 p-3 rounded-lg max-w-[80%] border-l-4 border-red-500'):
                    ui.markdown("**⚠️ Error**\n\nCould not get response")
            
            # Scroll to bottom
            try:
                await ui.run_javascript('''
                    setTimeout(() => {
                        const container = document.querySelector('.h-\\\\[73vh\\\\]');
                        if (container) {
                            container.scrollTop = container.scrollHeight;
                        }
                    }, 100);
                ''', timeout=5.0)
            except Exception as e:
                print(f"Error scrolling chat: {e}")
            
        finally:
            # Hide spinner
            spinner.visible = False
    
    # Message input area - direct child of the page content
    with ui.footer().classes('bg-white p-4'):
        with ui.row().classes('w-full items-center gap-2'):
            message_input = ui.input(placeholder='Type your message...').classes('w-full')
            
            # Allow sending message with Enter key
            message_input.on('keydown.enter', send_message)
            
            # Send button
            ui.button('Send', on_click=send_message).classes('bg-blue-500 text-white') 

# Run the NiceGUI app
ui.run(title='NiceGUI Chat Example', storage_secret='a_secret_key_for_storage', port=8080, reload=False)