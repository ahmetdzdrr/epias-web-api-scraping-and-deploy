# EPİAŞ Web API Scraping and Deployment

![Screenshot 2024-08-28 at 14 52 30](https://github.com/user-attachments/assets/03dc74bf-fa10-4962-8182-84ca1515745d)


This repository provides a solution to scrape data from the EPİAŞ (Energy Exchange Istanbul) API, process the data, and deploy the results using Docker, GitHub Actions, and Streamlit Cloud.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Running the API Scraper](#running-the-api-scraper)
  - [Deploying the Streamlit Application](#deploying-the-streamlit-application)
- [File Structure](#file-structure)
- [GitHub Actions Workflow](#github-actions-workflow)
- [Docker Deployment](#docker-deployment)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

This project focuses on retrieving data from the EPİAŞ API using a Python script that sends a POST request with a username and password to obtain a ticket key. This key is then used to make further requests to retrieve specific data. The collected data is processed, filtered, and displayed using a Streamlit application. The entire process is automated and deployed using Docker and GitHub Actions.

## Features

- **Data Scraping**: Retrieve data from EPİAŞ API using a secure POST request.
- **Data Filtering**: Filter the retrieved data based on city and district.
- **Automated Deployment**: Use GitHub Actions to schedule the scraping script to run every 24 hours and update the data automatically.
- **Streamlit Integration**: Display the filtered data in a user-friendly manner using a Streamlit application.
- **Dockerized Application**: Containerize the application using Docker for easy deployment and scaling.

## Requirements

- Python 3.8+
- Docker
- GitHub account
- EPİAŞ API credentials (username, password)

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/ahmetdzdrr/epias-web-api-scraping-and-deploy.git
   cd epias-web-api-scraping-and-deploy
   ```

2. **Install the required Python packages**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:

   Create a `.env` file in the root directory and add your EPİAŞ API credentials:

   ```env
   USERNAME=your_username
   PASSWORD=your_password
   ```

## Usage

### Running the API Scraper

To manually run the scraping script:

```bash
python main.py
```

This will fetch the latest data from the EPİAŞ API and save it locally.

### Deploying the Streamlit Application

To run the Streamlit application locally:

```bash
streamlit run streamlit.py
```

The application will be available at `http://localhost:8501`.

## File Structure

```
epias-web-api-scraping-and-deploy/
│
├── .github/workflows/         # GitHub Actions workflow files
├── data/                      # Directory where scraped data is stored
├── Dockerfile                 # Docker configuration file
├── main.py                    # Main script to fetch data from EPİAŞ API
├── requirements.txt           # Python dependencies
├── streamlit.py               # Streamlit application file
└── README.md                  # Project documentation (this file)
```

## GitHub Actions Workflow

The repository includes a GitHub Actions workflow that automatically runs the `main.py` script every 24 hours. The data is fetched and saved to the `data/` directory. The workflow file is located in `.github/workflows/`.

To view or modify the workflow:

```yaml
name: Data Scraping and Deployment

on:
  schedule:
    - cron: "0 0 * * *"  # Runs every 24 hours

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'

    - name: Install dependencies
      run: pip install -r requirements.txt

    - name: Run the scraping script
      run: python main.py
```

## Docker Deployment

The project includes a `Dockerfile` that can be used to containerize the application.

To build and run the Docker container:

```bash
docker build -t epias-web-api .
docker run -p 8501:8501 epias-web-api
```

The Streamlit application will be available at `http://localhost:8501`.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
