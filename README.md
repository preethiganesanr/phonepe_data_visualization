# phonepe_data_visualization

This project aims to create an end-to-end data pipeline that involves fetching data from the Phonepe Pulse Github repository, performing data transformation, inserting it into a MySQL database, creating an interactive dashboard using Python libraries (Streamlit and Plotly), and deploying the dashboard for public access.

## Project Overview

1. **Data Extraction**
   - Use scripting to clone the Phonepe Pulse Github repository.
   - Fetch the data and store it in CSV or JSON format.

2. **Data Transformation**
   - Utilize Python scripting, leveraging Pandas library for data manipulation.
   - Clean, handle missing values, and transform data for analysis and visualization purposes.

3. **Database Insertion**
   - Employ "mysql-connector-python" library to connect to a MySQL database.
   - Use SQL commands to insert the transformed data into the database.

4. **Dashboard Creation**
   - Implement Streamlit and Plotly libraries in Python.
   - Develop an interactive and visually appealing dashboard.
   - Utilize Plotly's geo map functions for spatial data representation.
   - Create user-friendly interfaces with dropdown options for various data views.

5. **Data Retrieval**
   - Connect to the MySQL database using "mysql-connector-python".
   - Fetch data into Pandas dataframe for dynamic updates to the dashboard.

6. **Deployment**
   - Ensure security, efficiency, and user-friendliness of the solution.
   - Thoroughly test the solution.
   - Deploy the dashboard publicly for accessibility to users.

## Usage

1. **Clone the Repository**

2. **Setup**
   - Install necessary Python libraries .
   - Set up a MySQL database and configure credentials in the script.

3. **Running the Scripts**
   - Execute the data extraction, transformation, and database insertion scripts.
   - Launch the Streamlit dashboard script.

4. **Accessing the Dashboard**
   - Access the dashboard via the provided URL after deployment.

## Technologies Used

- Python
- Pandas
- Plotly
- Streamlit
- MySQL
- mysql-connector-python

