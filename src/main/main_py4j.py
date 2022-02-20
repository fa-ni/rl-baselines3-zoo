import csv
import subprocess
from timeit import default_timer as timer

from py4j.java_gateway import JavaGateway

from utils.utils import startup_wo_failing_speedy_java


def main(round_number: int) -> None:
    """
    This method starts the jar as a subprocess and communicates with the java program over a java gateway using the
    py4j framework. After starting the java application it sets all necessary action to start the reactor and bring
    it to a stable, power producing state.
    Additionally, it saves the time that it needed to start the reactor and the round_number
    (which is an argument that needs to be parsed to this function) to a csv file.
    """
    start = timer()
    p = subprocess.Popen(["java", "-jar", "NPP_Simu.jar"])
    while True:
        try:
            gateway = JavaGateway(java_process=p)  # connect to the JVM
            entry = gateway.entry_point
            backend = entry.getSystemInterface()
            backend.init(False)
            startup_wo_failing_speedy_java(backend)
            end = timer()
            print(f"TIME TOTAL: {end - start}")
            with open("py4j.csv", "a", newline="") as file:
                writer = csv.writer(file, delimiter=",", quoting=csv.QUOTE_MINIMAL)
                if file.tell() == 0:
                    writer.writerow(["RoundNumber", "ExecutionTime"])
                writer.writerow([round_number, end - start])
            gateway.shutdown()
            p.kill()
            break
        except:
            pass


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create a ArcHydro schema")
    parser.add_argument("--round_number", metavar="path", required=True)
    args = parser.parse_args()
    main(round_number=args.round_number)
