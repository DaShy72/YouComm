from textblob import TextBlob
from langdetect import detect

# Функция для классификации
def classify_comment(text):
    try:
        if detect(text) != 'en':
            return "neutral"  # если не английский — считаем нейтральным
    except:
        return "neutral"

    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity  # от -1 до 1

    if polarity > 0.4:
        return "good"
    elif polarity < -0.4:
        return "angry" if any(word in text.lower() for word in ['hate', 'stupid', 'idiot']) else "bad"
    elif -0.4 <= polarity <= 0.4:
        return "neutral"

def result_classifity(list_comments):
    # Чтение комментариев и классификация
    categories = {
        "angry": [],
        "good": [],
        "bad": [],
        "neutral": [],
    }


    for line in list_comments:
        comment = line.strip()
        if comment:
            category = classify_comment(comment)
            categories[category].append(comment)
    result = []
    for cat in categories.values():
        result.append(len(cat))

    return result
