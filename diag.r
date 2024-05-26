from graphviz import Digraph

# Create Digraph object
dot = Digraph()

# Define nodes
dot.node('UI', 'User Interface (GUI Window)')
dot.node('Functions', 'Functions')
dot.node('FileSystem', 'File System')

# Define edges
dot.edge('UI', 'Functions', label='User clicks\n"Select Encrypted File"')
dot.edge('Functions', 'FileSystem', label='Opens file dialog')
dot.edge('FileSystem', 'Functions', label='User selects file')
dot.edge('Functions', 'FileSystem', label='Reads encrypted file')
dot.edge('Functions', 'FileSystem', label='Decrypts file using\nencryption key')
dot.edge
('Functions', 'FileSystem', label='Saves decrypted file\nin the same directory')
dot.edge('Functions', 'UI', label='Success message\nand decrypted file path')

# Render and save the graph
dot.render('file_decryption_diagram', format='png', cleanup=True)
