import csv
import os
from timeit import default_timer as timer

from services.SystemInterfaceService import SystemInterfaceService
from utils.utils import startup_wo_failing_speedy_python


def main_new(round_number) -> None:
    """
    This method uses the native python implementation to start the reactor and bring it into a stable, power producing
    state.
    Additionally, it saves the time that it needed to start the reactor and the round_number
    (which is an argument that needs to be parsed to this function) to a csv file.
    """
    start = timer()
    backend = SystemInterfaceService()
    backend.init(False)
    startup_wo_failing_speedy_python(backend)
    end = timer()
    with open("python.csv", "a", newline="") as file:
        writer = csv.writer(file, delimiter=",", quoting=csv.QUOTE_MINIMAL)
        if file.tell() == 0:
            writer.writerow(["RoundNumber", "ExecutionTime"])
        writer.writerow([round_number, end - start])
    os._exit(0)  # to make sure that every thread is killed


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create a ArcHydro schema")
    parser.add_argument("--round_number", metavar="path", required=True)
    args = parser.parse_args()
    main_new(round_number=args.round_number)
