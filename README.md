# SQR Project — Weather

## Project Description

This project is a web application that provides users with weather information, including current weather, forecast, and history. Users can set thresholds for various meteorological parameters and receive notifications when these thresholds are exceeded.

## Key Features

* **User authentication system** — registration and login for users.
* **Weather dashboard** — displaying current weather for a specified location.
* **Alert setup page** — allowing users to configure thresholds for various meteorological parameters (temperature, humidity, pressure, etc.).
* **Notification system** — users receive notifications when weather data exceeds or falls below set thresholds.
* **Basic historical view** — displaying historical weather data for a specified location.

## Project Structure

* **.github/workflows** — CI/CD pipeline configuration.
* **.streamlit** — configuration for the Streamlit app.
* **src** — source code for the application.
* **.coveragerc** — configuration for code coverage.
* **.dockerignore** — files ignored by Docker.
* **.env.example** — example environment file for storing variables (e.g., API keys).
* **.flake8** — configuration for Flake8.
* **.gitignore** — files ignored by Git.
* **Dockerfile** — instructions for building the Docker container.
* **poetry.lock** — Poetry dependency lock file.
* **pyproject.toml** — Poetry configuration for the project.
* **requirements.txt** — list of dependencies for the project.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-repository-url.git
   cd your-repository
   ```

2. Install dependencies:

   Using Poetry:

   ```bash
   poetry install
   ```

3. Create a `.env` file and add the necessary environment variables
  
4. Run the app:

   Using Streamlit:

   ```bash
   streamlit run src/main.py
   ```

## Technologies Used

* **Streamlit** — for creating the user interface.
* **Flake8** — for code analysis and maintaining coding standards.
* **pytest** and **pytest-cov** — for testing and code coverage.
* **Bcrypt** — for password encryption.
* **Requests** — for making API requests.
* **dotenv** — for working with environment variables.
* **McCabe** — for function complexity analysis.
* **Bandit** — for security analysis.

## Requirements

* Python 3.12+
* Poetry for dependency management
* Streamlit for deploying the app
