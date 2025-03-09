import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
import cv2
import uuid
import numpy as np

# Set the values of your computer vision endpoint and computer vision key
# as environment variables:
try:
    endpoint = os.environ["VISION_ENDPOINT"]
    key = os.environ["VISION_KEY"]
except KeyError:
    print("Missing environment variable 'VISION_ENDPOINT' or 'VISION_KEY'")
    print("Set them before running this sample.")
    exit()

# Create an Image Analysis client
client = ImageAnalysisClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)

def load_image(img_url):
    # Load the image
    with open(img_url, "rb") as image_stream:
        image = image_stream.read()
    return image

def get_set_of_text_and_position_from_results(results):
    # Get the text and position of the text in the image
    textSet = {}
    origTextSet = results["readResult"]["blocks"][0]["lines"]
    for index, sets in enumerate(origTextSet):
        score = round(getScore(sets) * 100, 3)
        textSet[index] = {
            "text": sets["text"],
            "position": sets["boundingPolygon"],
            "words": sets["words"],
            "score": score
        }
    return textSet

def getScore(value):
    # Get the score of the text in the image
    score_count = 0
    score = 0
    for confidence in value["words"]:
        score+= confidence["confidence"]
        score_count+=1
    score = score/score_count
    return score

def add_key_to_image(img_url, textSet):
    # Add the text to the image
    image = cv2.imread(img_url)
    for key, value in textSet.items():
        text = value["text"]

        #取得左上角及右下角座標
        posLTx = value["position"][0]["x"]
        posLTy = value["position"][0]["y"]
        posRBx = value["position"][2]["x"]
        posRBy = value["position"][2]["y"]

        # Draw the text on the image
        cv2.rectangle(image, (posLTx, posLTy), (posRBx, posRBy), (0, 255, 0), 2)
        cv2.putText(image, str(key), (posRBx - 15, posRBy), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    imgUrl = f"./outputs/{uuid.uuid4().hex}_output.jpg"
    cv2.imwrite(imgUrl, image)
        
    return imgUrl

def ocr_analysis(img_url):
    # Analyze the image
    image = load_image(img_url)
    results = client.analyze(image, visual_features=[VisualFeatures.READ]) #呼叫API取得結果
    try:
        textSet = get_set_of_text_and_position_from_results(results.as_dict()) #取得結果中的文字與位置
    except:
        return None

    outputImgUrl = add_key_to_image(img_url, textSet) #將文字加到圖片上
    imgFileName = os.path.basename(outputImgUrl)

    return textSet, imgFileName