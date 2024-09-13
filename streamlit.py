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
    st.title("EPIAS Power Outage Data")

    outage_type = st.selectbox("Select Outage Type", ["None", "Planned Outage Data", "Unplanned Outage Data"], index=0)

    if outage_type == "None":
        st.info("Please select the type of outage.")
    else:
        output_folder = "db"
        file_name = "data_planned.csv" if outage_type == "Planned Outage Data" else "data_unplanned.csv"
        file_path = os.path.join(output_folder, file_name)
        df = load_data(file_path)

        turkey_cities = [
            "None",
            "ADANA", "ADIYAMAN", "AFYONKARAHISAR", "AĞRI", "AKSARAY", "AMASYA", "ANKARA",
            "ANTALYA", "ARTVIN", "AYDIN", "BALIKESIR", "BARTIN", "BATMAN", "BAYBURT",
            "BILECIK", "BINGOL", "BITLIS", "BOLU", "BURDUR", "BURSA", "CANAKKALE",
            "CANKIRI", "CORUM", "DENIZLI", "DIYARBAKIR", "DUZCE", "EDIRNE", "ELAZIG",
            "ERZINCAN", "ERZURUM", "ESKISEHIR", "GAZIANTEP", "GIRESUN", "GUMUSHANE",
            "HAKKARI", "HATAY", "IGDIR", "ISPARTA", "ISTANBUL", "IZMIR", "KAHRAMANMARAS",
            "KARABUK", "KARAMAN", "KARS", "KASTAMONU", "KAYSERI", "KIRIKKALE", "KIRKLARELI",
            "KIRSEHIR", "KOCAELI", "KONYA", "KUTAHYA", "MALATYA", "MANISA", "MARDIN", 
            "MUGLA", "MUS", "NEVSEHIR", "NIGDE", "ORDU", "OSMANIYE", "RIZE",
            "SAKARYA", "SAMSUN", "SIIRT", "SINOP", "SIVAS", "SANLIURFA", "SIRNAK",
            "TEKIRDAG", "TOKAT", "TRABZON", "TUNCELI", "USAK", "VAN", "YALOVA",
            "YOZGAT", "ZONGULDAK"
        ]

        selected_sehir = st.selectbox("City", turkey_cities, index=0)

        if selected_sehir == 'None':
            st.info("Please choose your city.")
        else:
            filtered_data_sehir = df[df["Şehir"] == selected_sehir]
            filtered_data_sehir = filtered_data_sehir.dropna(axis=0)

            if filtered_data_sehir.empty:
                st.error(f"No outage data found for {selected_sehir}.")
            else:
                st.subheader(f"{outage_type} for {selected_sehir}")

                if not filtered_data_sehir[['Latitude', 'Longitude']].dropna().empty:
                    lat_mean = filtered_data_sehir['Latitude'].mean()
                    lon_mean = filtered_data_sehir['Longitude'].mean()
                    m = folium.Map(location=[lat_mean, lon_mean], zoom_start=8)

                    for _, row in filtered_data_sehir.iterrows():
                        if outage_type == 'Planned Outage Data':
                            popup_html = f"""
                            <div style="font-size: 14px; color: #333;">
                                <strong>Start:</strong> {row['Başlangıç Tarih - Saati']}<br>
                                <strong>End:</strong> {row['Bitiş Tarih - Saati']}<br>
                                <strong>Regions:</strong> {row['Bölgeler(Semt-Mahalle)']}
                            </div>
                            """
                        else:
                            popup_html = f"""
                            <div style="font-size: 14px; color: #333;">
                                <strong>Date:</strong> {row['Tarih']}<br>
                                <strong>Place:</strong> {row['Şehir']} - {row['İlçe Adı']}<br>
                                <strong>Number of Interruptions:</strong> {row['Kesinti Sayısı']}
                            </div>
                            """
                        folium.Marker(
                            location=[row["Latitude"], row["Longitude"]],
                            popup=folium.Popup(popup_html, max_width=300),
                            icon=folium.Icon(color="red")
                        ).add_to(m)

                    st_folium(m, width=700, height=500)
                else:
                    st.warning("No valid latitude and longitude data found for the selected city.")

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
            <p align="center">
            <a href="https://www.buymeacoffee.com/ahmetdizdar" target="_blank">
            <img src="https://img.buymeacoffee.com/button-api/?text=Buy%20me%20a%20coffee&emoji=&slug=your-username&button_colour=FFDD00&font_colour=000000&font_family=Arial&outline_colour=000000&coffee_colour=ffffff" alt="Buy Me A Coffee">
            </a>
            </p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
