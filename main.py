import os
import time
import requests
import pandas as pd
from datetime import datetime, timedelta

class EpiasClient:
    def __init__(self, output_folder="db"):
        self.username = os.getenv("USERNAME")
        self.password = os.getenv("PASSWORD")
        self.ticket_key = None
        self.output_folder = output_folder
        self.post_list = ['planned', 'unplanned']
        self.ticket_url = "https://giris.epias.com.tr/cas/v1/tickets"
        os.makedirs(self.output_folder, exist_ok=True)
        
    def get_ticket_key(self):
        headers = {
            "Accept": "text/plain",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "username": self.username,
            "password": self.password
        }
        
        response = requests.post(self.ticket_url, headers=headers, data=data)
        if self.username and self.password is not None:
            print("Username defined\nPassword defined")

        if response.status_code == 201:
            ticket_location = response.headers['Location']
            self.ticket_key = ticket_location.split('/')[-1]
            print(f"Ticket key başarıyla alındı")
        else:
            print(f"Ticket alma işlemi başarısız oldu: {response.status_code}")
            print("Hata mesajı:", response.text)
            self.ticket_key = None
    
    def make_request(self, base_url, period):
        headers = {
            "Content-Type": "application/json",
            "TGT": self.ticket_key
        }
        data = {"exportType": "CSV", "period": period}
        
        try:
            response = requests.post(base_url, json=data, headers=headers, stream=True)
            return response
        except requests.exceptions.RequestException as e:
            print(f"İstek sırasında bir hata oluştu: {e}")
            return None
    
    def save_response_to_file(self, response, file_name):
        with open(file_name, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        print(f"{file_name} dosyası başarıyla kaydedildi.")
    
    def download_data(self, index, base_url, start_date):
        current_date = start_date
        period = current_date.strftime("%Y-%m-%dT00:00:00+03:00")
        if self.post_list[index] == 'planned':
            print(f"{pd.to_datetime(current_date).strftime('%Y-%m-%d')} planlı kesinti verileri çekiliyor..")
        else:
            print(f"{pd.to_datetime(current_date).strftime('%Y-%m-%d')} plansız kesinti verileri çekiliyor..")
        file_name = f"{self.output_folder}/data_{self.post_list[index]}.csv"
        response = self.make_request(base_url, period)

        if response and response.status_code == 200:
            self.save_response_to_file(response, file_name)
            time.sleep(5)
        elif response:
            print(f"İstek başarısız oldu: {response.status_code} ({period})")
            print("Hata mesajı:", response.text)
        print("Tüm veriler başarıyla indirildi.")
    
    def get_lat_lon(self, sehir, ilce):
        url = f"https://nominatim.openstreetmap.org/search?city={ilce}&state={sehir}&country=Turkey&format=json"
        headers = {
            "User-Agent": f"YourAppName/1.0 ({self.username})"
        }
        response = requests.get(url, headers=headers)
        try:
            response_json = response.json()
            if response_json:
                return response_json[0]["lat"], response_json[0]["lon"]
            else:
                return None, None
        except ValueError:
            print("JSON Decode Error: Invalid JSON response")
            return None, None

    def add_lat_lon_to_data(self, df):
        df["Latitude"] = None
        df["Longitude"] = None
        for index, row in df.iterrows():
            lat, lon = self.get_lat_lon(row["Şehir"], row["İlçe Adı"])
            df.at[index, "Latitude"] = lat
            df.at[index, "Longitude"] = lon
        return df
    
    def preprocess_unplanned_data(self, df, file_name):
        try:
            grouped_df = df.groupby(['Şehir', 'İlçe Adı', 'Tarih']).size().reset_index(name='Kesinti Sayısı')
            
            lat_lon_df = grouped_df.apply(
                lambda row: pd.Series(self.get_lat_lon(row['Şehir'], row['İlçe Adı'])),
                axis=1
            )
            lat_lon_df.columns = ['Latitude', 'Longitude']
            grouped_df = pd.concat([grouped_df, lat_lon_df], axis=1)
            
            final_df = grouped_df[['Şehir', 'İlçe Adı', 'Tarih', 'Kesinti Sayısı', 'Latitude', 'Longitude']]
            output_file = f'{self.output_folder}/{file_name}'
            final_df.to_csv(output_file, index=False)
            
            print(f"Düzenlenmiş dosya başarıyla kaydedildi: {output_file}")
        
        except Exception as e:
            print(f"Hata oluştu: {file_name}")
            print(e)
    
    def preprocessing(self, file_name):
        selected_columns = [
            "Şehir", "İlçe Adı", "Tarih", 
            "Başlangıç Tarih - Saati", "Bitiş Tarih - Saati", 
            "Bölgeler(Semt-Mahalle)"
        ]
        
        file_path = os.path.join(self.output_folder, file_name)
        try:
            df = pd.read_csv(file_path, sep=';')
            df = df[selected_columns]
            df["Başlangıç Tarih - Saati"] = pd.to_datetime(df["Başlangıç Tarih - Saati"], format='%d.%m.%Y %H:%M', errors='coerce')
            df["Bitiş Tarih - Saati"] = pd.to_datetime(df["Bitiş Tarih - Saati"], format='%d.%m.%Y %H:%M', errors='coerce')
            df["İlçe Adı"] = df["İlçe Adı"].apply(lambda x: x.split('/')[0].strip() if '/' in x else x)
            df.replace({'İSTANBUL-AVRUPA': 'İSTANBUL', 'İSTANBUL-ASYA': 'İSTANBUL'}, inplace=True)
            df['İlçe Adı'] = df['İlçe Adı'].replace('Sivas Merkez', 'Merkez')
            df['Şehir'] = df['Şehir'].str.replace('Ç', 'C').str.replace('İ', 'I').str.replace('Ş', 'S')
            df.sort_values(by='Şehir', ascending=True, inplace=True)
            
            if 'unplanned' in file_name:
                self.preprocess_unplanned_data(df, file_name)
            else:
                df = self.add_lat_lon_to_data(df)
                output_file = f'{self.output_folder}/{file_name}'
                df.to_csv(output_file, index=False)
                print(f"Düzenlenmiş dosya başarıyla kaydedildi: {output_file}")
                    
        except pd.errors.ParserError as e:
            print(f"Hata oluştu: {file_name}")
            print(e)

    
    def run(self, start_date):
        self.get_ticket_key()
        for index, value in enumerate(self.post_list):
            if self.ticket_key:
                base_url = f"https://seffaflik.epias.com.tr/electricity-service/v1/consumption/export/{value}-power-outage-info"
                if value == 'planned':
                    self.download_data(index, base_url, start_date)
                else:
                    start_date = start_date - pd.Timedelta(days=2)
                    self.download_data(index, base_url, start_date)
                
                file_name = f"data_{value}.csv"
                self.preprocessing(file_name)
            else:
                print("Ticket key alınamadığı için işlemler gerçekleştirilemedi.")

if __name__ == "__main__":
    start_date = datetime.now() + timedelta(days=1)
    client = EpiasClient()
    client.run(start_date)
