# AI-Identifies-Crops

### List of contents

- [Introduction](#introduction)
- [Working](#working)
- [Installation](#installation)
- [Running](#running)


## Introduction
---
[(Back to top)](#list-of-contents)

- Dataset consists of 10 crops commonly found in India. Dataset is collected from different websites using web scraping and with the use of google images.  
- The labels predicted by the model, Information regarding the crop and user's geolocation information (at the time of upload) are also added to the database. 
- This application can be utilised for data collection by organisations. 
- The image when uploaded using forms will be sent to an image hosting service that will return the url of image which is stored in the database. This is an alternative to storing images as binary object in the database.

Note : The data used for training the model has not been open sourced yet.For dataset one may contact through email associated with this github account (shown on the profile).

## Working
---
[(Back to top)](#list-of-contents)

## Architectural Diagram
![img](https://imgur.com/K9R2ABT.png)

## Home Page
![img](https://imgur.com/Gkd4fVa.png)

## Prediction Page
![img](https://imgur.com/aQTPcp4.png)


### Model is also trained on negative images to identify a non crop image. Whenever it detects a non crop image, the user is directed to the following support page.

![img](https://imgur.com/KbHPOTu.png)

## Database

### Storing Image URL
![img](https://imgur.com/ynKGkIQ.png)


### Storing Image as binary object
![img](https://imgur.com/AKJZ8Ic.png)


## Installation
---
[(Back to top)](#list-of-contents)

These instructions assume you have `git` installed for working with Github from command window.

1. Clone the repository, and navigate to the downloaded folder. Follow below commands.
```
git clone https://github.com/pswaldia/AI-Identifies-Crops.git
cd AI-Identifies-Crops

```

2. Creating python virtual environment using virtualenv package using following lines of code.

NOTE: For this step make sure you have virtualenv package installed.

```
virtualenv venv
source venv/bin/activate

```

3. Install few required pip packages, which are specified in the requirements.txt file .
```
pip3 install -r requirements.txt

```


