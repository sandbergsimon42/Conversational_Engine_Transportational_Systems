# Thoughts from 30/3
<b> Day 1 </b>
First real day of the project where we ensamble and start implementing the NLP frameworks and research hwo they will work on the dataset. 

1. There is a possibility to create a rule-based handling of the issue, although this is not what we preffer. See in the main jupyter file and search for Rule-based NER to find this implementation. 
2. Possible thoughts about this is to look at the dependency parsing of a sentence to draw information of the strucutre of the sentence to pick up possible entities which may noto be known to the model from previous experience. 

# Thoughts from 31/3
<b>Day 2.</b> <br>
No real dataset have yet been shown, we have listened to two example audio files and done some manual transcribing to try to find the structure of the dialogues which happen. The goal of the day is to get a response from the dataprovider if we are going to generate own training data (this can give us the opportunity to develop an own NLP model and train it on the structure and use the transcriptions for testing) or if we are going to recieve transcribed and labeled data which can be used for either training or just specialize the pretrained models from spaCy.  <br><br>
We are a bit worried that the dataset will be quite late and therefore have held the discussion in the group (not among examiners or customer) to generate training data which we can handle and label from the middle of the next week if we have no further positive information about a dataset which we can use.<br> <b> DATE WHEN WE START GENERATE OWN DATA IF NO DATASET IS AVAILABLE:  9/4 </b>


1. To handle multiword NER we are now researching IOB or BILUO encodings of the data. Primary resources for this: 
 
<i>Spacy implementations of specializing pretrained models towards the BILOU encoding, pretty much training a model to recognize and predict the specialized NER tags.</i>  
```
https://towardsdatascience.com/extend-named-entity-recogniser-ner-to-label-new-entities-with-spacy-339ee597904
```
<i>Discussion of IOB implementation and how it would work training a model to recognize the tags.</i>
``` 
https://medium.com/swlh/approaching-a-named-entity-recognition-ner-end-to-end-steps-685735b4a2f9
```
<i>
Training spaCy NER on data, also check closer on the Entity linking to refer to the same entity even if it's not the same exact spelling by predicting hashes in the knowledgebase?: </i>

```
https://spacy.io/usage/linguistic-features (Look at the NER category - Accessing entity annotations and labels)
``` 

<i> Text classification (AKA topic classification or intentclassifciation)</i>
```
https://www.dataquest.io/blog/tutorial-text-classification-in-python-using-spacy/

spaCy documentation and implementation:
https://spacy.io/api/textcategorizer 
```

# Thoughts from 6/4
<b>Day 3.</b> <br>

No dataset has yet been given to us and this is starting to worry us. We will today start looking at alternative dialogue datasets to begin the developmnent of the NLP models to research if we have to retrain the pretrained datamodels which are available from spaCy. 

We do worry that the format of the data of the datasets we are finding do not follow the future data which we will recieve and therefore that we will be making unnecesary double work if we go to deep into this alternative dataset, yet we can not really do anything until we get any data to work with. 

Options:
1. ~~Work in text stuff such as the pair appendix which have to be made in final report.~~
2. <b>Find dataset to try implement NLP models.</b>
3. ~~Get in touch with Magnus earlier~~
4. ~~Try the audio -> text approach again (this does not give labels and would require maual labeling)~~

To have a model making corect predictions it must be trained to find the correct entities within a flowing text. We must find a dataset which contains dialogue-like text flow as this will be the closest to finding entities based on dependency arcs within a sentence as most new entities will be new entities which the model have no prior training on.

# Thoughts from 7/4
<b>Day 4.</b> <br>

Our concerns have been further strengthened. The audio data which we recieved in the examples do have such thick swedish accent that english NLP models have a hard time to automate the translations. We will retrieve the rest of the data this friday (9/4) and also get an NLP implementation which should handle speech to audio, although we do not believe it will outperform implementations by Microsoft and Google.

Our current plan is now instead to begin an implementation of a script which can generate training-data with identical structure to incoming dialogue structure from the example files. 

# Thoughts from 9/4
<b>Day 6.</b> <br>

A larger data-amount have been recieved today, about +16hrs of audio data have been recieved form an testsession where multiple operators acted as operators and drivers of vessles. 

```
A discussion have been held today as communication in the new data tells us that some of the audio also includes communication between vessles and not only information which are relevant to the operator as it's the operator that ahve told the vessle to communicate with another one. Because of this we choose to exclude analyzing this data and focus on communication which are primarily between a vessle and an operator. 
```

Unfortunatly the audiodata holds the same problems which we encountered earlier in the example data which we recieved earlier as the accent of the speakers are very swedish. This is a large problem when handling this kind of data and is a previously known problem when handling speech > text.

# Thoughts from 12/4
<b>Day 7.</b> <br>
Things start to get togheter with the trainingset generation. We've gotten transcriptions that kind of match the structure of the example audio files that ahve been given to us. We've today also worked with additional to further extend the intents, entities of the datastructure and also more intents. 

We must start to think about the need of analyzing the conversations where the operator is the first requester as these dialogues most likely will not be very usefull to be analyzed in the intent of help the operator prioritize whom they should talk to. 

<b>Question</b><br>
So the question is if we should only focus on dialogues where the vessles start the communication or add more such as when the operators start the coms?

# Thoughts from 13/4
<b>Day 8.</b> <br>
Focus today and tomorrow will be to have a finished and done set for extensions to be made thursday and friday to start training models during next week.

1. Tomorrow (wednesday) the focus will be to integrate a few new intents/topics of communication form the example files which we retrieved.
2. We will begin looking at how the data must be structured to have correct structure for spaCy models to be trained om them to handle NER and topic classification.
3. When we know the above we will begin implement these parts to the datageneration to hopefully begin implementing models during next week.

# Thoughts from 14/4
<b>Day 9.</b> <br>
Today we have begun to discuss the separation of training, validation and testdatasets. We have concluded: 
```
1. We must implement new entitites within the validation set which is not the same as in the training dataset.
2. The testdataset will be our manually transcribed datasets which will be around 20 dialogues of data, which is a very small testdataset yet it will be the most representative of true dialogues.
3. We may extend the testdataset further with this regard.
4. We will be using the same modules for generating data for validation and trainings.
```

We have begun to discuss how to find what the correct labels in the dataset is as this will be needed when we are starting to label data to train the NLP model during next week.

Begin to think of how we can split the data in the datacointainer to split up some of the words to only be used within the validationdataset and not be used in training, but first we must make sure that the genereation is working as intended. 

# Thoughts from 15/4
<b>Day 10.</b> <br>

Thoughts how to solve the labeling of NER:
1. When adding an entity of any kind (any of the entities within the datacontainer class) keep a seperate list of these entities within
the datacontainerclass or return a list of used entities (This might already be pretty much the nearby entities which can be found already implemented in the generate dialogue function.)
2. How should this be stored within the datasetfile? The spaCy NER model wants the format ("sentence", {"entities": [(start_index, end_index, "entity_class"), (more), (entities), (here), (on), (the), (previous), (format)]}) 

Thoughts of how the gold standard data should be formated:<br>
We hve concluded that the labvels should not conain submatches of other entitites, THIS WILL BE IMPLEMENTED TOMORROW (FRIDAY), we have ot find a good way to not include other matches (which are not the picked entity)

# Thoughts from 19/4
<b>Day 12.</b> <br>

The dataset are finally done and ready for training, todays session have been alot about handling the labels to the dataset to enable the spaCy model to train on the dataset. 

This weeks main purpose will be to keep implementing the NER implementations, think about how we should handle misspelled entities (if there's a way to identify then anyway) and in the later part of the week
start implementing topic classification, which most likely will be needing some adjusting on the labeling tactics used as of right now.

PRIO: 
we have to solve the overlapping entities in the labels.

# Thoughts from 20/4
<b>Day 13.</b> <br>

Thoughts from today:
We have expanded the multiple boat names to make it more difficult to predict entities. 
We could continue training this model on larger data but this would most likely need to include a validation dataset to make sure we are not overfitting the model to the entities which are found 
in the training dataset as this would decrease the performance of the model on new data.

TODO AFTER LUNCH:
1. Check if it's possible to use a validation dataset for each training iteration and check when the model starts to be overfit (lose accuracy over the validation set while still improving on the trainingset)
2. Find a "Good enough" benchmark of the NER model, or find a accuracy score which we can stand behind and think is good.
3. Start looking at topic classification?

Today was a good day.

** IMPORTANT **
We can now train and optimize the NER model to achieve higher accuracies, in this case we can try to find a larger dataset with the changes done today (which was to use the model which makes the best predictions 
on the validation set which is not used within the training). 


# Thoughts from 22/4
<b>Day 15.</b> <br>

We can not finalzie the NER model until we have transcribed a good amount of the "true data" which will be used as the final test dataset to truly check our accuracy of entities. 

1. How much data is needed for this test dataset? Is it enough with 20 dialogues? Should we spend more time than that to make sure our models are as good as we believe?
2. Should we do this now before we have done the topic classification to run them seperatly or should we wait with the transcribing task until we have a final dataset format as we will 
extend the dataset format for training and evaluating the topic classification? 
3. How much data should be used for training, as we can generate unlimited amounts of data we can use a million dialogues if needed but that would make the testdata such small dataset to test over and that may not be optimal.

We'll contiue focusing on writing the report today to make sure we don't fdall behind on the report writing and adding some of the results form the dataset generation and NER classification which have been achieved on the generated dataset. 

Add a section evaluating how well the models predict on the generated dataset in comparison to the testdataset which are strictly transcribed from the audiodata.

# Thoughts from 26/4
<b>Day 17.</b> <br>
This week prio is on geting the writing done in the report to be up to date with the writing before deep diving into the topic classification. We do need to do a few things:
1. Setup a meeting with Magnus to discuss definition of done, What is our goals with our models.
2. the first point should also be discussed with Rita to find what we are aiming for in respect to the bachelors thesis requirements.

```
RAPPORT:
Skriv om svårigheter med STT (speech to text) då man ska översätta entiteter då en standard STT kommer att predicta det ord den tror har störst sannolikhet är sagt, att de ska hitta de entiteterna måste tränas på något speciellt sätt för att detta ska prediktas. Men detta är ett STT problem och inte något som faller på vårt arbete.
```

TODO
**DO THE ABOVE MAILINGS TOMORROW ( TUESDAY )**

Seem to be able to predict the topics which we have so far.
Must gather information from Magnus/proffesional of what information is relevant to predict in the questions of what topics should be predicted. 


# Thoughts from 27/4
<b>Day 18.</b> <br>

Things we need to know forward:
<b><i> Rita </i></b>
1. Have a discussion with rita regarding size of data.
2. Discuss how many dialogues which should be needed as testset which awe have to manually transcribe and label.
3. What performance should we "settle" with.
4. How much we should consider the customer if there are no hard requirements from the customer when dealing with performance matters, are our good enough the baseline?

<b><i> Magnus </b></i>
1. What are the topics that should be predicted? Is there a expert or operator that we can talk to that can snwer this question?

Answers to these questions are available in the mail. 

Planned meeting with Magnus 13.30.

Make nice graphs showing divergent losses on the training dataset and the validation dataset. This is to show that we have choosen the best model as it performs the best on the validation data.

