import importlib.util
import sys

package = "deepface"

if package in sys.modules:
    print(f"{package!r} already in sys.modules")
elif (spec := importlib.util.find_spec(package)) is not None:
    # If you choose to perform the actual import ...
    module = importlib.util.module_from_spec(spec)
    sys.modules[package] = module
    spec.loader.exec_module(module)
    print(f"{package!r} has been imported")
else:
    print(f"can't find the {package!r} module")


from deepface import DeepFace


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
