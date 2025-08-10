import streamlit as st
import pandas as pd
import sqlite3

st.title("🎬 Box Office Analytics")

conn = sqlite3.connect("collections.db")
df = pd.read_sql_query("SELECT * FROM movie_collections", conn)
conn.close()

st.dataframe(df)

csv = df.to_csv(index=False)
st.download_button("📥 Download CSV", data=csv, file_name="collections.csv", mime="text/csv")

trending = df.groupby("movie_name")["estimated_collection"].sum().sort_values(ascending=False).head(5)
st.subheader("🔥 Trending Movies")
st.bar_chart(trending)
