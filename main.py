import os
from dotenv import load_dotenv
import requests
import json
from database import database_schema, execute_query

load_dotenv()

def generate_sql(nl_query):
    """Generate SQL query from natural language using OpenRouter's API"""
    tables,schema = database_schema()
    prompt = f"""
            This is the schema:

            {schema}

            Convert the following natural language query into a syntactically correct MySQL SQL query:
            "{nl_query}"

            Do not include any explanation. Only return the SQL query without wrapping it in markdown.
            """

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.getenv('API_KEY')}",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": "deepseek/deepseek-chat:free",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
            }),
            timeout=30
        )
        response.raise_for_status()
        response_data = response.json()
        return response_data['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error generating SQL: {e}")
        return None
    
def main():
    """Main function"""
    tables,schema = database_schema()
    print(f"Available Tables:{tables}")
    nl_query = input("Enter your query:")
    sql_query = generate_sql(nl_query)
    if not sql_query:
        print("Failed to generate SQL query.")
    else:
        print(f"Generted SQL query: {sql_query}")
        if sql_query.startswith('```sql'):
            sql_query = sql_query.replace("```sql","").replace("```","")
    try:
        result = execute_query(sql_query)
        if result['status'] == 'success':
            print('Query Executed Successfully')
            print(result)
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()


    