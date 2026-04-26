from pathlib import Path
from ex3.no_starvation.dont_starve_unit import HospitalNoStarvation
from ex3.starvation.starvation_unit import HospitalStarvation

if __name__ == "__main__":
    file_path = Path(__file__).parent / "inputs" / "json1.json"

    h1 = HospitalStarvation(file_path)
    h1.run()
    h1.print_result("POSSIVEL STARVATION")

    h2 = HospitalNoStarvation(file_path)
    h2.run()
    h2.print_result("SEM STARVATION")