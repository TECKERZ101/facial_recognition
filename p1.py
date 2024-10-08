from deepface import DeepFace

def process_face():
    objs = DeepFace.analyze(
    img_path = "img.jpg", # Accepts a jpg as an input (has to be named img.jpg)
    actions = ['age', 'gender', 'emotion'],
    )


    item = objs[0]




    gender_dict = item['gender']
    dominant_gender = item['dominant_gender']


    age = item['age']


    dominant_emotion = item['dominant_emotion']


    print("Age:", age, "\nEmotion:", dominant_emotion, "\nGender:", dominant_gender)

process_face()