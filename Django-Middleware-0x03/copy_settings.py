import shutil
import os

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Source and destination paths
source = os.path.join(current_dir, 'messaging_app', 'settings.py')
destination = os.path.join(current_dir, 'Django-Middleware-0x03', 'settings.py')

# Create destination directory if it doesn't exist
os.makedirs(os.path.dirname(destination), exist_ok=True)

# Copy the file
shutil.copy2(source, destination)
print(f"Copied {source} to {destination}")
