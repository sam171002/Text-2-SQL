# 🧠 Intelligent Text-to-SQL Chatbot System  
A Natural Language → SQL → Insights Engine

## 📌 Project Overview  
The **Intelligent Text-to-S-SQL Chatbot System** bridges the gap between non-technical users and relational databases.  
It allows users to interact with structured data using **plain English**, automatically converting natural language queries into **syntactically and semantically correct SQL statements**, executing them, and visualizing results — all through a clean, web-based interface.

This project demonstrates the integration of **LLM-powered reasoning**, **backend microservices**, **database querying**, and **modern cloud deployment** using Azure Web App Services.

---

## ✨ Features  
- 🔍 Query complex datasets using natural language  
- 🤖 LLM-powered SQL generation (Gemini 2.5 Flash)  
- 🧩 Schema-aware SQL creation with validation & safety  
- 📊 Dynamic visualizations (bar charts, tables, insights)  
- 📥 Downloadable results in CSV format  
- ⚙ Modular microservices architecture  
- ☁ Cloud deployment on **Azure Web App**  
- 🔒 Secure configuration using environment variables   

---

## 🏗 Architecture Overview  

The system follows a **modular microservices architecture**, ensuring scalability, clarity, and maintainability.

### **📚 Layered Architecture**

| Layer | Components | Technologies |
|-------|------------|--------------|
| **User Interface** | Streamlit frontend | Python, Streamlit |
| **API Layer** | Backend REST endpoints, JWT auth | FastAPI, Uvicorn |
| **NLU Layer** | Intent parsing, entity extraction | spaCy, Transformers |
| **SQL Generation** | Query generation, LLM calls, validation | Gemini 2.5 Flash, SQL parser |
| **Data Layer** | Database operations, caching | SQLite |
| **Cloud Infrastructure** | Hosting & deployment | Azure Web App Service |

---

## 🔄 End-to-End Data Flow  

1. **User Input**  
   - User enters a natural-language question in the Streamlit UI.

2. **API Call**  
   - Query is sent to FastAPI endpoint via REST.

3. **NLU Processing**  
   - Intent & entities are parsed from input text.

4. **SQL Generation**  
   - Gemini LLM converts parsed intent → SQL query.  
   - Schema info (JSON) ensures correctness.

5. **SQL Validation**  
   - Query syntax & table-column mapping verified.

6. **Query Execution**  
   - SQLite database executes the validated SQL.

7. **Result Formatting**  
   - Result returned as a dataframe-friendly structure.

8. **Visualization**  
   - Streamlit shows tables, insights, and Plotly graphs.

9. **Optional Export**  
   - User downloads results as a CSV.

---

## 🧰 Technology Stack  

### **Frontend**  
- Streamlit  
- Python  
- Plotly  
- Pandas  

### **Backend**  
- FastAPI  
- Uvicorn  
- Pydantic  
- SQLAlchemy  
- Python  

### **Machine Intelligence (GenAI)**  
- **Google Gemini 2.5 Flash** for text-to-SQL generation  
- Schema-aware prompting  
- Intent parsing & error correction  

### **Utilities**  
- python-dotenv  
- Requests  
- JSON schema ingestion  

### **Cloud**  
- Azure Web App (Backend)  
- Azure Web App (Frontend)  


---

## 🧪 Dataset Overview  

This project uses a **Cancer dataset** with:  
- **483 rows**  
- **17 columns**  
- Mixed data types: numerical, categorical, datetime  

### **Key Columns**  
- PatientID  
- EncounterID  
- Diagnosis Code  
- Cancer Category  
- Gender  
- Specialty  
- Age Group  
- Readmission  
- Encounter Dates  

### 📊 **Analytical Insights**  
1. Gender distribution is nearly equal across all encounters.  
2. Only **8%** of patients are readmitted (class imbalance exists).  
3. Age group **35–54** shows highest cancer detection frequency.  
4. Average **Length of Stay (LOS)** ≈ 3 hours.  
5. **Oncology** contributes to **60%+** of total encounters.  
6. Seasonal admission peaks observed in **Q3 & Q4**.  

---

## 🏁 Results

The Intelligent Text-to-SQL Chatbot successfully converts natural language queries into accurate SQL, executes them on SQLite, and returns interactive tables, charts, and downloadable CSVs.  
The system uses a Streamlit frontend, FastAPI backend, and Gemini 2.5 Flash for SQL generation.

### 🔹 Key Achievements
- End-to-end working Text-to-SQL pipeline  
- Conversational memory across user queries  
- Schema-aware SQL generation with validation  
- Interactive data visualization (Plotly)  
- Fully deployed on Azure Web App Services  

---

## 🔎 Example Questions Users Can Ask

### 📊 Data Insights
- “How many patients were diagnosed with cancer?”
- “Show average LOS by age group.”
- “What is the gender distribution?”

### 📅 Trends & Time Analysis
- “Show monthly admissions.”
- “Which quarter has the most encounters?”

### 🧬 Clinical & Demographic Queries
- “Which diagnosis category is most common?”
- “Readmission rate for each specialty?”

### 🔥 Filters & Comparisons
- “Show patients above 50 with breast cancer.”
- “Compare LOS for males vs females.”

### 🛠 Dataset Exploration
- “List all column names.”
- “Show summary statistics.”

---

## 🧪 Demo Flow
1. Open the Streamlit UI  
2. Enter a natural-language question  
3. View SQL + results + charts  
4. Download CSV if needed  

---
