# Emergency Reporter

The **Emergency Reporter** is a web application designed to predict and visualize emergency situations based on historical data. The application uses machine learning models to analyze various features such as the type of emergency, location (latitude, longitude), and time-related variables to predict emergency trends. The app also includes data visualization components and interactive maps for real-time reporting.

## Features

- **Data Upload**: Upload historical emergency data in CSV format to start predictions.
- **Prediction**: The application predicts future emergencies based on user-selected parameters such as month.
- **Visualization**: Visualizes data on a map and generates charts.
- **Reports**: Allows downloading of the results as CSV and PDF reports.
- **Interactive Map**: Displays locations of reported emergencies on an interactive map.

## Prerequisites

Before running the application, ensure you have the following installed:

- **Python** (>=3.6)
- **Streamlit**
- **Pandas**
- **Matplotlib**
- **Folium**
- **Scikit-learn**
- **Plotly**

You can install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

The `requirements.txt` file includes the necessary libraries to run the app.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/emergency-reporter.git
   cd emergency-reporter
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   ```

3. Activate the virtual environment:

   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```

   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. To start the app, run the following command:

   ```bash
   streamlit run app.py
   ```

2. Once the app is running, open your browser and navigate to [http://localhost:8501](http://localhost:8501) to interact with the app.

3. **Upload the CSV file** containing emergency data. The file should include the following columns (or a similar structure):

   - `Lat`: Latitude of the emergency location.
   - `Long`: Longitude of the emergency location.
   - `call_type`: Type of emergency (e.g., medical, fire).
   - `description of emergency`: Description of the emergency.
   - `Hour`: Hour of the day when the emergency occurred.
   - `dayofweek`: Day of the week when the emergency occurred.

4. **Set the month** for which you want to predict emergencies.

5. After the prediction is complete, you will have the option to download the results as a CSV or PDF report.

6. You will also see an interactive map displaying the emergency locations.

## Project Structure

```
emergency-reporter/
│
├── app.py             # Main application script
├── requirements.txt   # Python dependencies
├── data/              # Folder containing data files (optional)
│   ├── sample_data.csv
│
├── assets/            # Folder for storing reports and images
│   ├── output.csv
│   └── output.pdf
│
└── README.md          # This file
```

## Sample Data Format

The CSV file should have the following columns:

| Lat   | Long   | call_type | description of emergency | Hour | dayofweek |
|-------|--------|-----------|---------------------------|------|-----------|
| 40.7128 | -74.0060 | Medical  | Heart attack               | 14   | 1         |
| 34.0522 | -118.2437 | Fire     | House fire                 | 16   | 3         |
| ...   | ...    | ...       | ...                       | ...  | ...       |

## Handling Errors

If you encounter any issues with missing columns or incorrect data, the application will show an error message to inform you about the problem. Ensure the CSV file is formatted properly with the correct columns.

If you face any issues running the app, make sure the necessary dependencies are installed, and the data file is correctly formatted.

## Contributing

Feel free to fork the repository, submit pull requests, or raise issues for bugs and feature requests.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.


```

