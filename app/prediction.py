import json
from watson_developer_cloud import VisualRecognitionV3

def predict(image_name):
    visual_recognition = VisualRecognitionV3(
        '2018-03-19',
        iam_apikey = IAM_API_KEY )
    with open(image_name, 'rb') as images_file:
        classes = visual_recognition.classify(
            images_file,
            threshold='0.5',
    	classifier_ids='AIidentifiescrops_102957661').get_result()
    print(json.dumps(classes, indent=2))
