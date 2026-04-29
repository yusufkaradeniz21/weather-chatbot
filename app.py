import streamlit as st
import os
from tools.weather import get_weather
from rag.pipeline import create_vector_db, query_weather_data
from llm.grok import get_llm

# 1. Sayfa Yapılandırması (Tarayıcı başlığı)
st.set_page_config(page_title="AI Hava Durumu Asistanı", page_icon="🌤️")

# Sayfa Başlığı ve Açıklama
st.title("🌤️ Yapay Zeka Destekli Hava Durumu")
st.markdown("""
Bu uygulama **canlı hava durumu** verilerini çeker, bir **vektör hafızasına (RAG)** kaydeder
ve **LLaMA 3.3 70B** modelini kullanarak size akıllıca yorumlar sunar.
""")

# 2. Kullanıcı Giriş Alanı
city = st.text_input("Hangi şehrin hava durumunu öğrenmek istersiniz?", placeholder="Örn: İstanbul, Ankara, Berlin...")

if city:
    # Yükleme animasyonu başlat
    with st.spinner(f"{city} için veriler analiz ediliyor..."):
        try:
            # ADIM 1: Hava durumunu internetten çek (Tools)
            raw_weather_data = get_weather(city)
            
            if "bulunamadı" in raw_weather_data:
                st.error(raw_weather_data)
            else:
                # ADIM 2: Veriyi botun hafızasına (RAG) işle
                vector_db = create_vector_db(raw_weather_data)
                
                # ADIM 3: Grok modelini hazırla
                llm = get_llm()
                
                # ADIM 4: Hafızadaki (RAG) bilgiyi sorgula ve yorumla
                context = query_weather_data(vector_db, f"{city} hava durumu özeti")
                
                prompt = f"""
                Sen arkadaş canlısı bir hava durumu asistanısın. 
                Sana verilen şu güncel bilgiyi kullan: {context}
                
                Lütfen kullanıcıya şunları söyle:
                1. Şu anki sıcaklık ve genel durum nedir?
                2. Bu havada dışarı çıkarken ne giyilmesini önerirsin?
                3. Gününü daha iyi geçirmesi için kısa ve neşeli bir tavsiye ver.
                
                Cevabın samimi ve yardımsever olsun.
                """
                
                # Grok'tan yanıtı al
                response = llm.invoke(prompt)
                
                # 3. Sonuçları Ekrana Yazdır
                st.success(f"✅ {city} için analiz tamamlandı!")
                
                # Chatbot cevabını şık bir kutuda göster
                st.chat_message("assistant").write(response.content)
                
                # Teknik detayları merak edenler için gizli bölme
                with st.expander("🔍 API'den Gelen Ham Veriyi Gör"):
                    st.info(raw_weather_data)
                    
        except Exception as e:
            st.error("Bir hata oluştu. Lütfen .env dosyasındaki API anahtarınızı kontrol edin.")
            st.warning(f"Hata detayı: {e}")

st.divider()
st.caption("Gücünü LLaMA 3.3 70B (Groq), LangChain ve Open-Meteo API'den alır.")