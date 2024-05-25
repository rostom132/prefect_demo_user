from prefect import task
import pickle
from model.constants import Gender

# load
with open('./utils/gender_predictor.pkl', 'rb') as f:
    gender_predictor = pickle.load(f)

@task
def auto_correct_gender(userData):
    print('USERDATA ', userData)
    predict_rs = gender_predictor.predict([(float(userData['height']), float(userData['weight']))])
    if len(predict_rs) > 0 and predict_rs[0]:
        return Gender.male
    return Gender.female
