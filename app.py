from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Atomic masses of elements (you can add more as needed)
atomic_masses = {
    "H": 1.008, "He": 4.0026, "Li": 6.94, "Be": 9.0122, "B": 10.81, "C": 12.01, "N": 14.01, "O": 16.00, "F": 18.998, "Ne": 20.18,
    "Na": 22.99, "Mg": 24.305, "Al": 26.982, "Si": 28.085, "P": 30.974, "S": 32.06, "Cl": 35.45, "Ar": 39.95, "K": 39.10, "Ca": 40.08,
    "Sc": 44.956, "Ti": 47.867, "V": 50.942, "Cr": 52.00, "Mn": 54.938, "Fe": 55.845, "Co": 58.933, "Ni": 58.693, "Cu": 63.546, "Zn": 65.38,
    "Ga": 69.723, "Ge": 72.63, "As": 74.922, "Se": 78.971, "Br": 79.904, "Kr": 83.798, "Rb": 85.468, "Sr": 87.62, "Y": 88.906, "Zr": 91.224,
    "Nb": 92.906, "Mo": 95.95, "Tc": 98, "Ru": 101.07, "Rh": 102.91, "Pd": 106.42, "Ag": 107.87, "Cd": 112.41, "In": 114.82, "Sn": 118.71,
    "Sb": 121.76, "Te": 127.60, "I": 126.90, "Xe": 131.29, "Cs": 132.91, "Ba": 137.33, "La": 138.91, "Ce": 140.12, "Pr": 140.91, "Nd": 144.24,
    "Pm": 145, "Sm": 150.36, "Eu": 151.96, "Gd": 157.25, "Tb": 158.93, "Dy": 162.50, "Ho": 164.93, "Er": 167.26, "Tm": 168.93, "Yb": 173.05,
    "Lu": 174.97, "Hf": 178.49, "Ta": 180.95, "W": 183.84, "Re": 186.21, "Os": 190.23, "Ir": 192.22, "Pt": 195.08, "Au": 196.97, "Hg": 200.59,
    "Tl": 204.38, "Pb": 207.2, "Bi": 208.98, "Po": 209, "At": 210, "Rn": 222, "Fr": 223, "Ra": 226, "Ac": 227, "Th": 232.04, "Pa": 231.04,
    "U": 238.03, "Np": 237, "Pu": 244, "Am": 243, "Cm": 247, "Bk": 247, "Cf": 251, "Es": 252, "Fm": 257, "Md": 258, "No": 259, "Lr": 262,
    "Rf": 267, "Db": 270, "Sg": 271, "Bh": 270, "Hs": 277, "Mt": 278, "Ds": 281, "Rg": 282, "Cn": 285, "Nh": 286, "Fl": 289, "Mc": 290,
    "Lv": 293, "Ts": 294, "Og": 294
}

# Function to calculate the molar mass of a given chemical formula
def calculate_molar_mass(formula):
    elements = re.findall(r'([A-Z][a-z]*)(\d*)', formula)
    molar_mass = 0.0
    for element, count in elements:
        if element not in atomic_masses:
            raise ValueError(f"Unknown element: {element}")
        count = int(count) if count else 1
        molar_mass += atomic_masses[element] * count
    return molar_mass

# Function to expand the empirical formula based on a multiplier
def expand_formula(formula, multiplier):
    elements = re.findall(r'([A-Z][a-z]*)(\d*)', formula)
    expanded = ""
    for element, count in elements:
        count = int(count) if count else 1
        expanded += f"{element}{int(count * multiplier)}"
    return expanded

# Route to calculate the molecular formula based on empirical formula and molecular mass
@app.route('/calculate-molecular-formula', methods=['GET'])
def calculate_molecular_formula():
    empirical_formula = request.args.get('empiricalFormula')
    molecular_mass = float(request.args.get('molecularMass'))  # Get molecular mass from the user input

    if not empirical_formula or not molecular_mass:
        return jsonify({"error": "يرجى إدخال الصيغة الأولية والكتلة الجزيئية"}), 400

    try:
        empirical_mass = calculate_molar_mass(empirical_formula)
        
        # Calculate the ratio between molecular mass and empirical mass
        ratio = round(molecular_mass / empirical_mass)
        molecular_formula = expand_formula(empirical_formula, ratio)

        return jsonify({
            "empiricalMass": empirical_mass,
            "molecularMass": molecular_mass,
            "ratio": ratio,
            "molecularFormula": molecular_formula
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
