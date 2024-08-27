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
        self.base_url = "https://seffaflik.epias.com.tr/electricity-service/v1/consumption/export/planned-power-outage-info"
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
        print("Username:", self.username)
        print("Password:", self.password)

        if response.status_code == 201:
            ticket_location = response.headers['Location']
            self.ticket_key = ticket_location.split('/')[-1]
            print(f"Ticket key başarıyla alındı: {self.ticket_key}")
        else:
            print(f"Ticket alma işlemi başarısız oldu: {response.status_code}")
            print("Hata mesajı:", response.text)
            self.ticket_key = None
    
    def make_request(self, period):
        headers = {
            "Content-Type": "application/json",
            "TGT": self.ticket_key
        }
        data = {"exportType": "CSV", "period": period}
        
        try:
            response = requests.post(self.base_url, json=data, headers=headers, stream=True)
            return response
        except requests.exceptions.RequestException as e:
            print(f"İstek sırasında bir hata oluştu: {e}")
            return None
    
    def save_response_to_file(self, response, file_name):
        with open(file_name, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        print(f"{file_name} dosyası başarıyla kaydedildi.")
    
    def download_data(self, start_date):
        current_date = start_date
        period = current_date.strftime("%Y-%m-%dT00:00:00+03:00")
        print(f"{pd.to_datetime(current_date, format='%Y-%m-%d')} verileri çekiliyor..")
        file_name = f"{self.output_folder}/data.csv"
        response = self.make_request(period)

        if response and response.status_code == 200:
            self.save_response_to_file(response, file_name)
            time.sleep(5)
        elif response:
            print(f"İstek başarısız oldu: {response.status_code} ({period})")
            print("Hata mesajı:", response.text)
        print("Tüm veriler başarıyla indirildi.")
    
    def preprocessing(self):
        selected_columns = [
            "Şehir", "İlçe Adı", "Tarih", 
            "Başlangıç Tarih - Saati", "Bitiş Tarih - Saati", 
            "Bölgeler(Semt-Mahalle)"
        ]
        
        for file_name in os.listdir(self.output_folder):
            if file_name.endswith('.csv'):
                file_path = os.path.join(self.output_folder, file_name)
                try:
                    df = pd.read_csv(file_path, sep=';')
                    df = df[selected_columns]
                    df["Başlangıç Tarih - Saati"] = pd.to_datetime(df["Başlangıç Tarih - Saati"], format='%d.%m.%Y %H:%M', errors='coerce')
                    df["Bitiş Tarih - Saati"] = pd.to_datetime(df["Bitiş Tarih - Saati"], format='%d.%m.%Y %H:%M', errors='coerce')
                    df["İlçe Adı"] = df["İlçe Adı"].apply(lambda x: x.split('/')[0].strip() if '/' in x else x)
                    df.replace({'İSTANBUL-AVRUPA': 'ISTANBUL', 'İSTANBUL-ASYA': 'ISTANBUL'}, inplace=True)
                    df['Şehir'] = df['Şehir'].str.replace('Ç', 'C').str.replace('İ', 'I').str.replace('Ş', 'S')
                    df.sort_values(by='Şehir', ascending=True, inplace=True)
                except pd.errors.ParserError as e:
                    print(f"Hata oluştu: {file_name}")
                    print(e)
                    continue
        
        output_file = f'{self.output_folder}/{file_name}'
        df.to_csv(output_file, index=False)
        print(f"Düzenlenmiş dosya başarıyla kaydedildi: {output_file}")

    
    def run(self, start_date):
        self.get_ticket_key()
        if self.ticket_key:
            self.download_data(start_date)
            self.preprocessing()
        else:
            print("Ticket key alınamadığı için işlemler gerçekleştirilemedi.")

if __name__ == "__main__":
    start_date = datetime.now() + timedelta(days=1)
    client = EpiasClient()
    client.run(start_date)
