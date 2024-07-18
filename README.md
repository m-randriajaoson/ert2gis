# ERT to GIS GeoJSON

This Streamlit application converts Electrical Resistivity Tomography (ERT) data into GIS-compatible GeoJSON format. GeoJSON is a popular format for encoding a variety of geographic data structures, making it suitable for integration with GIS software and web mapping applications.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Support](#support)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Electrical Resistivity Tomography (ERT) is a geophysical imaging technique used to create cross-sectional images of subsurface structures. This Streamlit app facilitates the conversion of ERT data into GeoJSON, which can be visualized and analyzed using GIS software like QGIS, ArcGIS, or web mapping libraries.

## Features

- **File Upload**: Upload ERT data files in supported formats.
- **Data Conversion**: Convert uploaded ERT data into GeoJSON format.
- **Visualization**: Display converted data on an interactive map within the app.
- **Export**: Option to download the converted GeoJSON file for further use.

## Getting Started

### Prerequisites

Ensure you have the following installed on your system:

- Python 3.7+
- pip (Python package installer)

### Installation

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd <repository_directory>
    ```
2. Install Dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Usage

1. Start the Streamlit app:
    ```bash
    streamlit run app.py
    ```

2. Upload your ERT data file(s) using the file uploader in the app.

3. Wait for the app to process and convert the data to GeoJSON format.

4. Once conversion is complete, view the converted data on the interactive map within the app.

5. Optionally, download the GeoJSON file for use with GIS software or web mapping applications.

### Support
For any issues or questions, please open an issue on GitHub.

### Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your improvements.

### License
This project is licensed under the MIT License.