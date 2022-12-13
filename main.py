import streamlit as st
import psycopg2, time, numpy, os, pyautogui, base64, plotly, kaleido
import pandas as pd
from psycopg2.extensions import register_adapter, AsIs
import plotly.express as px
from io import BytesIO, StringIO
import plotly.io as pio


hostname = "localhost"
port_id = 5432
database = "nlpDatabase"
username = "postgres"
password = ""



st.set_page_config(page_title="Veri Etiketleme Aracı",
                   page_icon=":bar_chart:",
                   layout="wide",
                   initial_sidebar_state="expanded"
                   )

st.markdown('''<h1 style='text-align: center; color: white; font_size = 20'> 📊 Veri Etiketleme Aracı</h1>''',
            unsafe_allow_html=True)

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
          
def dataResult():
    csvDataQuery = "select c.id,text,t.target, u.username from comp c join targets t using (id) inner join users u on t.userId = u.id;"
    csvDataQuery = sqlData(csvDataQuery)
    csvData = pd.DataFrame(csvDataQuery, columns=["id", "text", "target", "username"])
    return csvData
  
def page2():
    def downloadImage(img_path, file_name):
        with open(img_path, "rb") as file:
            btn = st.download_button(
                label="Download image",
                data=file,
                mime="image/png",
                file_name=file_name
            )
    csvData = dataResult()
    static = st.empty()
    st.subheader("Etikete Göre İstatistikler")
    fig = px.bar(csvData.target.value_counts(), width=1200)
    st.plotly_chart(fig)
    pio.kaleido.write_image(fig=fig, file='img/targetStatics.jpg', format='jpg', engine="kaleido")
    downloadImage("img/targetStatics.jpg", "targetStatics.jpg")
    staticButton = static.button("Kullanıcı İstatistikleri Görüntüle")
    if staticButton:
        fig = px.bar(csvData.username.value_counts(), width=1200)
        st.plotly_chart(fig)
        pio.kaleido.write_image(fig=fig, file='img/userStatics.jpg', format='jpg', engine="kaleido")
        downloadImage("img/userStatics.jpg", "userStatics.jpg")
        static.empty()
        
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
            csvData = dataResult()
            cho = st.selectbox("Dataset indirme biçimini seçiniz", ("csv", "excel", "json"))
            csvData.to_csv("datas/targetDataset.csv")
            if cho == "csv":
                st.download_button(
                    label="📥 Download data as CSV",
                    data=csvData.to_csv().encode("utf-8"),
                    file_name='bank_result.csv',
                    mime='text/csv',
                )
            elif cho == "excel":
                file_path = "datas/targetDataset.csv"
                with open(file_path, 'rb') as my_file:
                    st.download_button(label='📥 Download data as Excel', data=my_file, file_name='bank_result.xlsx',
                                       mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

            elif cho == "json":
                st.download_button(
                    label="📥 Download data as Json",
                    data=csvData.to_json(),
                    file_name="bank_result.json",
                    mime="text/json"
                )
        # def statics():
        #     staticButton = st.button("İstatistikleri Görüntüle")
        #     if staticButton:
        #         st.bar_chart(csvData.username.value_counts())
        userId = user()
        file()
    return userId


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
    session = st.empty()
    if USER_ID == "None":
        USER_ID = sidebarPanel()
        os.environ["USER_ID"] = str(USER_ID)
    else:
        # st.write(f"User Giriş Yapılıyor Yeni ID: {USER_ID}")
        out = session.button("Çıkış")
        if out:
            st.write(f"{USER_ID} çıkış yapılıyor...")
            time.sleep(0.5)
            logout()
            session.empty()
            login()
            time.sleep(0.5)
            pyautogui.hotkey('f5')
    return USER_ID
def main():
    USER_ID = login()
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

def main_page():
    # st.sidebar.markdown("# Ana Sayfa 🎈")
    main()

if __name__ == "__main__":
    page_names_to_funcs = {
        "Ana Sayfa": main_page,
        "İstatistikler": page2}

    selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
    page_names_to_funcs[selected_page]()
    
    
