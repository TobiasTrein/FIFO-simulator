import os
import logging
import time

# Create a log folder if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Define the log file path using the current timestamp
log_file = f"logs/log_{time.strftime('%Y%m%d-%H%M%S')}.log"

# Set up logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] %(message)s',
    handlers=[
        # Handler to output INFO level logs to console
        logging.StreamHandler(),
        # Handler to output all levels to log file
        logging.FileHandler(log_file)
    ]
)

# Set the log level for the console handler to INFO
logging.getLogger('').handlers[0].setLevel(logging.WARNING)
