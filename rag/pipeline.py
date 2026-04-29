from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from llm.grok import get_embeddings

def create_vector_db(weather_text):
    """
    Ham metni belge formatına çevirip vektör veritabanına (hafıza) ekler.
    """
    # Belge oluşturma
    documents = [Document(page_content=weather_text, metadata={"source": "live_api"})]
    
    # llm/gemini.py dosyasındaki get_embeddings fonksiyonunu kullanıyoruz
    embeddings = get_embeddings()
    
    # FAISS vektör veritabanını oluşturma
    vector_db = FAISS.from_documents(documents, embeddings)
    return vector_db

def query_weather_data(vector_db, query):
    """
    Vektör veritabanında arama yapar ve en yakın sonucu döner.
    """
    # Hafızada benzerlik araması yap
    docs = vector_db.similarity_search(query)
    
    if docs:
        return docs[0].page_content
    return "Hafızada ilgili bilgi bulunamadı."