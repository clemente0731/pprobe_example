import os
import threading
print(f"start ==> example_5/sitecustomize.py (pid: {os.getpid()}, thread: {threading.current_thread().ident})")


import time
import functools
from typing import Any, Callable
import torch 
func_counts = 0


def log_to_csv(step, execution_time, loss_value=None):
    """log training metrics to csv file"""
    import os
    import csv
    
    csv_file = "training_log.csv"
    file_exists = os.path.isfile(csv_file)
    
    with open(csv_file, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['step', 'time', 'loss'])
        writer.writerow([step, execution_time, loss_value])

def get_loss_value(args):
    """extract loss value from args if possible"""
    loss_value = None
    if len(args) > 0 and hasattr(args[0], 'grad_fn'):
        try:
            loss_value = float(args[0].item())
        except:
            loss_value = "N/A"
    return loss_value

def check_max_steps(current_count, func_name, execution_time, loss_value):
    """check if we need to exit after certain steps"""
    import os
    import sys
    
    max_steps = int(os.environ.get('MAX_TRAINING_STEPS', '10'))
    print(f"training func_name {func_name} --> counts {current_count}, time: {execution_time:.4f}s")
    
    # log metrics to csv
    log_to_csv(current_count, execution_time, loss_value)
    
    if current_count >= max_steps:
        print(f"Reached maximum training steps ({max_steps}), exiting...")
        sys.exit(0)

def func_torch_step_count_wrapper(func):
    """
    torch.autograd.backward / torch.Tensor.backward
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        global func_counts

        if callable(func):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            func_counts += 1
            
            # get loss value if available
            loss_value = get_loss_value(args)
            
            # check if we need to stop and log metrics
            check_max_steps(func_counts, func, end-start, loss_value)
                
            return result
        else:
            # handle the case where func is not callable
            print(f"func:{func} is not callable")
            return None

    return wrapper


torch.autograd.backward = func_torch_step_count_wrapper(
    torch.autograd.backward
)

print(f"end ==> example_7/sitecustomize.py (pid: {os.getpid()}, thread: {threading.current_thread().ident})")
