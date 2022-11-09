from time import sleep
import random

from pyremto.RemoteControl import RemoteControl

def log_example_values(logger: RemoteControl):
    logger.log_string("Hallo", description="Test String")
    sleep(5)
    logger.log_int(42, description="Test Integer")
    
    for _ in range(10):
        logger.log_data_point(random.random(), random.random(), description="Test Data Points")
        sleep(2)

if __name__ == "__main__":
    logger = RemoteControl(show_qr=True)
    log_example_values(logger)