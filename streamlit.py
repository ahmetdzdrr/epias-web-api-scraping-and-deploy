import streamlit as st
import pandas as pd
import os
import folium
from streamlit_folium import st_folium

def load_data(file_path):
    df = pd.read_csv(file_path, sep=',')
    return df

def get_unique_values(df, column_name):
    return ["None"] + df[column_name].unique().tolist()

def main():
    st.title("EPİAŞ Elektrik Kesintisi Verileri")

    # Kesinti Tipi Seçimi
    kesinti_tipi = st.selectbox("Kesinti Tipini Seçin", ["None", "Planlı Kesinti Verileri", "Plansız Kesinti Verileri"], index=0)

    if kesinti_tipi == "None":
        st.info("Lütfen kesinti tipini seçiniz.")
    else:
        output_folder = "db"
        file_name = "data_planned.csv" if kesinti_tipi == "Planlı Kesinti Verileri" else "data_unplanned.csv"
        file_path = os.path.join(output_folder, file_name)
        df = load_data(file_path)
        
        # Şehir Seçimi
        unique_sehir = get_unique_values(df, 'Şehir')
        selected_sehir = st.selectbox("Şehir Seçin", unique_sehir, index=0)

        if selected_sehir == 'None':
            st.info("Lütfen bir şehir seçiniz.")
        else:
            filtered_data_sehir = df[df["Şehir"] == selected_sehir]

            if filtered_data_sehir.empty:
                st.error(f"{selected_sehir} ile ilgili veri bulunamadı.")
            else:
                st.subheader(f"{selected_sehir} İçin {kesinti_tipi}")

                if not filtered_data_sehir[['Latitude', 'Longitude']].dropna().empty:
                    lat_mean = filtered_data_sehir['Latitude'].mean()
                    lon_mean = filtered_data_sehir['Longitude'].mean()
                    m = folium.Map(location=[lat_mean, lon_mean], zoom_start=8)

                    for _, row in filtered_data_sehir.iterrows():
                        if kesinti_tipi == 'Planlı Kesinti Verileri':
                            popup_html = f"""
                            <div style="font-size: 14px; color: #333;">
                                <strong>Başlangıç:</strong> {row['Başlangıç Tarih - Saati']}<br>
                                <strong>Bitiş:</strong> {row['Bitiş Tarih - Saati']}<br>
                                <strong>Bölgeler:</strong> {row['Bölgeler(Semt-Mahalle)']}
                            </div>
                        """
                        else:
                            popup_html = f"""
                            <div style="font-size: 14px; color: #333;">
                                <strong>Tarih:</strong> {row['Tarih']}<br>
                                <strong>Yer:</strong> {row['Şehir']} - {row['İlçe Adı']}<br>
                                <strong>Kesinti Sayısı:</strong> {row['Kesinti Sayısı']}
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
            position: relative;
            bottom: 0;
            left: 0;
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
