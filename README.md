# AutoNotes
A simple website with an integrated TensorFlow convolutional neural network for handwriting classification.

I built this project as an attempt to further my understanding of two areas that are of great interest to me - machine learning and backend development. Throughout this project I had to conquer several challenges that were completely new to me:
 
 - Find an affordable and powerful hosting service
 - Integrate a PostgreSQL database
 - Design and implement a user assignment system for posts
 - Deploy a full project to a hosting site
 - Learn dJango and utilize its capabilities
 - Understand how to use OpenCV to pre-process images

As you can see, I essentially jumped into entirely unknown territory with this. I was unfamiliar with practically all of the libraries/frameworks used. In fact, TensorFlow was the only library that I had prior experience in. However, this didn't prevent me from deploying the initial form of this project within two weeks of beginning, although it took countless hours of research and design. In the future, I hope to revisit this and implement a few changes, number one being a more accuracte neural network.

If you have any questions or would like to contact me, feel free to reach out at: bdutton12@outlook.com


Tensorflow training was implemented using the MNIST 0-9 handwriting dataset, as well as the Kaggle A-Z handwriting dataset. They are available at:

http://yann.lecun.com/exdb/mnist/
https://www.kaggle.com/sachinpatel21/az-handwritten-alphabets-in-csv-format

Tensorflow model training script, as well as image running script is visible in the AutoNotesTF folder. It is not necessary for the project to run with dJango but is included for reproducability.

dJango's secret keys, as well as email information is stored locally in an environ file. This is to prevent the leaking of my passwords from this GitHub repo. If you attempt to recreate this project, simply swap the following variables in AutoNotes/settings.py to your own information:
 - dJango Secret Key
 - Email Host
 - Email username
 - Email password

If you swap these, you should be good to go!