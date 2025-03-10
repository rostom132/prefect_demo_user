from prefect import task
from model.constants import Gender

gender_fuzzy_mapper = {
    Gender.male : [
        'male',
        'm',
        'boy',
        'strong',
        'alpha'
    ],
    Gender.female : [
        'female',
        'f',
        'girl',
        'weak',
        'beta'
    ]
}

email_fuzzy_mapper = {
    'gmail.com': [
        'mail.com',
        'google.com',
        'gmail1.com',
        'gmail2.com',
        'gmail.comm'
    ],
    'outlook.com': [
        'outloook.com',
        'outloooook.com'
    ]
}

@task
def auto_correct_gender(value: str):
    print("auto_correct_gender old value: ", value)
    if value is None:
        return value

    new_value = value.lower()
    for gender in gender_fuzzy_mapper:
        if new_value in gender_fuzzy_mapper[gender]:
            value = gender
            break
        
    print("auto_correct_gender new value: ", value)
    return value

@task
def auto_correct_mail(value: str):
    print("auto_correct_mail old value: ", value)
    if value is None:
        return value
    
    index_of_at = value.rfind('@')
    if index_of_at == -1:
        return value
    
    pre_email = value[:index_of_at]
    post_email = value[index_of_at+1:]

    for email in email_fuzzy_mapper:
        if post_email in email_fuzzy_mapper[email]:
            value = pre_email + '@' +  email
            break
    
    print("auto_correct_mail old value: ", value)
    return value
