# 🌡️ ThermoSim: Non-Flow Process Calculator

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

**ThermoSim** is a full-stack engineering application designed to calculate, simulate, and store thermodynamic data for non-flow (closed system) processes. 

By integrating standard thermodynamic formulas (e.g., $Q - W = \Delta U$) with comprehensive steam table datasets, this tool allows engineers and students to easily evaluate state changes, calculate work done, and determine heat transfer in closed systems.

---

## ✨ Key Features
* **Thermodynamic Property Lookups:** Automatically retrieves properties (enthalpy, entropy, specific volume) using the integrated `steam_table.csv` dataset.
* **Process Calculations:** Supports calculations for standard non-flow processes (Isobaric, Isochoric, Isothermal, Adiabatic, and Polytropic).
* **Full-Stack Architecture:** Cleanly decoupled architecture with a dedicated Python backend API and a dynamic frontend UI.
* **Persistent Storage:** Saves calculation histories and process states using a SQLite database (`thermosim.db`).

---

## 📂 Repository Structure

The project is structured to separate the API logic, data layers, and user interface:

```text
ThermoSim-Non-Flow-Process-Calculator/
│
├── backend/               # Backend API and Database Logic
│   ├── crud.py            # Database Create, Read, Update, Delete operations
│   ├── database.py        # Database connection and engine configuration
│   ├── main.py            # Main API application routing
│   ├── models.py          # Database table models/schemas
│   └── utils.py           # Helper functions and core math logic
│
├── data/                  
│   └── steam_table.csv    # Dataset for thermodynamic properties lookup
│
├── frontend/              
│   └── app.py             # User interface application (e.g., Streamlit/Dash)
│
├── thermosim.db           # SQLite Database file
├── start.sh               # Shell script to boot both frontend and backend
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation


🚀 Installation & Setup
To run this project locally, you need Python installed on your machine.

1. Clone the repository:

Bash
git clone [https://github.com/emmanuel2021-guru/ThermoSim-Non-Flow-Process-Calculator.git](https://github.com/emmanuel2021-guru/ThermoSim-Non-Flow-Process-Calculator.git)
cd ThermoSim-Non-Flow-Process-Calculator
2. Create a virtual environment (Recommended):

Bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
3. Install dependencies:

Bash
pip install -r requirements.txt
4. Run the application:
You can quickly boot up both the backend and frontend using the provided shell script:

Bash
chmod +x start.sh
./start.sh
(Alternatively, you can manually start the backend server and the frontend app in separate terminal windows depending on your specific framework.)

🛠️ Tech Stack
Language: Python

Backend: REST API Architecture (main.py)

Database: SQLite (thermosim.db), ORM Models

Data Integration: CSV parsing for thermodynamic lookup tables

🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

📝 License
This project is MIT licensed.
