
import streamlit as st
import requests
import pandas as pd
from datetime import datetime

API_KEY = 'YOUR_NEWSAPI_KEY'  # Wprowadź swój klucz API z NewsAPI.org

def search_articles(query, start_date, end_date, num_links):
    url = f'https://newsapi.org/v2/everything?q={query}&from={start_date}&to={end_date}&sortBy=publishedAt&pageSize={num_links}&apiKey={API_KEY}'
    response = requests.get(url)
    articles = response.json().get('articles', [])
    results = [{"title": article['title'], "link": article['url']} for article in articles]
    return results

st.title("Wyszukiwarka Artykułów")

query = st.text_input("Temat wyszukiwania")
num_links = st.slider("Liczba linków", min_value=1, max_value=50, value=20)
start_date = st.date_input("Data początkowa")
end_date = st.date_input("Data końcowa")
file_format = st.selectbox("Format pliku", ["csv", "xlsx", "txt"])

if st.button("Szukaj"):
    if start_date > end_date:
        st.write("Data początkowa nie może być późniejsza niż data końcowa.")
    else:
        articles = search_articles(query, start_date, end_date, num_links)
        if articles:
            df = pd.DataFrame(articles)
            st.write(df)
            file_name = f"search_results.{file_format}"
            if file_format == "csv":
                df.to_csv(file_name, index=False)
            elif file_format == "xlsx":
                df.to_excel(file_name, index=False)
            elif file_format == "txt":
                df.to_csv(file_name, index=False, sep='\t')
            with open(file_name, "rb") as file:
                btn = st.download_button(
                    label="Pobierz wyniki",
                    data=file,
                    file_name=file_name,
                    mime="application/octet-stream"
                )
        else:
            st.write("Nie znaleziono wyników.")
