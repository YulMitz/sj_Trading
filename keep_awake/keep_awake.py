import time
import multiprocessing as mp
import os
import atexit
import logging
import sys
import signal

# numpy for CPU
import numpy as np

# torch for GPU
import torch

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)  # Log to stdout (will be redirected to file by nohup)
    ]
)
logger = logging.getLogger()

# -------------------------------
# Params
# -------------------------------
# CPU
CPU_MATRIX_SIZE = 128

# GPU
GPU_MATRIX_SIZE = 256

# Run duration
RUN_DURATION = None  # None for forever

# PID file location
PID_FILE = "matmul_worker.pid"

# Write PID file
def write_pid_file():
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))
    
    logger.info(f"Main process PID: {os.getpid()} written to {PID_FILE}")
    # Remove PID file on normal exit
    atexit.register(lambda: os.remove(PID_FILE) if os.path.exists(PID_FILE) else None)

# -------------------------------
# CPU Worker
# -------------------------------
def cpu_worker(stop_event: mp.Event, worker_id: int):
    logger.info(f"[CPU Worker {worker_id}] running, PID: {os.getpid()}")
    A = np.random.rand(CPU_MATRIX_SIZE, CPU_MATRIX_SIZE).astype(np.float64)
    B = np.random.rand(CPU_MATRIX_SIZE, CPU_MATRIX_SIZE).astype(np.float64)

    iteration = 0
    while not stop_event.is_set():
        C = np.dot(A, B)
        iteration += 1
        if iteration % 100 == 0:
            logger.info(f"[CPU Worker {worker_id}] had completed {iteration} matmul operations")
        time.sleep(3)


# -------------------------------
# GPU Worker
# -------------------------------
def gpu_worker(stop_event: mp.Event, gpu_id: int):
    logger.info(f"[GPU Worker] GPU {gpu_id} running, PID: {os.getpid()}")
    device = torch.device(f"cuda:{gpu_id}")
    torch.cuda.set_device(device)
    
    try:
        A = torch.randn(GPU_MATRIX_SIZE, GPU_MATRIX_SIZE, device=device, dtype=torch.float32)
        B = torch.randn(GPU_MATRIX_SIZE, GPU_MATRIX_SIZE, device=device, dtype=torch.float32)
    except RuntimeError as e:
        logger.error(f"[GPU Worker] GPU {gpu_id} failed initializing matrix: {e}")
        return

    iteration = 0
    torch.mm(A, B)
    torch.cuda.synchronize(device)
    
    while not stop_event.is_set():
        C = torch.mm(A, B)
        iteration += 1
        if iteration % 50 == 0:
            logger.info(f"[GPU Worker] GPU {gpu_id} had completed {iteration} matmul operations")
            torch.cuda.empty_cache()
        time.sleep(2)


# -------------------------------
# Main function
# -------------------------------
def main():
    # Make stdout and stderr unbuffered to ensure real-time logging
    sys.stdout.reconfigure(line_buffering=True)
    sys.stderr.reconfigure(line_buffering=True)

    # Write PID to file for easier termination
    write_pid_file()

    mp.set_start_method('spawn', force=True)
    stop_event = mp.Event()

    # Start CPU workers
    cpu_worker_count = 4
    cpu_workers = []
    for i in range(cpu_worker_count):
        p = mp.Process(target=cpu_worker, args=(stop_event, i))
        p.start()
        cpu_workers.append(p)

    # Start GPU workers
    gpu_count = torch.cuda.device_count()
    if gpu_count == 0:
        logger.warning("No GPU found, skipping GPU workers.")
        gpu_workers = []
    else:
        gpu_workers = []
        for gpu_id in range(gpu_count):
            p = mp.Process(target=gpu_worker, args=(stop_event, gpu_id))
            p.start()
            gpu_workers.append(p)

    logger.info(f"Keep awake program now running with {len(cpu_workers)} CPU workers and {len(gpu_workers)} GPU workers.")

    try:
        if RUN_DURATION is None:
            while True:
                time.sleep(1)
        else:
            time.sleep(RUN_DURATION)
    except KeyboardInterrupt:
        logger.info("Keyboard Interrupt, stopping workers...")
    finally:
        stop_event.set()
        for p in cpu_workers + gpu_workers:
            p.join(timeout=10)
        logger.info("All workers have been stopped.")

if __name__ == "__main__":
    main()