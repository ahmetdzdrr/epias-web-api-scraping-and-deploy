import streamlit as st
import pandas as pd
import os

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
            unique_ilce = get_unique_values(filtered_data_sehir, 'İlçe Adı')
            selected_ilce = st.selectbox("İlçe Seçin", unique_ilce, index=0)
            
            if selected_ilce == 'None':
                st.info("Lütfen bir ilçe seçiniz.")
            else:
                filtered_data_ilce = filtered_data_sehir[filtered_data_sehir["İlçe Adı"] == selected_ilce]
                
                if filtered_data_ilce.empty:
                    st.error(f"{selected_ilce} ile ilgili veri bulunamadı.")
                else:
                    st.subheader(f"{selected_sehir} - {selected_ilce} İçin Elektrik Kesinti Saatleri")
                    st.dataframe(filtered_data_ilce.reset_index(drop=True))

    st.markdown("""
        <style>
        .footer {
            text-align: center;
            padding: 20px;
            position: fixed;
            bottom: 0;
            left: 0;
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
            margin-bottom: 29px;
            vertical-align: middle;
        }
        </style>
        <div class="footer">
            <a href="https://github.com/ahmetdzdrr" target="_blank">
                <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="GitHub Logo">
            </a>
            <a href="https://linkedin.com/in/ahmet-dizdar" target="_blank">
                <img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" alt="LinkedIn Logo">
            </a>
            <br>
            <span>Powered by Ahmet Dizdar</span>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
