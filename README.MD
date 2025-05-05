# Natural Language to SQL Query Application

This application allows users to input natural language queries and retrieve corresponding SQL queries, along with the results from executing those queries against a specified database. It leverages the Gemini API for natural language to SQL conversion and Flask for the web interface.

## Prerequisites

Before you begin, ensure you have the following installed and configured:

1.  **Python 3.x:** Python is required to run the Flask application. You can download it from the official Python website: [https://www.python.org/downloads/](https://www.python.org/downloads/). The project was tested on Python 3.12.2

2.  **pip:** Python's package installer. It usually comes with Python installations. You might need to upgrade it using:

    ```bash
    pip install --upgrade pip
    ```

3.  **MySQL Server:** You need a running MySQL server instance to connect to. If you don't have one, you can download and install MySQL Community Server from: [https://dev.mysql.com/downloads/mysql/](https://dev.mysql.com/downloads/mysql/)

4.  **Gemini API Key:** You'll need an API key from Google's Gemini to use the natural language processing capabilities.  Obtain your API key from the Google Cloud Console or the appropriate Google AI platform.  **Replace `"enter Gemini API Key"` in the `app.py` file with your actual API key.**

5.  **Python Packages:** Install the required Python packages using pip:

    ```bash
    pip install Flask pandas sqlalchemy pymysql google-generativeai
    ```

## Installation and Setup

Follow these steps to set up and run the application:

1.  **Configure Database Connection:**

    * Open the `app.py` file and update the `DB_CONFIG` dictionary with your MySQL database credentials:

        ```python
        DB_CONFIG = {
            'username': "your_mysql_username",  # e.g., "root"
            'password': "your_mysql_password",  # e.g., "your_secret_password"
            'host': "your_ec2_public_dns",
        }
        ```

    * Ensure your MySQL server is running and accessible from where you are running the python script. If your MySQL server is on an EC2 instance, ensure that the security groups allow connections from your machine.

2.  **Set Gemini API Key:**

    * In the `app.py` file, replace `"enter Gemini API Key"` with your actual Gemini API key:

        ```python
        genai.configure(api_key="YOUR_GEMINI_API_KEY")
        ```

3.  **Run the Application:**

    * Open a terminal in the directory where `app.py` is located and run the Flask application:

        ```bash
        python app.py
        ```

    * The application should start, and you'll see output similar to:

        ```
        * Serving Flask app "app"
        * Debug mode: on
          WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
        * Running on [http://127.0.0.1:5000/](http://127.0.0.1:5000/) (Press CTRL+C to quit)
        * Restarting with watchdog (fsevents)
        * Debugger is active!
        * Debugger PIN: xxx-xxx-xxx
        ```

4.  **Access the Application:**

    * Open your web browser and go to `http://127.0.0.1:5000/`.

## Usage

1.  **Select Database:** Choose the database you want to query from the dropdown menu. The dropdown will be populated with the databases available on your MySQL server.

2.  **Enter Query:** Type your natural language query into the text area.  For example: "Show me all customers named John" or "Create a table called 'orders' with columns 'id' and 'product'."

3.  **Get SQL Query and Results:** Click the "Submit Query" button.

4.  **View Results:** The generated SQL query and the results (or a success/error message for write operations) will be displayed below the button.

## Error Handling

The application includes error handling to manage issues such as:

* Invalid database selection.
* Errors in the natural language to SQL conversion by the Gemini API.
* Errors during SQL query execution (e.g., syntax errors, table not found).
* Connection errors to the database.

Error messages are displayed in the web interface to help users understand and resolve issues.

## Important Notes

* **EC2 Setup:** If you are running your MySQL server on an EC2 instance, ensure that the security group associated with the instance allows inbound traffic on the MySQL port (default 3306) from your machine or the machine running the Flask application.
