from flask import Flask, render_template, request, jsonify, redirect, url_for
from quantum_simulator import run_adiabatic_simulation

app = Flask(__name__)


MOLECULE_DATA = {
    "H2O": {
        "formula": "H₂O",
        "name": "Water",
        "structure": "Bent",
        "properties": {
            "bond_angle": "104.5°",
            "dipole_moment": "1.85 D",
            "boiling_point": "100°C",
            "molar_mass": "18.015 g/mol"
        },
        "drug_relevance": [
            "Universal solvent for drug formulations",
            "Crucial for drug absorption and distribution",
            "Key component in drug stability studies"
        ],
        "expected_energy": "-76.4 eV"
    },
    "CO2": {
        "formula": "CO₂",
        "name": "Carbon Dioxide",
        "structure": "Linear",
        "properties": {
            "bond_angle": "180°",
            "dipole_moment": "0 D",
            "sublimation_point": "-78.5°C",
            "molar_mass": "44.009 g/mol"
        },
        "drug_relevance": [
            "Used in supercritical fluid extraction for drug purification",
            "pH adjustment in drug formulations",
            "Propellant in pharmaceutical aerosols"
        ],
        "expected_energy": "0 eV"
    },
    
    "O2": {
        "formula": "O₂",
        "name": "Oxygen",
        "structure": "Diatomic",
        "properties": {
            "bond_order": "2",
            "dipole_moment": "0 D",
            "boiling_point": "-183°C",
            "molar_mass": "31.999 g/mol"
        },
        "drug_relevance": [
            "Critical in oxidative drug metabolism studies",
            "Used in oxygen therapy as a pharmaceutical gas",
            "Important in aerobic fermentation for drug production"
        ],
        "expected_energy": "-76.4 eV"
    },
    "CO": {
        "formula": "CO",
        "name": "Carbon Monoxide",
        "structure": "Linear",
        "properties": {
            "bond_length": "1.128 Å",
            "dipole_moment": "0.122 D",
            "boiling_point": "-191.5°C",
            "molar_mass": "28.010 g/mol"
        },
        "drug_relevance": [
            "Studied as a potential therapeutic gas in low doses",
            "Used in organometallic chemistry for drug synthesis",
            "Important in understanding hemoglobin interactions"
        ],
        "expected_energy": "-76.4 eV"
    },
    "NO": {
        "formula": "NO",
        "name": "Nitric Oxide",
        "structure": "Linear",
        "properties": {
            "bond_order": "2.5",
            "dipole_moment": "0.159 D",
            "boiling_point": "-151.7°C",
            "molar_mass": "30.006 g/mol"
        },
        "drug_relevance": [
            "Signaling molecule in cardiovascular drug development",
            "Studied for its role in neurotransmission",
            "Used in the development of vasodilators"
        ],
        "expected_energy": "-76.4 eV"
    },
    "CH4": {
        "formula": "CH₄",
        "name": "Methane",
        "structure": "Tetrahedral",
        "properties": {
            "bond_angle": "109.5°",
            "dipole_moment": "0 D",
            "boiling_point": "-161.5°C",
            "molar_mass": "16.043 g/mol"
        },
        "drug_relevance": [
            "Model compound for studying hydrophobic interactions in drug binding",
            "Used as a starting material in organic synthesis for pharmaceuticals",
            "Relevant in understanding anaerobic metabolism of certain drugs"
        ],
        "expected_energy": "-76.4 eV"
    }
}


@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    results = []
    for key, data in MOLECULE_DATA.items():
        if key.lower().startswith(query) or data['name'].lower().startswith(query):
            results.append({
                "key": key,
                "name": data['name'],
                "formula": data['formula']
            })
    return jsonify(results)


@app.route('/')
def index():
    return render_template('index.html', molecules=MOLECULE_DATA.keys())

@app.route('/analyze', methods=['POST'])
def analyze():
    molecule = request.form['molecule']
    return redirect(url_for('loading', molecule=molecule))

@app.route('/loading')
def loading():
    molecule = request.args.get('molecule')
    return render_template('loading.html', molecule=molecule)

@app.route('/results')
def results():
    molecule = request.args.get('molecule')
    data = MOLECULE_DATA[molecule]
    #expected = run_adiabatic_simulation(molecule)
    return render_template('results.html',
                           molecule=molecule,
                           formula=data['formula'],
                           ground_state=data['expected_energy'],
                           data=data)

if __name__ == '__main__':
    app.run(debug=True)
