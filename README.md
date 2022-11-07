<h1 align="left"> Veri Etiketleme Aracı </h1>
Bu araç veri kazıma aşamasından sonra verilerin istenilen kategoriye göre etiketlenmesi ve kullanılmayacak olan verilerin database'ten silinmesi ile makine öğrenmesi modellerini kullanmak için etiketleme adımınını otomatikleştirmek amaçlı yapılmıştır.
<h2 align="left"> Geliştirme Ortamını Ayarlamak </h2>
<a href="https://www.python.org/downloads/" target="blank"><img align="center" src="https://img.shields.io/pypi/pyversions/Scrapy.svg"></a>


```
python3 --version
```

- Virtual environment oluşturma ve aktif etme
  
```
cd venv-folder-path 
python3 -m venv <venv-name>
source <venv-name> /bin/activate
```  
  
  
- Pycharm ile virtual environment oluşturma

  <img src="https://camo.githubusercontent.com/..." data-canonical-src="https://github.com/elifftosunn/Data-Labeling/blob/master/img/virtualenvEnvironment.PNG
" width="250" height="250" />
  
- Terminal üzerinden streamlit, psycopg2(postgresql) ve pandas indirme

<a href="https://docs.streamlit.io/library/get-started/installation" target="blank"><img align="center" src="https://docs.streamlit.io/logo.svg"></a>

```
pip install streamlit
```

<a href="https://pypi.org/project/psycopg2/" target="blank"><img align="center" src="https://pypi.org/static/images/logo-small.95de8436.svg"></a>
```
pip install psycopg2
```
<a href="https://pypi.org/project/pandas/" target="blank"><img align="center" src="https://warehouse-camo.ingress.cmh1.psfhosted.org/49dfa37dbb471fb97b1d94f27e3b343fb74ebcc1/68747470733a2f2f696d672e736869656c64732e696f2f707970692f762f70616e6461732e737667"></a>
```
pip install pandas
```
<h2 align="left"> Veri Etiketleme Aracı Uygulama Aşamaları </h2>

- İlk olarak, pgAdmin veya psql gibi herhangi bir istemci aracını kullanarak PostgreSQL veritabanı sunucusunda oturum açın.
- İkinci olarak, PostgreSQL veritabanı sunucusunda adlandırılmış yeni bir veritabanı oluşturmak için aşağıdaki ifadeyi kullanın

```
CREATE DATABASE complaints;
```
- Postgresql üzerinde tablo oluşturun

```
create table complaints(
	id integer primary key,
	name varchar(50),
	text text,
	link varchar(150)
)
```

- Tabloya bank.csv'yi import edin
```
COPY persons(id, name, text, link)
FROM 'csv-path\bank.csv'
DELIMITER ','
CSV HEADER;
```
- python dosyanızda kütüphaneleri import edin.

```
import psycopg2
import streamlit
import pandas as pd
```

- PostgreSQL veritabanına bağlanın

```
hostname = "localhost"
port_id = portId
database = "databaseName"
username = "username"
password = "password"

def sqlData(raw_code):
    with psycopg2.connect(host=hostname,port=port_id,dbname=database,user=username,password=password) as conn:
        with conn.cursor() as curs:
            curs.execute(raw_code)
            conn.commit()
            data = curs.fetchall()
            return data
          
          
data = sqlExecute("select * from complaints")
df = pd.DataFrame(data, columns=["id", "name", "text", "link"])
st.dataframe(df)
```
- Web sayfasında görüntülemek için streamlit'i terminal üzerinden çalıştırın

```
streamlit run main.py
```





