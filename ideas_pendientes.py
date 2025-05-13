#
# there are a set of elements to consider to create a chat function
# 
# Graphic elements:
# 1. a scroll area to display messages
# 2. a text input to type messages
#    handle key presses
#    respond to click send button
# 3. a send button to send messages
# 4. a spinner to show that the message is being sent
#
# Function elements
# 1. a function to send messages to the server
# 2. a function to display messages from the server and from the client
# 3. a function to handle key presses
# 4. a function to respond to click send button
#
# Storage elements
# 1. a list to store messages
# 2. database to store messages
# 3. a list to store the user's name, avatar, and session id
#
#
#


# Create a database manager instance
db = DatabaseManager("my_database.db")

# Create a table
db.create_table("users", [
    "id INTEGER PRIMARY KEY",
    "name TEXT NOT NULL",
    "email TEXT UNIQUE"
])

# Insert a record
user_id = db.insert("users", {
    "name": "John Doe",
    "email": "john@example.com"
})

# Query records
users = db.select("users", where="name LIKE ?", params=("%John%",))

# Update a record
db.update("users", 
    {"name": "John Smith"}, 
    where="id = ?", 
    params=(user_id,)
)

# Delete a record
db.delete("users", where="id = ?", params=(user_id,))

