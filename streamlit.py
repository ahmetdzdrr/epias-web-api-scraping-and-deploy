import streamlit as st
import pandas as pd
import os
import folium
from streamlit_folium import st_folium

def load_data(output_folder):
    combined_csv = pd.DataFrame()
    for file_name in os.listdir(output_folder):
        if file_name.endswith('.csv'):
            file_path = os.path.join(output_folder, file_name)
            df = pd.read_csv(file_path, sep=',')
            combined_csv = pd.concat([combined_csv, df], axis=0)
    return combined_csv

def get_unique_values(df, column_name):
    return ["None"] + df[column_name].unique().tolist()

def main():
    st.title("EPİAŞ Elektrik Kesintisi Verileri")

    output_folder = "db"
    df = load_data(output_folder)
    
    unique_sehir = get_unique_values(df, 'Şehir')
    selected_sehir = st.selectbox("Şehir Seçin", unique_sehir, index=0)

    if selected_sehir == 'None':
        st.info("Lütfen bir şehir seçiniz.")
    else:
        filtered_data_sehir = df[df["Şehir"] == selected_sehir]
        
        if filtered_data_sehir.empty:
            st.error(f"{selected_sehir} ile ilgili veri bulunamadı.")
        else:
            st.subheader(f"{selected_sehir} İçin Planlı Elektrik Kesinti Bölgeleri ve Saatleri")
            filtered_data_sehir = filtered_data_sehir.dropna(axis=0)
            if not filtered_data_sehir[['Latitude', 'Longitude']].dropna().empty:
                lat_mean = filtered_data_sehir['Latitude'].mean()
                lon_mean = filtered_data_sehir['Longitude'].mean()
                m = folium.Map(location=[lat_mean, lon_mean], zoom_start=8)

                for _, row in filtered_data_sehir.iterrows():
                    popup_html = f"""
                        <div style="font-size: 14px; color: #333;">
                            <strong>Başlangıç:</strong> {row['Başlangıç Tarih - Saati']}<br>
                            <strong>Bitiş:</strong> {row['Bitiş Tarih - Saati']}<br>
                            <strong>Bölgeler:</strong> {row['Bölgeler(Semt-Mahalle)']}
                        </div>
                    """
                    folium.Marker(
                        location=[row["Latitude"], row["Longitude"]],
                        popup=folium.Popup(popup_html, max_width=300),
                        icon=folium.Icon(color="red")
                    ).add_to(m)

                st_folium(m, width=700, height=500)
            else:
                st.warning("Seçilen şehir için geçerli enlem ve boylam verisi bulunamadı.")

    st.markdown("""
        <style>
        .footer {
            text-align: center;
            padding: 20px;
            position: absolute;
            bottom: 0;
            left: 0;
            top: 0;
            right: 0;
            width: 100%;
            background-color: transparent;
            z-index: 1000;
        }
        .footer a {
            margin: 0 15px;
            text-decoration: none;
            color: #0073e6;
        }
        .footer img {
            height: 30px;
            margin-bottom: 15px;
            vertical-align: middle;
        }
        .name {
            position: relative;
            font-weight: 600;
            font-size: 20px;
            margin-left: 5px;    
        }
        </style>
        <div class="footer">
            <a href="https://github.com/ahmetdzdrr" target="_blank">
                <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="GitHub Logo">
            </a>
            <a href="https://linkedin.com/in/ahmet-dizdarr" target="_blank">
                <img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" alt="LinkedIn Logo">
            </a>
            <br>
            <span>Powered by</span><span class="name">Ahmet Dizdar</span>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
