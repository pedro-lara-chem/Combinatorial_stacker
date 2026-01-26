# Combinatorial_stacker
A Python tool for generating supramolecular stacks by combinatorially rotating and translating a monomer unit. 
This script reads a molecular geometry (XYZ format), centers it, and generates a series of stacked geometries where every unit in the stack is rotated independently. This is useful for sampling potential energy surfaces of aggregates, crystals, or columns to find the most stable stacking configuration.

## Features

- **Combinatorial Generation:** Generates *all* possible rotation combinations for a stack of $N$ molecules.
- **Systematic Rotations:** Rotates units in 30° increments (0°, 30°, ..., 330°).
- **Fixed Displacement:** Stacks molecules with a predefined offset (Default: 6.0 Å Vertical, 5.0 Å Lateral).
- **Auto-Centering:** Automatically recenters the input molecule to the origin before stacking.

## Prerequisites

- Python 3.x
- `numpy`

## Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/molecular-stacker.git](https://github.com/YOUR_USERNAME/molecular-stacker.git)
   cd molecular-stacker
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
## Usage 

Run the script from the command line, providing your input .xyz file:
```bash
python stacker.py input_molecule.xyz
```
## Examples

1. Generate Dimer Configurations (Default)Creates a stack of 2 molecules. Generates $12^2 = 144$ geometries.
```bash
python stacker.py benzene.xyz
```
2. Generate Trimer Configurations
Creates a stack of 3 molecules. Generates $12^3 = 1,728$ geometries.
```bash
python stacker.py benzene.xyz -n 3
```
## Options

| Argument | Flag | Description | Default |
| :--- | :--- | :--- | :--- |
| `input_file` | (Positional) | Path to the `.xyz` file containing the monomer. | Required |
| `num_copies` | `-n` | Number of molecules in the stack. | `2` |
## How It Works

1. Centering: The script calculates the centroid of the input atoms and translates the molecule to (0,0,0).
2. Grid Generation: It creates a list of rotation angles $[0, 30, 60, ..., 330]$.
3. Combinatorics: It calculates the Cartesian product of these angles for the number of copies requested.
   * Example (Dimers): (0°,0°), (0°,30°)... (330°,330°).
4. Construction: For each combination:
   * Molecule 1: Rotated by Angle A, Translated by $(0, 0, 0)$.
   * Molecule 2: Rotated by Angle B, Translated by $(5.0, 0.0, 6.0)$.
   * Molecule N: Rotated by Angle N, Translated by $(5.0 \times (N-1), 0.0, 6.0 \times (N-1))$.
5. Output: Files are saved to a stacked_geometries/ directory.
## Configuration
The displacement and rotation parameters are currently defined as constants inside stacker.py. You can modify them by editing the generate_combinations method:
```python
Z_DISPLACEMENT = 6.0 # Vertical separation (Z-axis)
X_DISPLACEMENT = 5.0 # Lateral offset (X-axis)
ROTATION_STEP = 30   # Rotation increment in degrees
```
