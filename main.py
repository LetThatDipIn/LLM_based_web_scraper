import streamlit as st
import pandas as pd
import json
from scrape import structured_scrape
from parse import process_scraped_data

# Streamlit UI 
st.title("Web Scraper")

api_key = ''

# User Input for Website URL
url = st.text_input("Enter Website URL")

if st.button("Scrape and Analyze Data"):
    if url and api_key:
        st.write("🔄 Scraping and analyzing the website...")
        
        # Scrape Website & Extract Structured Data
        structured_data = json.loads(structured_scrape(url))
        
        # Process and enhance the data using LLM with strict rules
        enhanced_data = process_scraped_data(structured_data, api_key)
        
        # Display Raw JSON (for debugging)
        with st.expander("📜 View Data"):
            st.json(enhanced_data)
        
        # Ensure a table is always generated
        if "enhanced_tables" in enhanced_data and enhanced_data["enhanced_tables"]:
            st.subheader("📊 Generated Table:")
            
            for i, enhanced in enumerate(enhanced_data["enhanced_tables"], 1):
                st.write(f"### Table {i}")
                
                if "enhanced_table" in enhanced:
                    df_enhanced = pd.DataFrame(enhanced["enhanced_table"]["data"])
                    st.dataframe(df_enhanced)
                else:
                    st.write("No valid table generated.")
        else:
            st.write("⚠️ No valid table. Please try again with different data.")
    else:
        st.error("Please provide a URL ")