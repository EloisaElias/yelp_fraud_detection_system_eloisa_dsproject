# yelp_fraud_detection_system_eloisa_dsproject

## Detecting fake reviews in Yelp using Spark 

###Eloisa Tran - Data Scientist
####Seattle - Galvanize Student
####Oct 2015

###Description

***Public opinion in this country is everything***
***-Abraham Lincoln***

Building and maintaining trust is fundamentally important for an online company. The proliferation of fake reviews is a huge problem for e-commerce and recommendation sites that depend on user ratings. “At the end of the day, if consumers don’t trust the content, then there is no value for anyone,” says Vince Sollitto, a spokesman for the local review site Yelp. In E-commerce, detecting and filtering fraud reviews is important in order to earn the trust of the customers (users).

Currently, fraud reviews are prevalent due to misuse of sites like [marketplace platforms for services performed by its users such as Fiverr.com.](http://www.geekwire.com/2015/after-conducting-undercover-sting-amazon-files-suit-against-1000-fiverr-users-over-fake-product-reviews/)

![AWS Lambda architecture](https://s3-us-west-2.amazonaws.com/fake-reviews-project/fake_reviews_fiver.png)

Companies have been particularly aggressive about fighting fraudulent reviews.

* [2015 Harvard study identified 16% of reviews as fake.](http://officialblog.yelp.com/2013/09/fake-reviews-on-yelp-dont-worry-weve-got-your-back.html)


####Project presentation

In this project, I investigate through machine learning the extent and patterns of review fraud on the popular consumer review platform Yelp.com. We cannot directly observe which reviews are fake, we focus on reviews that Yelp's algorithmic indicator has identified as fraudulent.  Using this proxy, I present my project replicating one of [the best models](http://www.bloomberg.com/bw/magazine/a-lie-detector-test-for-online-reviewers-09292011.html) for detecting fake online reviews using AWS and python machine learning tools.


![AWS Lambda architecture](https://s3-us-west-2.amazonaws.com/fake-reviews-project/01_project_presentation.png)
 
 
#### Data Source
 
For the purpose of this project the Yelp Challenge Dataset is considered genuine reviews. Consist of 35k reviews that include restaurants data from U.S.: Pittsburgh, Charlotte, Urbana-Champaign, Phoenix, Las Vegas, and Madison.

Fake reviews were a challenge, for the purpose of this project, with the help of Jason fennell, the Director of Data Science at Yelp; I have determined that the non-recommended reviews are the most readily available source of label for questionable reviews. Fraudulent reviews are crawled from yelp.com not recommended review section.  These reviews are put under not recommended review section because these are classified as fake/ suspicious reviews. Yelp runs all its review through an anti-fraud algorithm, and is used in yelp to filter these types of deceptive reviews. The number of suspicious reviews extracted is 35k.

Implementing text preprocessing in order to obtain the reviews data frames in a clean and organized manner.

Training dataset has a ratio of 50:50 i.e. it contains 50% of fake reviews and 50% of truthful reviews.

![AWS Lambda architecture](https://s3-us-west-2.amazonaws.com/fake-reviews-project/02_data_source.png)

#### Feature Construction 

* N-gram presence
* Review length
* Friends Count
* Naive Bayes classifier


#### Model Construction
##### Model_1

Using TF-IDF in order to obtain the n-gram presence as features for our model_1. 

Training data obtained in the previous steps is used to train the Naïve Bayes Classifier

![AWS Lambda architecture](https://s3-us-west-2.amazonaws.com/fake-reviews-project/03_model_01.png)


##### Model_2

I trained model_2 with data obtained from the results of model_1(the Naïve Bayes Classifier), as an extra feature including review length.


![AWS Lambda architecture](https://s3-us-west-2.amazonaws.com/fake-reviews-project/04_model_2.png)

#### Results

The detection accuracy percentage varies with different sets of test reviews, we have used 5 fold cross validation technique by considering folds of trained dataset and test dataset in the ratio of 75:25.  Test frequency accuracy obtained for n-gram presence and review lengths.

#### Further Work - Project stage_2

In process_

This project was developed with basic tools and in a two weeks timeline and focus in how to detect fake reviews using supervised learning with linguistic features only. The same model can also be implemented with a combination of behavioral and linguistic features by using supervised, unsupervised or semi-supervised learning techniques. 

Including a new dataset - web scraping yelp reviews directly from platform Yelp.com.

#### Further Work - Project stage_3

In stage_3 the vision of this project is to develop a data processing model that detects fake/fraudulent reviews in two sections near real-time processing for immediate graph detection performance of the model and a processing batch where I would like to apply more training and bigger and better data to the model.


![AWS Lambda architecture](https://s3-us-west-2.amazonaws.com/fake-reviews-project/05_yelp_lambda_architecture.png)
