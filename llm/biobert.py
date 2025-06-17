from fastapi import FastAPI, Query
from typing import List
import nltk
import torch
import faiss
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer
from keybert import KeyBERT
import logging
import os
import fitz  # PyMuPDF
import nltk
import torch
import faiss
from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import AutoTokenizer, AutoModel
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sentence_transformers import SentenceTransformer
from keybert import KeyBERT

# Initialisation de FastAPI
app = FastAPI(debug=True)
logger = logging.getLogger('uvicorn')
logger.setLevel(logging.DEBUG)

# on télécharge les ressources ntlk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')

# on charge nos modèles
biobert_tokenizer = AutoTokenizer.from_pretrained("dmis-lab/biobert-base-cased-v1.1")
biobert_model = AutoModel.from_pretrained("dmis-lab/biobert-base-cased-v1.1")
keybert_model = KeyBERT(model=biobert_model)  # pour pas que y'ai l'avertissement

# on charge le sentence model
sentence_model = SentenceTransformer("msmarco-distilbert-base-v4")

# dossier où se trouvent les pdf
PDF_DIR = "../uploads"
pdf_files = [f for f in os.listdir(PDF_DIR) if f.endswith(".pdf")]
pdf_texts = []

# on lit + extract le texte
for pdf_file in pdf_files:
    pdf_path = os.path.join(PDF_DIR, pdf_file)
    doc = fitz.open(pdf_path)
    text = " ".join([page.get_text("text") for page in doc])
    pdf_texts.append((pdf_path, text))

# on enlève les mots the a et tt
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [word for word in tokens if word.isalpha() and word not in stop_words]
    return " ".join(tokens)

# on prétraite les données
cleaned_texts = [preprocess_text(text) for _, text in pdf_texts]

# on extrait des mots-clés avec TF-IDF et KeyBERT (BioBERT)
vectorizer = TfidfVectorizer(max_features=50, stop_words='english', ngram_range=(1, 2))
tfidf_matrix = vectorizer.fit_transform(cleaned_texts)
feature_names = vectorizer.get_feature_names_out()

keywords_per_doc = []
for i, text in enumerate(cleaned_texts):
    tfidf_scores = tfidf_matrix[i].toarray().flatten()
    tfidf_keywords = [feature_names[j] for j in tfidf_scores.argsort()[-10:][::-1]]
    bert_keywords = [kw[0] for kw in keybert_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), top_n=10)]
    
    # Priorisation des mots-clés longs et spécifiques
    keywords = sorted(set(tfidf_keywords + bert_keywords), key=len, reverse=True)
    keywords_per_doc.append(keywords)

    print(f"📄 {pdf_texts[i][0]} - Mots-clés extraits : {keywords}\n")

# on crée l'index FAISS avec IP (produit scalaire) (g testé L2 et c nul) et on normalise
embedding_dim = sentence_model.get_sentence_embedding_dimension()
index = faiss.IndexFlatIP(embedding_dim) 
doc_embeddings = []
doc_ids = []

for i, text in enumerate(cleaned_texts):
    embedding = sentence_model.encode(text, convert_to_numpy=True, normalize_embeddings=True)
    embedding = np.array([embedding], dtype=np.float32)  # format (1, d)
    doc_embeddings.append(embedding)
    index.add(embedding)  # ajout direct de l'embedding normalisé
    doc_ids.append(i)

MIN_SIMILARITY = 0.3  # à ajuster

def search_similar_docs(query, top_k=20):
    query_embedding = sentence_model.encode(query, convert_to_numpy=True, normalize_embeddings=True)
    query_embedding = np.array([query_embedding], dtype=np.float32)

    print(f"🔍 Embedding de la requête calculé ({query_embedding.shape})\n")

    D, I = index.search(query_embedding, top_k)
    results = []

    for rank, idx in enumerate(I[0]):
        if idx < 0 or idx >= len(pdf_texts):
            continue

        score = D[0][rank]
        if score < MIN_SIMILARITY:
            continue  

        doc_path, _ = pdf_texts[idx]
        keywords_list = keywords_per_doc[idx]
# TODO: append score
        results.append((doc_path, keywords_list[:5]))#, score))

    # on vérifie les mots clés si faiss trouve pas ce golmon
    if not results:
        print(f"⚠️ Aucun résultat FAISS trouvé pour '{query}'. Vérification des mots-clés...")
        for i, keywords in enumerate(keywords_per_doc):
            if query.lower() in [kw.lower() for kw in keywords]:  # on vérifie si le mot clé est dedans
                print(f"✅ Correspondance directe trouvée dans '{pdf_texts[i][0]}' ! Ajout manuel.")
                results.append((pdf_texts[i][0], keywords[:5], 0.95))

    # trier les results
    #results = sorted(results, key=lambda x: x[2], reverse=True)

    for doc, closest_words in results:
    #    print(f"📄 {doc} - Score FAISS : {score:.4f}")
        print(f"   🔹 Mots-clés proches : {', '.join(closest_words)}\n")

    return results

@app.get("/search/")
def search_documents(queries: List[str] = Query(...)):
    results = []
    logger.debug("TEST 2")
    logger.debug(queries)
    for query in queries:
        logger.debug(query)
        query_results = search_similar_docs(query)
        print(query_results)
        results.append({
            "query": query,
            "results": query_results
        })
    return results

# Pour lancer le serveur : uvicorn main:app --reload

# Maintenant, tu peux tester avec :
# GET /search/?queries=genetic&queries=biology

# Dis-moi si tu veux ajuster quelque chose ! 🚀
