from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

questions = [
    "weather prediction",
    "crop disease",
    "contract price",
    "government scheme",
    "fertilizer usage",
    "hello"
]

answers = {
    "weather prediction": {
        "en": "Check the weather prediction section for rainfall details.",
        "ta": "மழை முன்னறிவிப்பை பார்க்க வானிலை பகுதியைச் செல்லுங்கள்.",
        "hi": "मौसम पूर्वानुमान अनुभाग देखें।"
    },
    "crop disease": {
        "en": "Use crop disease predictor to identify diseases.",
        "ta": "பயிர் நோய் கண்டறிதலை பயன்படுத்துங்கள்.",
        "hi": "फसल रोग भविष्यवाणी का उपयोग करें।"
    },
    "contract price": {
        "en": "Use contract predictor to analyze profit.",
        "ta": "ஒப்பந்த கணிப்பை பயன்படுத்தி லாபத்தை அறியுங்கள்.",
        "hi": "अनुबंध मूल्य भविष्यवाणी देखें।"
    },
    "government scheme": {
        "en": "Government schemes are available in scheme section.",
        "ta": "அரசு திட்டங்களை திட்டங்கள் பகுதியில் பார்க்கலாம்.",
        "hi": "सरकारी योजनाएँ योजना अनुभाग में उपलब्ध हैं।"
    },
    "fertilizer usage": {
        "en": "Use fertilizers based on soil test results.",
        "ta": "மண் பரிசோதனை அடிப்படையில் உரங்களை பயன்படுத்துங்கள்.",
        "hi": "मिट्टी परीक्षण के अनुसार उर्वरक उपयोग करें।"
    },
    "hello": {
        "en": "Hello Farmer! How can I help you?",
        "ta": "வணக்கம் விவசாயி! நான் எப்படி உதவலாம்?",
        "hi": "नमस्ते किसान! मैं आपकी कैसे मदद कर सकता हूँ?"
    }
}

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(questions)

def chatbot_response(user_input, lang="en"):
    user_vec = vectorizer.transform([user_input])
    similarity = cosine_similarity(user_vec, X)
    index = similarity.argmax()
    key = questions[index]
    return answers[key][lang]
