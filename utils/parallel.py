import multiprocessing
from typing import Callable, Iterable, TypeVar, List
import sys

T = TypeVar("T")
R = TypeVar("R")


def run_parallel(
    worker_func: Callable[[T], R],
    tasks: Iterable[T],
    processes: int = None,
    chunksize: int = 10,
) -> List[R]:
    """
    Executes a worker function in parallel across a list of tasks using multiprocessing.

    Args:
        worker_func: The function to execute for each task.
        tasks: An iterable of arguments to pass to the worker function.
        processes: Number of processes to use. Defaults to CPU count or 4.
        chunksize: The chunksize for the map operation.

    Returns:
        A list of results from the worker function.
    """
    if processes is None:
        try:
            cpu_count = multiprocessing.cpu_count()
            processes = max(1, cpu_count)
        except NotImplementedError:
            processes = 4

    print(f"Running with {processes} processes...", file=sys.stderr)

    # Use 'fork' context to avoid pickling issues with dynamic imports
    ctx = multiprocessing.get_context("fork")

    with ctx.Pool(processes=processes) as pool:
        return pool.map(worker_func, tasks, chunksize=chunksize)
