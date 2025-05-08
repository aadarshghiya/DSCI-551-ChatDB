from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import pandas as pd
from sqlalchemy import create_engine, text

app = Flask(__name__, template_folder='templates')

# Initialize Gemini
genai.configure(api_key="YOUR_GEMINI_API_KEY")
model = genai.GenerativeModel("gemini-2.0-flash")

# Database configuration (root connection to list databases)
DB_CONFIG = {
    'username': "your_mysql_username",
    'password': "your_mysql_password",
    'host': "your_ec2_public_dns"
}

def get_db_engine(database=None):
    db_url = f"mysql+pymysql://{DB_CONFIG['username']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/"
    if database:
        db_url += database
    return create_engine(db_url)

@app.route('/')
def home():
    # Get list of databases
    engine = get_db_engine()
    with engine.connect() as connection:
        databases = pd.read_sql("SHOW DATABASES;", connection)
    db_list = databases['Database'].tolist()
    return render_template('index.html', databases=db_list)

@app.route('/query', methods=['POST'])
@app.route('/query', methods=['POST'])
def handle_query():
    try:
        data = request.json
        description = data['query']
        database = data['database']
        
        if not database:
            return jsonify({"status": "error", "message": "Please select a database"})

        # Get database schema information
        engine = get_db_engine(database)
        with engine.connect() as connection:
            # Get table information
            tables = pd.read_sql("SHOW TABLES;", connection)
            schema_info = {}
            for table_name in tables.iloc[:, 0]:
                # Get column information for each table
                columns = pd.read_sql(f"SHOW COLUMNS FROM {table_name};", connection)
                schema_info[table_name] = columns.to_dict('records')
        
        # Generate SQL with more specific instructions
        prompt = f"""
        Convert the following natural language query into a valid SQL query: "{description}". Just remember that the Database schema is shown by {schema_info}. In one line return only the SQL query with the ';' at the end of the output without any additional explanation. The format of the output should be as follows:
        ```sql
        query
        ```
        
        Database schema: {schema_info}
        
        Important rules:
        1. Always include table aliases
        2. Every derived table must have an alias
        3. Use proper JOIN syntax
        4. Return only the SQL query with semicolon at end
        5. Ensure all table references are qualified with aliases
        6. Use concat() whenever you need inplace of ||
        7. Use show tables; when someone asks to name the tables in the database
        8. Format the SQL query with proper indentation and line breaks for readability
        """
        
        q = model.generate_content(prompt)
        query = q.text.strip().strip('```sql').strip('```').strip()
        
        # Add error handling for the SQL execution
        try:
            with engine.connect() as connection:
                if query.lower().strip().startswith('select') or query.lower().strip().startswith('show') or query.lower().strip().startswith('with'):
                    df = pd.read_sql(text(query), connection)
                    results = df.to_dict('records')
                    query_type = "reading"
                else:
                    connection.execute(text(query))
                    connection.commit()
                    results = {"message": "Write operation successful"}
                    query_type = "writing"
                
            return jsonify({
                "status": "success",
                "query_type": query_type,
                "generated_sql": query,
                "results": results
            })
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e),
                "generated_sql": query
            }), 400
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)