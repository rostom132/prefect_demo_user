from prefect import task
import pickle

# load
with open('./utils/gender_predictor.pkl', 'rb') as f:
    gender_predictor = pickle.load(f)

@task
def auto_correct_gender(value, userData):
    print('USERDATA ', userData)
    predict_rs = gender_predictor.predict([(userData['height'], userData['weight'])])
    if len(predict_rs) > 0 and predict_rs[0]:
        return 'MALE'
    return 'FEMALE'

correcter_mapping = {
    'gender': auto_correct_gender
}

def auto_correct(field: str, value, userData):
    print('RUN correcter with field: ', field)
    if field in correcter_mapping:
        return correcter_mapping[field](value, userData)
    return None