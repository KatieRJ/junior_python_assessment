1.	HOW TO RUN THE APPLICATION

Firstly, make sure these are installed:
- Python
- Code editor E.g. VS Code

Step 1:
Open the project folder called junior_python_assessment in your code editor.

Step 2:
I strongly suggest creating a virtual environment for the project by using the following command in the terminal:
``` python -m venv .venv ```

Step 3:
To activate the virtual environment you can use the following command line:
```  .venv\Scripts\Activate.ps1 ```

Note: After this step, the terminal should show (.venv) at the beginning of the line.

Step 4:
Install all required dependencies from requirements.txt by using the following command line:
``` pip install -r requirements.txt ```

Note: Because virtual environment was created beforehand, these dependencies will be installed inside the project only. 

Step 5:
Set up the database by running setup script. Use the following command line in the terminal:
``` python -m app.setup_db ```
This script will create the SQLite database file, including the tables, and load the CSV files.

Note: After running this script, a database file called customer_orders.db should appear.

Step 6:
Start the API by running the following command line:
``` uvicorn app.api:app --reload ```

Note: After running this command, the terminal should show a message like this: “ Uvicorn running on http://127.0.0.1:8000 “

Step 7:
Next, open the API in browser by using this address http://127.0.0.1:8000/docs  . The endpoint can be tested from here and it uses FastAPI Swagger documentation page. Alternatively, you can also use http://127.0.0.1:8000/customers/20 , replacing the last number with the customer you wish to see. 

Step 8:
To test the customer endpoint, on the Swagger page, click on the little arrow on the left in the “ GET/customers/ {customer_id} ” line. Next, click on “Try it out”, specify which customer ID you wish to inspect and click “ Execute “ .  This should show the information about the customer and their order/s. 

Note: To stop the API, press CTRL + C in the terminal. 

Step 9:
Next, to run the export script, use the following command line:
``` python -m app.etl_export ```
This script looks for the active customers in the database, adds their order information, transforms the data and exports the results to a csv file in the output folder.

Note: The output csv file should look like this “ Active_Customer_Orders_YYYY-MM-DD.csv “. 

Step 10:
The database setup script can be run multiple times without it creating any duplicate records. To test this, run the following command again:
``` python -m app.setup_db ```
There should be no errors and no duplicate rows. To confirm everything still works correctly, run the export script again:
``` python -m app.etl_export ```
and check the CSV file to make sure the exported data looks correct.  



2. CHOICES AND REASONING

For this task, my goal was to build a small API with a database and an export process. I tried to keep the design simple but still follow common Python practices and widely used libraries.

-	Framework Choice

For the API, I chose FastAPI. I made this decision because FastAPI’s official documentation describes this framework as widely used for building APIs in Python and has become very popular in recent years. One of the main reasons for choosing FastAPI is its high performance and simplicity. FastAPI is considered one of the fastest Python frameworks available for building APIs. 
Another useful feature and a reason I chose FastAPI, is that it automatically generates interactive documentation (Swagger/OpenAPI). This makes it much easier to test endpoints and understand how the API works without needing additional tools. 

-	Library Choices
  
For database interaction I used SQLAlchemy because SQLAlchemy allowed me to represent database tables as Python classes and interact with them using Python objects, instead of writing raw SQL queries. This approach keeps the code more readable and easier to maintain. Importantly, it also supports multiple database systems, which makes it flexible if the database needs to change later. 

To run the API locally, I used Uvicorn. Uvicorn is an ASGI web server for Python, and FastAPI commonly runs on top of it. I used it because it is simple to start from the command line and supports reload mode for local development, which I found useful when testing changes.

I also used Pydantic, through FastAPI, for the response models. Pydantic is commonly used for validation and serialization based on Python type hints. I chose it because it helped me define a clear response structure for the customer endpoint and made the API documentation cleaner.

-	SQLite Database

For this project I used SQLite as the database. I chose SQLite because it requires no external database server and it is convenient to set up locally. Since the goal of this task was to demonstrate functionality rather than production deployment, I chose SQLite because it keeps the setup simple while still allowing the use of SQL.
Another reason I decided to use SQLite is that it lets me demonstrate relational database design properly, including separate customers and orders tables and a relationship between them. I felt this was enough for the scope of the task without adding unnecessary complexity.

-	Main decisions I had to make

Firstly, I had to decide how to structure this project. I decided to break it into small modules inside the app folder.
This separation helped me keep responsibilities of the modules clear:
1.	models.py → responsible for database tables
2.	db.py → responsible for database connection
3.	setup_db.py → responsible for database setup and data loading
4.	api.py → responsible for API endpoints
5.	etl_export.py → responsible for export/ETL script

This structure makes the project easier to maintain and extend later.

Another decision I had to make was how much data to include in the schema. I kept the structure simple and included the required fields, plus a small number of extra fields such as phone_number and country, because they made the sample data feel more realistic without making the database too complicated. 

Next decision was how to make the database setup script repeatable. The brief says the script should be able to run again without causing duplicates or errors. To handle this, I chose to check whether each customer or order already existed before inserting it. That way, the script can be run multiple times safely and makes it easier to reset or rebuild the database during development and testing.

I also decided to write the export script so that it follows a simple ETL pattern:
1.	Extract data from the database
2.	Transform the data (combine customer and order information, calculate the total cost)
3.	Load the result into a CSV file

Each order is exported as one row in the CSV file. This structure keeps the dataset easy to analyse and process later.

I also named the export file so that it also includes the current date in the file name. This way multiple exports can exist without overwriting previous files and provides clarity on when the file was generated.

Finally, I chose to use snake_case for file naming in the final version of the project because that is the common naming style in Python projects and keeps file names simple and consistent. I also added small comments in the code to explain what each main block does. I tried to keep these comments simple and focused on explaining the purpose of the code rather than describing every line. The goal was to make the scripts easier to read and understand for someone reviewing the project or running it for the first time.



3. APPLICATION FLOW

This application has three main stages:
1.	sample data is stored in CSV files
2.	the CSV data is loaded into the SQLite database
3.	the database is then used by both the API and the export script

The overall flow is:
data.csv → setup_db.py → customer_orders.db → api.py / etl_export.py → output CSV file

Data Loading:
The project includes two sample data files located in the data folder (customers.csv and orders.csv). These files contain the initial dataset used by the application. The orders.csv file references customers using the customer_id field, which creates the relationship between customers and their orders.

Next, the setup script is run using:
``` python -m app.setup_db ```
This script creates the SQLite database (customer_orders.db), creates the required tables (customers and orders), and loads the data from the CSV files into the database. Before inserting records, the script checks whether a customer or order already exists. This allows the script to be run multiple times without creating duplicate records.

API Flow:
The API is implemented in api.py and is started with:
``` uvicorn app.api:app --reload ```
The main endpoint is: /customers/{customer_id}.
When this endpoint is called, the API:
1.	receives the customer ID from the request
2.	queries the database for that customer
3.	loads all orders linked to that customer
4.	returns the customer information together with their orders as a JSON response
If the customer does not exist, the API returns a 404 error.

Export Script Flow:
The export script is run using:
``` python -m app.etl_export ```
This script performs a simple ETL process:
1.	Extract active customers from the database
2.	Transform the data by combining customer details with their orders and calculating the total order value (quantity × unit_price)
3.	Load the result into a CSV file in the output folder
Each order becomes one row in the export file. And the generated file follows this format: Active_Customer_Orders_YYYY-MM-DD.csv
This prevents previous exports from being overwritten.

4. WHAT I WOULD IMPROVE
While the current implementation meets the requirements of the task, there are a few improvements I would make.

First, I would add input validation for data loading. Currently the CSV loading process assumes the input data is valid. In a real world scenario, I would add stronger validation when reading the CSV files. For example, checking for missing values and incorrect data types. This would help prevent invalid data from being inserted into the database.

Second, I would add basic automated tests for the API and database logic. For example, tests that confirm the API returns the correct customer data or that the setup script loads the expected number of records.


Lastly, for larger datasets, the current export process might become slower because it loads all results into memory before writing them to the CSV file. A possible improvement would be streaming the results directly to the file.




