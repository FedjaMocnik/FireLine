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
    cell2fire_path = os.path.join(original_dir, "../../Cell2Fire/cell2fire")

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

    # Run the command from the cell2fire directory
    subprocess.run(command, cwd=cell2fire_path)

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
    
    
# #!/bin/bash
# zagon iz Cell2Fire/cell2fire
# zagon: bash ../testiranje/tolmin/go.bash

# mydir=../testiranje/tolmin

# # pobrisemo prejsnji Data.csv
# rm $mydir/podatki/Data.csv

# python3 main.py --input-instance-folder $mydir/podatki/ --output-folder $mydir/results/ --ignitions --sim-years 1 --nsims 1 --finalGrid --weather rows --nweathers 1 --Fire-Period-Length 60.0 --Weather-Period-Length 60.0 --output-messages --ROS-CV 0.0 --seed 1134 --ignitions --stats --allPlots --IgnitionRad 5 --grids --combine --verbose
# #python3 main.py --input-instance-folder $mydir/podatki/ --output-folder $mydir/results/ --ignitions --sim-years 1 --nsims 5 --finalGrid --weather rows --nweathers 1 --Fire-Period-Length 1.0 --output-messages --ROS-CV 0.0 --seed 123 --stats --allPlots --IgnitionRad 5 --grids --combine


# # za gif iz Cell2Fire dir za ta primer
# cd ..
# python3 -m cell2fire.utils.gif testiranje/tolmin/results/Plots/Plots1 testiranje/tolmin/results/Plots/Plots1/tolmin_output.gif    

