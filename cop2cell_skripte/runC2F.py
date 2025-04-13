# ZA ZAGON main.py (Cell2Fire) V main.py (FireLine)

import subprocess
import os

def run_cell2fire(
    input_folder,
    output_folder,
    ignitions=True,
    sim_years=1,
    nsims=1,
    final_grid=True,
    weather="rows",
    nweathers=1,
    fire_period_length=1.0,
    output_messages=True,
    ros_cv=0.0,
    seed=123,
    stats=True,
    all_plots=True,
    ignition_rad=5,
    grids=True,
    combine=True
):

    original_dir = os.getcwd()  # Save the current directory
    cell2fire_path = os.path.join(original_dir, "../Cell2Fire/cell2fire")
    gif_path = os.path.join(original_dir, "../Cell2Fire")
    # "../Cell2Fire/cell2fire" in "../Cell2Fire" CE LAUFA"S V main.py


    # Base command
    command = [
        "python3", "main.py",
        "--input-instance-folder", input_folder,
        "--output-folder", output_folder,
        "--sim-years", str(sim_years),
        "--nsims", str(nsims),
        "--weather", weather,
        "--nweathers", str(nweathers),
        "--Fire-Period-Length", str(fire_period_length),
        "--ROS-CV", str(ros_cv),
        "--seed", str(seed),
        "--IgnitionRad", str(ignition_rad),
    ]

    # Add optional flags
    if ignitions: command.append("--ignitions")
    if final_grid: command.append("--finalGrid")
    if output_messages: command.append("--output-messages")
    if stats: command.append("--stats")
    if all_plots: command.append("--allPlots")
    if grids: command.append("--grids")
    if combine: command.append("--combine")

    # ODSTRANI data.csv
    try:
        os.remove("cop2cell_skripte/results/Data.csv")
        print("Data.csv je izbrisan (se mi zdi).")
    except FileNotFoundError:
        print("Ni Data.csv za izbrisati.")
    
    # Run the command from the cell2fire directory
    subprocess.run(command, cwd=cell2fire_path)
    
    subprocess.run(["python3", "cell2fire/utils/gif.py", "../FireLine/rezultati_cell2fire/Plots/Plots1", "../FireLine/rezultati_cell2fire/output.gif"], cwd=gif_path)


    # Back to the original directory (not strictly needed unless you're doing more afterward)
    os.chdir(original_dir)

# Example call
def main():
    run_cell2fire(
        input_folder="../../FireLine/cop2cell_skripte/results/",
        output_folder="../../FireLine/rezultati_cell2fire/",
        sim_years=1,
        nsims=1,
    )

if __name__=="__main__":
    main()
