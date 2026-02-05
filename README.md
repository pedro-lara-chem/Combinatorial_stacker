# Combinatorial Stacker
A Python tool for generating supramolecular stacks by combinatorially rotating and translating molecular units. 
This script reads one or more molecular geometries (XYZ format), centers them, and generates a series of stacked geometries where every unit in the stack is rotated independently.  This is essential for sampling potential energy surfaces of aggregates, crystals, or columns to find the most stable stacking configurations. 
## Features
* **Combinatorial Generation:** Generates *all* possible rotation combinations for a stack of $N$ molecules. 
* **Multi-Molecule Support:** If multiple input files are provided, the tool generates every possible molecular ordering (e.g., A-A, A-B, B-B). 
* **Systematic Rotations:** Rotates units based on a user-defined interval (Default: 30°). 
* **Flexible Displacement:** Stacks molecules with custom vertical ($Z$) and lateral ($X$) offsets.
* **Auto-Centering:** Automatically recenters the input molecule to the origin before stacking to ensure rotation consistency.
## Prerequisites
* **Python 3.x**
numpy 
## Installation
**Clone the repository:**
```bash 
git clone https://github.com/YOUR_USERNAME/molecular-stacker.git
cd molecular-stacker
```
**Install dependencies:**
```bash
pip install -r requirements.txt
```
## Usage
Run the script from the command line by providing your input .xyz files and desired parameters: 
```bash
python stacker.py [input_files ...] [options]
```
### Examples
* **Generate Dimer Configurations (Default):** Creates a stack of 2 molecules from a single input. 
```bash
python stacker.py benzene.xyz
```
* **Hetero-stack with Custom Spacing:** Creates a stack of 2 molecules using two different species with a 3.5 Å vertical gap.
```bash
python stacker.py donor.xyz acceptor.xyz --z_dist 3.5
```
* **Generate Trimer Configurations:** Creates a stack of 3 molecules with a 15° rotation step.
```bash
python stacker.py molecule.xyz -n 3 --rot_step 15
```
## Options
| Argument | Flag | Description | Default |
| :--- | :--- | :--- | :--- |
| `input_files` | (Positional) | List of `.xyz` files to stack. | Required |
| `num_layers` | `-n` | Total number of molecules in the stack. | `2` |
| `z_dist` | `--z_dist` | Vertical distance between layers (Å). | `6.0` |
| `x_dist` | `--x_dist` | Horizontal offset between layers (Å). | `0.0` |
| `rot_step` | `--rot_step` | Rotation interval in degrees. | `30` |
## How It Works
* **Centering:** The script calculates the centroid of the input atoms and translates the molecule to $(0,0,0)$. 
* **Library Building:** All provided .xyz files are loaded into a library for combinatorial selection. 
* **Combinatorics:**  It calculates the Cartesian product of all possible rotation angles for the number of layers requested. * It calculates the Cartesian product of the molecular order (which molecule goes in which layer). 
* **Construction:** For each combination, layers are rotated around the Z-axis and translated according to their position in the stack. 
* **Output:** Files are organized into sub-directories named after the molecular order (e.g., stacked_geometries/A-B-A/). 
## Acknowledgments
This software was developed by **Pedro Lara Salcedo at Excited States Reactivity Group** at **Universidad Autónoma de Madrid**.  This work was supported by **Diseño y caracterización de nuevos materiales moleculares y optimización de fármacos: Sinergia experimento y teoría$$** under grant number **$$PGC2018-094644-B-C21$$**.
