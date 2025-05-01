import streamlit as st
import pandas as pd
import numpy as np
import random
from sklearn.cluster import KMeans
from datetime import datetime, timedelta
import folium
from folium.plugins import MarkerCluster
from fpdf import FPDF
import os


# Function to run the prediction model
def predict_emergencies(uploaded_csv, num_months):
    # Step 1: Read uploaded CSV
    df = pd.read_csv(uploaded_csv)

    # Step 2: Preprocess
    rename_mapping = {
        'addr': 'Address',
        'call_type': 'call_type',
        'date': 'date',
        'dayofweek': 'dayofweek',
        'desc': 'Description',
        'description_of_emergency': 'description of emergency',
        'h3_cell': 'h3_cell',
        'hour': 'Hour',
        'lat': 'Lat',
        'lng': 'Long',
        'month': 'Month',
        'timeStamp': 'timeStamp',
        'title': 'title',
        'twp': 'twp',
        'year': 'Year',
        'zip': 'Zip Code'
    }
    df = df.rename(columns=rename_mapping)

    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['timeStamp'] = pd.to_datetime(df['timeStamp'], errors='coerce')

    # Step 3: Prepare data for clustering
    data = df[['Lat', 'Long', 'call_type', 'description of emergency', 'Hour', 'dayofweek']].copy()
    kmeans = KMeans(n_clusters=20, random_state=42)
    data['cluster'] = kmeans.fit_predict(data[['Lat', 'Long']])
    call_type_distribution = data['call_type'].value_counts(normalize=True)

    # Step 4: Generate date range dynamically based on months entered
    start_date = datetime(2020, 8, 1)  # starting point (adjust if needed)
    end_date = start_date + pd.DateOffset(months=num_months) - timedelta(days=1)
    dates_range = pd.date_range(start_date, end_date)

    # Step 5: Simulate future data
    predicted_data = []
    num_samples = 3000 * num_months  # Increase samples with months

    for _ in range(num_samples):
        date = random.choice(dates_range)
        cluster_id = random.choice(data['cluster'].unique())

        center_lat, center_lng = kmeans.cluster_centers_[cluster_id]
        lat = center_lat + np.random.normal(0, 0.005)
        lng = center_lng + np.random.normal(0, 0.005)

        call_type = np.random.choice(call_type_distribution.index, p=call_type_distribution.values)
        desc_options = df[df['call_type'] == call_type]['description of emergency']
        if not desc_options.empty:
            desc = random.choice(desc_options.tolist())
        else:
            desc = "General Emergency"

        predicted_data.append([date.strftime('%Y-%m-%d'), lat, lng, call_type, desc])

    output_df = pd.DataFrame(predicted_data, columns=['date', 'lat', 'lng', 'call_type', 'description of emergency'])

    # Step 6: Save CSV
    output_csv_path = 'predicted_emergencies.csv'
    output_df.to_csv(output_csv_path, index=False)

    # Step 7: Convert CSV to PDF
    pdf_path = 'predicted_emergencies.pdf'
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=8)
    # Add headings
    col_width = pdf.w / 5
    row_height = pdf.font_size * 1.5

    # Write headers
    for header in output_df.columns:
        pdf.cell(col_width, row_height, header, border=1)
    pdf.ln(row_height)

    # Write data
    for i in range(min(100, len(output_df))):  # Limit rows for performance
        for item in output_df.iloc[i]:
            pdf.cell(col_width, row_height, str(item), border=1)
        pdf.ln(row_height)

    pdf.output(pdf_path)

    # Step 8: Create Map
    map_center = [output_df['lat'].mean(), output_df['lng'].mean()]
    m = folium.Map(location=map_center, zoom_start=11)
    marker_cluster = MarkerCluster().add_to(m)

    emoji_map = {
        'EMS': '🚑',
        'Fire': '🔥',
        'Traffic': '🚓',
        'Other': '❓'
    }

    for idx, row in output_df.iterrows():
        emoji = emoji_map.get(row['call_type'], '❓')
        popup_text = f"{emoji} <b>Call Type:</b> {row['call_type']}<br><b>Description:</b> {row['description of emergency']}<br><b>Date:</b> {row['date']}"
        folium.Marker(
            location=[row['lat'], row['lng']],
            popup=popup_text,
            icon=folium.DivIcon(
                html=f"""<div style="font-size:24px;">{emoji}</div>"""
            )
        ).add_to(marker_cluster)

    map_html_path = 'predicted_hotspots_map.html'
    m.save(map_html_path)

    return output_csv_path, pdf_path, map_html_path


# Streamlit App
def main():
    st.title("Emergency Call Prediction")

    # File uploader
    uploaded_file = st.file_uploader("Upload your cleaned 911 CSV file", type=["csv"])

    # Month input (1 to 12 only)
    month_input = st.number_input("Months", min_value=1, max_value=12, step=1,
                                  help="Enter number of months between 1 and 12.")

    # Predict button
    if st.button("Predict"):
        if uploaded_file is not None and month_input is not None:
            with st.spinner('Predicting emergencies... Please wait ⏳'):
                csv_path, pdf_path, map_html_path = predict_emergencies(uploaded_file, int(month_input))

            st.success('✅ Prediction completed!')

            # Show PDF link
            st.subheader("Prediction Results PDF")
            with open(pdf_path, "rb") as f:
                st.download_button(label="Download PDF", data=f, file_name="predicted_emergencies.pdf",
                                    mime="application/pdf")

            # Show map view link
            st.subheader("Click to have a map view")
            st.markdown(f"[View Map](./{map_html_path})", unsafe_allow_html=True)

        else:
            st.error("Please upload a CSV and enter months before clicking Predict.")


if __name__ == "__main__":
    main()
