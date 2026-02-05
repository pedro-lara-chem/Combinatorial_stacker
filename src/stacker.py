import numpy as np
from itertools import product
import os
import argparse
import sys

class CombinatorialStacker:
    def __init__(self, filepaths):
        # Library to store loaded molecules
        self.molecule_library = [] 
        
        # Load all input files
        for fp in filepaths:
            self.add_molecule(fp)
            
    def add_molecule(self, filepath):
        """Reads a standard .xyz file, centers it, and adds it to the library."""
        abs_path = os.path.abspath(filepath)
        filename = os.path.basename(abs_path).replace('.xyz', '')
        
        if not os.path.exists(abs_path):
            print(f"Error: File not found at {abs_path}")
            return 

        atoms = []
        base_coords = []
        
        with open(abs_path, 'r') as f:
            lines = f.readlines()
            if len(lines) < 3:
                print(f"Warning: Skipping {filename} (Invalid format).")
                return

            for line in lines[2:]:
                parts = line.split()
                if len(parts) >= 4:
                    atoms.append(parts[0])
                    base_coords.append([float(parts[1]), float(parts[2]), float(parts[3])])
        
        base_coords = np.array(base_coords)
        
        # Center the molecule
        if len(base_coords) > 0:
            centroid = np.mean(base_coords, axis=0)
            base_coords = base_coords - centroid
            
            self.molecule_library.append({
                'name': filename,
                'atoms': atoms,
                'coords': base_coords
            })
            print(f"Loaded: {filename} ({len(atoms)} atoms)")
        else:
            print(f"Warning: No atoms found in {filename}.")

    def rotate_molecule(self, coords, angle_degrees):
        """Rotates coordinates around the Z-axis."""
        theta = np.radians(angle_degrees)
        c, s = np.cos(theta), np.sin(theta)
        Rz = np.array(((c, -s, 0), (s, c, 0), (0, 0, 1)))
        return np.dot(coords, Rz)

    def generate_combinations(self, num_layers, z_dist, x_dist, rot_step):
        """
        Generates geometries iterating over both MOLECULE ORDER and ROTATIONS.
        Creates a separate sub-directory for each molecule order.
        """
        num_inputs = len(self.molecule_library)
        if num_inputs == 0:
            print("No valid molecules loaded. Exiting.")
            sys.exit(1)

        # 1. Generate Rotation Combinations
        rotation_angles = list(range(0, 360, rot_step))
        rotation_combos = list(product(rotation_angles, repeat=num_layers))

        # 2. Generate Molecule Order Combinations
        molecule_indices = list(range(num_inputs))
        structure_combos = list(product(molecule_indices, repeat=num_layers))

        total_files = len(rotation_combos) * len(structure_combos)
        print(f"\n--- Calculation Details ---")
        print(f"Layers in stack: {num_layers}")
        print(f"Unique input molecules: {num_inputs}")
        print(f"Total geometries to generate: {total_files}")
        
        if total_files > 10000:
            confirm = input(f"Warning: This will generate {total_files} files. Continue? (y/n): ")
            if confirm.lower() != 'y':
                sys.exit(0)

        # Base Output Directory
        cwd = os.getcwd()
        base_output_dir = os.path.join(cwd, "stacked_geometries")
        os.makedirs(base_output_dir, exist_ok=True)
        
        count = 0
        
        # --- OUTER LOOP: MOLECULE ORDER ---
        for mol_order_tuple in structure_combos:
            # 1. Determine the folder name based on the molecules used (e.g., "A-A-B")
            mol_names = [self.molecule_library[i]['name'] for i in mol_order_tuple]
            order_str = "-".join(mol_names)

            # 2. Create the specific directory for this combination
            current_dir = os.path.join(base_output_dir, order_str)
            os.makedirs(current_dir, exist_ok=True)

            # --- INNER LOOP: ROTATIONS ---
            for rotation_tuple in rotation_combos:
                final_atoms = []
                final_coords = []
                rot_str = "_".join(map(str, rotation_tuple))

                for layer_idx in range(num_layers):
                    # Get molecule data
                    lib_index = mol_order_tuple[layer_idx]
                    mol_data = self.molecule_library[lib_index]
                    
                    # Transform
                    current_coords = mol_data['coords'].copy()
                    angle = rotation_tuple[layer_idx]
                    current_coords = self.rotate_molecule(current_coords, angle)
                    
                    translation = np.array([x_dist * layer_idx, 0.0, z_dist * layer_idx])
                    current_coords = current_coords + translation
                    
                    final_atoms.extend(mol_data['atoms'])
                    final_coords.extend(current_coords)

                # Save File inside the specific directory
                # Filename is shorter now: rot_0_30_60.xyz
                fname = f"rot_{rot_str}.xyz"
                full_path = os.path.join(current_dir, fname)
                
                self.save_xyz(full_path, final_atoms, np.array(final_coords), order_str)
                count += 1
                
                if count % 1000 == 0:
                    print(f"Generated {count} / {total_files}...")

        print(f"Done. {count} files saved to {base_output_dir}")

    def save_xyz(self, filename, atoms, coords, comment_info):
        with open(filename, 'w') as f:
            f.write(f"{len(atoms)}\n")
            f.write(f"Stack: {comment_info} | Generated by CombinatorialStacker\n")
            for atom, coord in zip(atoms, coords):
                f.write(f"{atom:<4} {coord[0]:.6f} {coord[1]:.6f} {coord[2]:.6f}\n")

# --- MAIN EXECUTION BLOCK ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stack multiple molecular geometries with combinatorial ordering and rotations.")
    
    # Input files
    parser.add_argument("input_files", nargs='+', help="List of .xyz files to stack")
    
    # Parameters
    parser.add_argument("-n", "--num_layers", type=int, default=2, help="Total height of the stack.")
    parser.add_argument("--z_dist", type=float, default=6.0, help="Vertical distance (Angstroms).")
    parser.add_argument("--x_dist", type=float, default=0.0, help="Horizontal offset (Angstroms).")
    parser.add_argument("--rot_step", type=int, default=30, help="Rotation interval in degrees.")

    args = parser.parse_args()

    try:
        stacker = CombinatorialStacker(args.input_files)
        stacker.generate_combinations(args.num_layers, args.z_dist, args.x_dist, args.rot_step)
        
    except KeyboardInterrupt:
        print("\nProcess interrupted.")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
