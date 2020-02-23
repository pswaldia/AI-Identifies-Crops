from app import app
import ipinfo
import os
import csv
#prediction return
from app.prediction import predict
#flask utilities
from flask import Flask, flash, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
#to prevent warnings
import warnings
warnings.filterwarnings('ignore')
import base64
import requests

import json
from watson_developer_cloud import VisualRecognitionV3

ENV='prod'
if ENV=='dev':
    app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:Pradeep.1@localhost/ISRO_Crop_DB'
else:
    app.debug=False
    app.config["SQLALCHEMY_DATABASE_URI"]='postgres://eioqoznjiacycv:36222997e5326fb6d2b54ecd0e08eaf5a779f4f7d7eb156da01f4c6270816a77@ec2-54-174-229-152.compute-1.amazonaws.com:5432/ddcaac2ve4crog'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db=SQLAlchemy(app)

class Image(db.Model):
    __table__name='image_info'
    id=db.Column(db.Integer,primary_key=True)
    image_url=db.Column(db.String(200))
    predicted_label=db.Column(db.String(200))
    user_city=db.Column(db.String(200))
    user_country=db.Column(db.String(200))
    user_lat=db.Column(db.String(200))
    user_long=db.Column(db.String(200))
    def __init__(self,image_url,predicted_label,user_city,user_country,user_lat,user_long):
        self.image_url=image_url
        self.predicted_label=predicted_label
        self.user_city=user_city
        self.user_country=user_country
        self.user_lat=user_lat
        self.user_long=user_long

db.create_all()
#for storage
UPLOAD_FOLDER = "/Users/pswaldia1/crop_identification/app/static/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def predict(image_url):
    iam_api_key = ""

    visual_recognition = VisualRecognitionV3(
        '2018-03-19',
        iam_apikey= iam_api_key)

    classes = visual_recognition.classify(
        url=image_url,
        threshold='0.5',
	classifier_ids='AIidentifiescrops_102957661').get_result()
    dictt=json.loads(json.dumps(classes, indent=2))
    to_return=dictt["images"][0]["classifiers"][0]['classes']
    if len(to_return)==0:
        return None
    return dictt["images"][0]["classifiers"][0]['classes'][0]

info={'Bajra': 'Bajra known as "Pear Millet" belongs to the family of Gramenea. Most prominently grown in Africa and Asia.',
 'Coffee': 'Coffea is a genus of flowering plants in the family Rubiaceae. Coffea species are shrubs or small trees native to tropical and southern Africa and tropical Asia.',
 'Cotton': 'Cotton is a soft, fluffy staple fiber that grows in a boll, or protective case, around the seeds of the cotton plants of the genus Gossypium in the mallow family Malvaceae.Cotton is a kharif crop which requires 6 to 8 months to mature. Its time of sowing and harvesting differs in different parts of the country depending upon the climatic conditions.',
 'Maize': 'Corn, (Zea mays), also called Indian corn or maize, cereal plant of the grass family (Poaceae) and its edible grain.',
 'Oilseed': 'Oilseed crops are primarily grown for edible oil. Recently, oilseeds attracted more attention due to an increasing demand for their healthy vegetable oils, livestock feeds, pharmaceuticals, biofuels, and other oleochemical industrial uses. ',
 'Rice': "Rice is the seed of the grass species Oryza sativa (Asian rice) or Oryza glaberrima (African rice). As a cereal grain, it is the most widely consumed staple food for a large part of the world's human population, especially in Asia.",
 'Sugarcane': 'Sugarcane, or sugar cane, or simply cane, are several species of tall perennial true grasses of the genus Saccharum, tribe Andropogoneae, used for sugar production.',
 'Tea': 'Camellia sinensis is a species of evergreen shrub or small tree whose leaves and leaf buds are used to produce tea.',
 'Tobacco': 'Tobacco is the common name of several plants in the Nicotiana genus and the Solanaceae (nightshade) family.',
 'Wheat': 'Wheat is a grass widely cultivated for its seed, a cereal grain which is a worldwide staple food.'}
rainfall={'Bajra': ' 40-75 cm',
 'Coffee': '150-200 cm',
 'Cotton': ' 60-100 cm',
 'Maize': ' 60-100 cm',
 'Oilseed': ' 50-75 cm',
 'Rice': '150-350 cm',
 'Sugarcane': '120-350 cm',
 'Tea': '150-250 cm',
 'Tobacco': ' 60-150 cm',
 'Wheat': ' 30-100 cm'}
temp={'Bajra': '20° -  30° C',
 'Coffee': '23° -  28° C',
 'Cotton': '24° - 30°C',
 'Maize': '18° -  27° C',
 'Oilseed': '20° - 30° C',
 'Rice': '20° -  28° C',
 'Sugarcane': '20° - 26°C',
 'Tea': '13° -  28°C',
 'Tobacco': '20° -  30° C',
 'Wheat': 'Around 15° C'}
soil={'Bajra': 'It thrives best in black cotton soils, sandy loam soils having good drainage.',
 'Coffee': 'Coffee can be grown on lots of soils but the ideal types are fertile volcanic red earth or deep sandy loam.',
 'Cotton': 'Cotton grows best on sandy soils with a minimum 5.5 soil pH and on clay soils with a minimum 5.8 soil pH. Soils should be well drained.',
 'Maize': 'Maize can be grown successfully in variety of soils ranging from loamy sand to clay loam.',
 'Oilseed': 'It is grown on red sandy loams in the peninsular India and on light alluvial soils of the Satluj-Ganga plain.',
 'Rice': 'Fertile riverine alluvial soil is best for rice cultivation.',
 'Sugarcane': 'A well drained, deep, loamy soil with a bulk density of 1.1 to 1.2 g/cm3 (1.3-1.4 g/cm3 in sandy soils) and total porosity with an adequate balance between pores of various sizes.',
 'Tea': 'Tea grows well on high land well drained soils having a good depth, acidic pH in the range 4.5 to 5.5 and more than 2% organic matter.',
 'Tobacco': 'A light, sandy soil is required for flue-cured, light tobacco. ',
 'Wheat': 'Loam soil is the best for wheat cultivation. Clay and sandy loam soils can also used for wheat cultivation.'}
producer={'Bajra': 'Rajasthan, Maharashtra',
 'Coffee': 'Karnataka , Kerala',
 'Cotton': 'Tamil Nadu, Punjab',
 'Maize': 'Karnataka , Rajasthan',
 'Oilseed': 'Gujarat, Rajasthan',
 'Rice': 'West Bengal , UP',
 'Sugarcane': 'UP, Maharashtra, Karnataka',
 'Tea': 'Assam, West Bengal, Tamil Nadu',
 'Tobacco': 'Andhra Pradesh',
 'Wheat': 'UP, Punjab'}

def return_location():
    handler=ipinfo.getHandler(access_token=os.environ.get("IPINFO_KEY"))
    details=handler.getDetails()
    info_dict={"latitude":details.latitude,"longitude":details.longitude,"country":details.country_name}
    info_dict["city"]=details.all["city"]   #city of upload
    info_dict["region"]=details.all["region"]  #region of upload
    info_dict["ip"]=details.all["ip"]   #ip address of the upload device
    return info_dict

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#hard coded descriptions

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file1 = request.files['file']
        # if user does not select file, browser also submit an empty part without filename
        if file1.filename == '':
            flash('No selected file')
            return redirect(request.url)
        image_base64=base64.b64encode(file1.read())
        # image_base64=image_base64.decode('utf-8')
        # filename = secure_filename(file1.filename)
        # file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # with open(os.path.join(app.config['UPLOAD_FOLDER'], filename),"rb") as file:
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": "",
            "image": image_base64,
        }

        res = requests.post(url, payload)
        dicttt=dict(json.loads(res.text))
        image_url=dicttt['data']['url']
        location=return_location()
        preds=predict(image_url)
        if preds==None:
            return render_template("error404.html")
        data = Image(image_url,preds["class"],location['city'],location['country'],location['latitude'],location['longitude'])
        db.session.add(data)
        db.session.commit()
        class_label=preds['class']
        return render_template("1.html",image_url=image_url,label=preds['class'],score=preds['score'],rainfall=rainfall[class_label],temp=temp[class_label],soil=soil[class_label],producer=producer[class_label],info=info[class_label])
    return render_template('index.html')
