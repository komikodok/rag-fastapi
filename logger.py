import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout), 
        logging.FileHandler('app.log')
    ],
)
logger = logging.getLogger(__name__)