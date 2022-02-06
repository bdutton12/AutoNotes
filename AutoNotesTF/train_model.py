from sklearn.model_selection import train_test_split
import numpy as np
from dataset import helpers
import tensorflow as tf
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def get_data(path):
    # Initialize data
    azLabels, azImg = helpers.create_az_dataset(path)
    mnistTrainLabels, mnistTrainImg, mnistTestLabels, mnistTestImg = helpers.create_dig_dataset()

    # Split AZ dataset into train and test
    testSize = float(len(mnistTestLabels) / len(mnistTrainLabels))
    azTrainImg, azTestImg, azTrainLabels, azTestLabels = train_test_split(azImg, azLabels, test_size=testSize)

    # Shift MNIST labels to make room for AZ dataset
    mnistTrainLabels = mnistTrainLabels + max(azLabels)+1
    mnistTestLabels = mnistTestLabels + max(azLabels)+1

    # concatenate datasets
    trainImg = np.concatenate((azTrainImg, mnistTrainImg),axis=0)
    trainLabels = np.concatenate((azTrainLabels, mnistTrainLabels))
    testImg = np.concatenate((azTestImg, mnistTestImg),axis=0)
    testLabels = np.concatenate((azTestLabels, mnistTestLabels))

    return trainLabels, trainImg, testLabels, testImg

def init_model(trainLabels):
    model = tf.keras.models.Sequential([
        # Note the input shape is the desired size of the image 150x150 with 3 bytes color
        tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(28, 28, 1)),
        tf.keras.layers.MaxPooling2D(2,2),
        tf.keras.layers.Conv2D(32, (3,3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2,2), 
        # Flatten and put through Dense network
        tf.keras.layers.Flatten(), 
        # 512 neuron hidden layer
        tf.keras.layers.Dense(512, activation='relu'), 
        # Only 1 output neuron. It will contain a value from 0-1
        tf.keras.layers.Dense(len(np.unique(trainLabels)), activation='softmax')  
    ])

    model.compile(optimizer=RMSprop(learning_rate=1e-4),
              loss='sparse_categorical_crossentropy',
              metrics = ['accuracy'])
    
    return model


def train_model():
    # Initialize datasets
    path = input("Input path to dataset: ")
    trainLabels, trainImg, testLabels, testImg = get_data(path)
    print("---Data Processed---")

    # Initialize model
    model = init_model(trainLabels)

    # Initialize image data gen to augment model
    trainGen = ImageDataGenerator(
      rescale=1./255,
      rotation_range=15,
      width_shift_range=0.1,
      height_shift_range=0.1,
      shear_range=0.1,
      zoom_range=0.2,
      horizontal_flip=False,
      fill_mode='nearest')

    testGen = ImageDataGenerator(rescale=1./255)

    # Create flow of images using generator
    trainingGenerator = trainGen.flow(trainImg, trainLabels, batch_size=50, shuffle=True)
    testingGenerator = testGen.flow(testImg, testLabels, batch_size=50, shuffle=True)

    # Fit model to training data
    history = model.fit(
      trainingGenerator,
      steps_per_epoch=500,  
      epochs=100,
      validation_data=testingGenerator,
      validation_steps=50,  
      verbose=2)
    
    model.save('char_classifer')

if __name__=="__main__":
  train_model()