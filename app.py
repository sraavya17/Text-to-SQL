import streamlit as st
import mysql.connector 
from database import database_schema,execute_query
from main import generate_sql

st.set_page_config(
    page_title = "Text to SQL",
    page_icon = "📝",
    layout = "wide",
    initial_sidebar_state= "expanded"
)

st.title("Text to SQL Assistant Chatbot")
st.markdown("This is a chatbot which can convert your natural language queries into SQL queries and execute them on a database")

st.sidebar.header("Settings")
st.sidebar.markdown("Configure your database connection settings here.")
DB_CONFIG = {
"host" : st.sidebar.text_input("Database Host"),
"user" : st.sidebar.text_input("Database User"),
"password" : st.sidebar.text_input("Database Password", type="password"),
"database" : st.sidebar.text_input("Database Name")
}

if st.sidebar.button("Connect"):
    if not all(DB_CONFIG.values()):
        st.sidebar.error("Please fill in all fields.")
    else:
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            if conn.is_connected():
                st.sidebar.success("Connected to the database successfully")
                tables, schema = database_schema()
                st.sidebar.write("Available Tables:")
                for table in tables:
                    st.sidebar.write(f"- {table}")
        except Exception as e:
            st.sidebar.error(f"Error connecting to the database: {e}")

if 'sql_query' not in st.session_state:
    st.session_state.sql_query = None
if'show_execute' not in st.session_state:
    st.session_state.show_execute = False

nl_query = st.text_input("Enter your natural language query", key="nl_query")
if st.button("Generate SQL Query"):
    with st.spinner("generating..."):
        nl_query = st.session_state.nl_query
        if not nl_query:
            st.error('Please enter a natural language query')
        else:
            try:
                sql_query = generate_sql(nl_query)
                if not sql_query:
                    st.error('Failed to generate SQL query.')
                else:
                    st.session_state.sql_query = sql_query
                    st.session_state.show_execute = True
                    st.markdown("Generated SQL query:")
                    st.code(sql_query, language='sql')
            except Exception as e:
                st.error(f"Error generating SQL query: {e}")

if st.session_state.show_execute and st.session_state.sql_query:
    st.warning("Executing SQL Query can modify your database. Proceed with Caution")
    if st.button('Execute SQL Query'):
        with st.spinner("Executing..."):
            try:
                result = execute_query(st.session_state.sql_query)
                if result["status"] == "success":
                    if "data" in result:  
                        st.dataframe(result["data"])  
                    else: 
                        st.success(f"Query executed. Rows affected: {result['rows_affected']}")
                else:  
                    st.error(f"Execution failed: {result['message']}")
            except Exception as e:
                st.error(f"Error executing SQL query: {e}")






