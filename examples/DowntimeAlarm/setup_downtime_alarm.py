from time import sleep

from pyremto.RemoteControl import RemoteControl

def run_10_minutes(logger: RemoteControl):
    for _ in range(5):
        sleep(50)
        logger.ping()

if __name__ == "__main__":
    logger = RemoteControl(show_qr=True, min_ping_interval_minutes=1)
    run_10_minutes(logger)