#!/bin/sh
#SBATCH --job-name=createDataset
#SBATCH --output=/home/s2155435/createDataset.out
#SBATCH --error=/home/s2155435/createDataset.err
#SBATCH --mail-user="christie@ziggo.nl"
#SBATCH --mail-type="ALL"
#SBATCH --partition=cpu-medium
#SBATCH -c 1
#SBATCH --time=1-00:00:00
#SBATCH --mem-per-cpu=32gb

export PYTHONPATH=/home/s2155435/wateroverlast/
module load Miniconda3/4.7.10
conda init bash
source ~/.bashrc
conda activate bepalice
python3 /home/s2155435/wateroverlast/scripts/get_w_rain.py alice