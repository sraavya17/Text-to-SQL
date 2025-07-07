# 📝 Text to SQL Assistant Chatbot

This project is an **AI-powered chatbot** built using **Streamlit** and **OpenRouter's LLM API**, designed to convert **natural language queries** into executable **MySQL SQL queries**. It allows users to interact with their database using plain English, view schema, generate SQL, and optionally execute the query.

---

## 🔧 Features

- ✅ Convert natural language queries into SQL using LLMs (`deepseek-chat:free` via OpenRouter)
- ✅ View available tables in the connected MySQL database
- ✅ Execute SQL queries directly from the app (with caution warning)

## 🧠 How It Works

- The app first retrieves your database schema using SHOW TABLES and DESCRIBE.
- You enter a natural language query in the Streamlit UI.
- The query and schema are sent to OpenRouter’s deepseek-chat model to generate SQL.
- You can preview and optionally execute the query against the connected MySQL database.

## 📁 Project Structure

.
├── app.py                 
├── main.py                
├── database.py            
├── .env                   
├── requirements.txt       
└── README.md              
