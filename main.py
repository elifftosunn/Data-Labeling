import streamlit as st
import psycopg2, time, numpy, os
import pandas as pd
from psycopg2.extensions import register_adapter, AsIs

df = pd.read_csv("../databaseConnect/database.csv")
hostname = "localhost"
port_id = 5432
database = "nlpDatabase"
username = "postgres"
password = "Eliftosun123"



st.set_page_config(page_title="Veri Etiketleme Aracı",
                   page_icon=":bar_chart:",
                   layout="wide",
                   initial_sidebar_state="expanded"
                   )

st.markdown('''<h1 style='text-align: center; color: white; font_size = 20'> 📊 Veri Etiketleme Aracı</h1>''',
            unsafe_allow_html=True)

def sidebarPanel():
    with st.sidebar:
        def user():
            user = st.text_input("👤 Kullanıcı adınızı giriniz", key="user")
            userButton = st.button("📁 Kaydet")
            userIdTotalQuery = "select id from users"
            userIdQuery = f"select id from users where username = '{user}'"
            userId = sqlData(userIdQuery)
            userIdTotalQuery = sqlData(userIdTotalQuery)
            usersDf = pd.DataFrame(userIdTotalQuery, columns=["users"])
            usersIdList = []
            for i in range(len(usersDf)):
                usersIdList.append(usersDf.iloc[i, 0])
            if userButton:
                if userId in usersIdList:
                    with st.spinner('Giriş yapılıyor...'):
                        time.sleep(0.5)
                    st.warning(f"Hoşgeldin {user} :smile:")
                    userIdDf = pd.DataFrame(userId)
                    return userIdDf.iloc[0, 0]
                else:
                    insertQuery = f"insert into users (id,username) values ({len(usersDf)},'{user}')"
                    insertQuery = sqlExecute(insertQuery)
                    if insertQuery == None:
                        with st.spinner('Kaydınız yapılıyor...'):
                            time.sleep(0.5)
                        st.success(f"Hoşgeldin {user} :smile:")
                    userIdQuery = sqlData(f"select id from users where id = {len(usersDf)}")
                    userIdDf = pd.DataFrame(userIdQuery)
                    return userIdDf.iloc[0, 0]

        def file():
            cho = st.selectbox("Dataset indirme biçimini seçiniz", ("csv", "excel", "json"))
            if cho == "csv":
                st.download_button(
                    label="📥 Download data as CSV",
                    data=df.to_csv().encode("utf-8"),
                    file_name='bank_deneme.csv',
                    mime='text/csv',
                )
            elif cho == "excel":
                file_path = "../databaseConnect/database.csv"
                with open(file_path, 'rb') as my_file:
                    st.download_button(label='📥 Download data as Excel', data=my_file, file_name='bank_deneme.xlsx',
                                       mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

            elif cho == "json":
                st.download_button(
                    label="📥 Download data as Json",
                    data=df.to_json(),
                    file_name="bank_deneme.json",
                    mime="text/json"
                )

        userId = user()
        file()
    return userId


def sqlExecute(raw_code):
    with psycopg2.connect(host=hostname, port=port_id, dbname=database, user=username, password=password) as conn:
        with conn.cursor() as cursor:
            cursor.execute(raw_code)
            conn.commit()  # save


def sqlData(raw_code):
    with psycopg2.connect(host=hostname, port=port_id, dbname=database, user=username, password=password) as conn:
        with conn.cursor() as curs:
            curs.execute(raw_code)
            conn.commit()
            data = curs.fetchall()
            return data

def addapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)


def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)


register_adapter(numpy.float64, addapt_numpy_float64)
register_adapter(numpy.int64, addapt_numpy_int64)


def repeatFunction(insertQuery, deleteQuery, placeholder, idNumber):
    insertQuery = sqlExecute(insertQuery)
    deleteQuery = sqlExecute(deleteQuery)
    if insertQuery == None and deleteQuery == None:
        placeholder.empty()
        st.success(f"{idNumber} id'li şikayet veritabanına aktarıldı.")
    else:
        placeholder.empty()
        st.info(f"{idNumber} id'li şikayet targets tablosunda bulunuyor...")


def stages(query_df, i, targetIdList, USER_ID):
    idNumber = query_df.iloc[i, 0]  # idNumber = complaintId
    placeholder = st.empty()
    with placeholder.form(key=str(i)):
        text = st.text_area(str(query_df.iloc[i].loc["name"]),
                            value=query_df.iloc[i].loc[
                                "text"])
        choice = st.selectbox(
            "Etiketi Seçiniz",
            ('Kredi İşlemleri', 'Bankacılık İşlemleri', 'Kart İşlemleri', 'Müşteri Temsilcisi', 'Diğer'),
            key=i
        )
        deleteButon = st.form_submit_button("Sil")
        approveButon = st.form_submit_button("Onayla")
    deleteQuery = f"delete from complaints where id = {idNumber}"
    if approveButon and USER_ID is not None:
        insertQuery = f"insert into targets (id,target,userid) values ({idNumber},'{choice}',{USER_ID})"
        if choice == 'Kredi İşlemleri' and idNumber not in targetIdList:
            repeatFunction(insertQuery, deleteQuery, placeholder, idNumber)
        elif choice == 'Bankacılık İşlemleri' and idNumber not in targetIdList:
            repeatFunction(insertQuery, deleteQuery, placeholder, idNumber)
        elif choice == 'Kart İşlemleri' and idNumber not in targetIdList:
            repeatFunction(insertQuery, deleteQuery, placeholder, idNumber)
        elif choice == 'Müşteri Temsilcisi' and idNumber not in targetIdList:
            repeatFunction(insertQuery, deleteQuery, placeholder, idNumber)
        elif choice == 'Diğer' and idNumber not in targetIdList:
            repeatFunction(insertQuery, deleteQuery, placeholder, idNumber)
    elif deleteButon and USER_ID != "None":
        deleteQuery = sqlExecute(deleteQuery)
        if deleteQuery == None:
            placeholder.empty()
            st.success(f"{idNumber} id'li şikayet veritabanından silindi.")
def logout():
    os.environ["USER_ID"] = "None"
def login():
    USER_ID = os.environ.get('USER_ID')
    if USER_ID == "None":
        USER_ID = sidebarPanel()
        if USER_ID != None:
            st.write(f"User Giriş Yapılıyor Yeni ID: {USER_ID}")

        os.environ["USER_ID"] = str(USER_ID)
    else:
        st.write(f"User Giriş Yapmış ID: {USER_ID}")
    return USER_ID
def main():
    USER_ID = login()
    if USER_ID != "None":
        out = st.button("Çıkış")
        if out:
            logout()
    outer_cols = st.columns([1, 1])
    targetIdQuery = "SELECT id FROM targets"
    targetIdQuery = sqlData(targetIdQuery)
    targetIdDataFrame = pd.DataFrame(targetIdQuery, columns=["targetId"])
    targetIdList = [targetIdDataFrame.iloc[i, 0] for i in range(len(targetIdDataFrame))]
    with outer_cols[0]:
        raw_code = "SELECT id, name, text FROM complaints"
        data = sqlData(raw_code)
        query_df = pd.DataFrame(data, columns=["id", "name", "text"])
        for i in range(10):
            stages(query_df, i, targetIdList, USER_ID)
    with outer_cols[1]:
        # inner_cols = st.columns([1, 1, 1])
        raw_code = "select id,name,text from complaints"
        data = sqlData(raw_code)
        query_df = pd.DataFrame(data, columns=["id", "name", "text"])
        for i in range(10, 20):
            stages(query_df, i, targetIdList, USER_ID)

if __name__ == "__main__":
    main()
