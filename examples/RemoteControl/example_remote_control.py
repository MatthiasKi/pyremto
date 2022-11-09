from pyremto.RemoteControl import RemoteControl
from pyremto.Datatype import Datatype

def compute_performance(hyperparameter: float):
    return hyperparameter / 2

def ask_for_input(remote: RemoteControl):
    performance = 42.42
    remote.log_string(f"{performance}", description="Performance")

    new_hyperparameter = remote.get_input(datatype=Datatype.FLOAT, desciption="New Hyperparameter to test")
    
    performance = compute_performance(new_hyperparameter)
    remote.log_string(f"{performance}", description="New Performance", send_push_notification=True)

if __name__ == "__main__":
    remote = RemoteControl(show_qr=True)
    ask_for_input(remote)