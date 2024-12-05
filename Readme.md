# Cara Menjalankan Proyek di Local

1. Masuk ke dalam projek

```bash
git clone https://github.com/Luthfiyanto/AccountingApp.git
cd AccountingApp
```

2. Buat Virtual Environtment

```bash
python -m venv env

env\Scripts\activate
```

3. Install Dependencies

```bash
pip install -r requirements.txt
```

4. Buat file database dengan nama accounting.db dan tambahkan file inventory.csv

5. Jalankan Aplikasi

```bash
streamlit run app.py
```
