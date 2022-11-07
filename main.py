import streamlit as st
import psycopg2
import pandas as pd

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
    with psycopg2.connect(host=hostname,port=port_id,dbname=database,user=username,password=password) as conn:
        with conn.cursor() as curs:
            curs.execute(raw_code)
            conn.commit() # save
def sqlData(raw_code):
    with psycopg2.connect(host=hostname,port=port_id,dbname=database,user=username,password=password) as conn:
        with conn.cursor() as curs:
            curs.execute(raw_code)
            conn.commit()
            data = curs.fetchall()
            return data
def repeatFunction(insertQuery, deleteQuery, placeholder, idNumber):
    insertQuery = sqlExecute(insertQuery)
    deleteQuery = sqlExecute(deleteQuery)
    if insertQuery == None and deleteQuery == None:
        placeholder.empty()
        st.success(f"{idNumber} id'li şikayet veritabanına aktarıldı.")
    else:
        placeholder.empty()
        st.info(f"{idNumber} id'li şikayet targets tablosunda bulunuyor...")

def stages(query_df,i,inner_cols,targetIdList):
    idNumber = query_df.iloc[i, 0]
    # st.write(idNumber)
    placeholder = st.empty()
    with placeholder.form(key=str(i)):
        text = st.text_area(str(query_df.iloc[i].loc["name"]),
                            value=query_df.iloc[i].loc[
                                "text"])  # col1 yerine complaints name, text yerine complaints text
        colOne, colTwo, colThree = st.columns(3)
        with inner_cols[0]:
            choice = colOne.selectbox(
                "Etiketi Seçiniz",
                ("Kredi İşlemleri", "Bankacılık İşlemleri", "Kart İşlemleri", "Müşteri Temsilcisi", "Diğer"), key=i
            )
        with inner_cols[1]:
            deleteButon = colTwo.form_submit_button("Sil")
        with inner_cols[2]:
            approveButon = colThree.form_submit_button("Onayla")
    insertQuery = f"insert into targets (id,target) values ({idNumber},'{choice}')"
    deleteQuery = f"delete from complaints where id = {idNumber}"
    if approveButon:
        if choice == "Kredi İşlemleri" and idNumber not in targetIdList:
            repeatFunction(insertQuery, deleteQuery, placeholder, idNumber)
        elif choice == "Bankacılık İşlemleri" and idNumber not in targetIdList:
            repeatFunction(insertQuery, deleteQuery, placeholder, idNumber)
        elif choice == "Kart İşlemleri" and idNumber not in targetIdList:
            repeatFunction(insertQuery, deleteQuery, placeholder, idNumber)
        elif choice == "Müşteri Temsilcisi" and idNumber not in targetIdList:
            repeatFunction(insertQuery, deleteQuery, placeholder, idNumber)
        elif choice == "Diğer" and idNumber not in targetIdList:
            repeatFunction(insertQuery, deleteQuery, placeholder, idNumber)
    elif deleteButon:
        deleteQuery = sqlExecute(deleteQuery)
        if deleteQuery == None:
            placeholder.empty()
            st.success(f"{idNumber} id'li şikayet veritabanından silindi.")
def main():
    outer_cols = st.columns([1,1])
    targetIdQuery = "select id from targets"
    targetIdQuery = sqlData(targetIdQuery)
    targetIdDataFrame = pd.DataFrame(targetIdQuery, columns=["targetId"])
    targetIdList = [targetIdDataFrame.iloc[i,0] for i in range(len(targetIdDataFrame))]
    # st.write(targetIdList)
    with outer_cols[0]:
        inner_cols = st.columns([1, 1, 1])
        raw_code = "select id,name,text from complaints"
        data = sqlData(raw_code)
        query_df = pd.DataFrame(data, columns=["id", "name", "text"])
        for i in range(10):
            stages(query_df, i, inner_cols, targetIdList)
    with outer_cols[1]:
        inner_cols = st.columns([1, 1, 1])
        raw_code = "select id,name,text from complaints"
        data = sqlData(raw_code)
        query_df = pd.DataFrame(data, columns=["id", "name", "text"])
        for i in range(10,20):
            stages(query_df, i, inner_cols, targetIdList)
if __name__ == "__main__":
    main()
