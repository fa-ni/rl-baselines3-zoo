import csv
from timeit import default_timer as timer

import jnius_config

from utils.utils import startup_wo_failing_speedy_java


def main(round_number: int) -> None:
    """
    This method starts the jar as a with the help of the pyjnius implementation. It communicates over the JNI with the
    java application.
    After starting the java application it sets all necessary action to start the reactor and bring it to a
    stable,power producing state.
    Additionally, it saves the time that it needed to start the reactor and the round_number
    (which is an argument that needs to be parsed to this function) to a csv file.
    """

    start = timer()
    jnius_config.add_classpath("NPP_Simu.jar")
    from jnius import autoclass  # Somehow this  import has to be here

    gateway_class = autoclass("org.base.Gateway")
    gateway_object = gateway_class()
    backend = gateway_object.getSystemInterface()
    backend.init(False)
    startup_wo_failing_speedy_java(backend)
    end = timer()
    with open("pyjnius.csv", "a", newline="") as file:
        writer = csv.writer(file, delimiter=",", quoting=csv.QUOTE_MINIMAL)
        if file.tell() == 0:
            writer.writerow(["RoundNumber", "ExecutionTime"])
        writer.writerow([round_number, end - start])


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create a ArcHydro schema")
    parser.add_argument("--round_number", metavar="path", required=True)
    args = parser.parse_args()
    main(round_number=args.round_number)
