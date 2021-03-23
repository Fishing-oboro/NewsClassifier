from create_csv import wdv_model as wm
from create_csv import main as cm
from sklearn.metrics import accuracy_score

data = wm.load_csv(r'C:\Users\turib\Desktop\data\sample1page.csv')

result = [cm.text_categorize(article) for article in data['articles']]
answer = data['categories']
score = accuracy_score(answer, result)

# 86%くらいだった
print(score)

