# Mariner Project

This is the top level Arches project for the Marine HER system.

## Installing for Development

For development purposes, either use the instructions for developing an Arches project or use the arches-containers configuration included in this repository.

- **For development using included arches-container configuration:**
  

  This repository includes an `arches-containers` project configuration, so you can import, activate, and start the system as follows:

  1. Ensure Docker is installed and running.
  2. Navigate to your workspace directory (the root where your projects and containers live).
  3. Set up a virtual environment
  4. Clone the repository

     ```bash
     git clone https://github.com/HistoricEngland/mariner-proj.git
     ```

  5. Import the arches-container project configuration:

     ```bash
     act import -p mariner-proj
     ```

  4. Activate the project:

     ```bash
     act activate -p mariner-proj
     ```

  5. Start the system:

     ```bash
     act up
     ```

  6. Once setup and webpack builds are complete, open a browser and navigate to `http://localhost:8002` or use `act view` in a terminal to open the project in your default browser.

  For more details, see the [arches-containers documentation](../arches-containers/readme.md).
