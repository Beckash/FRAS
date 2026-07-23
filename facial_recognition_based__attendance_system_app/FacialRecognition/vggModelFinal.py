# -*- coding: utf-8 -*-
import os
import numpy as np
import keras
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input, decode_predictions
import matplotlib.pyplot as plt
from numpy import expand_dims

from tensorflow.keras import Input
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.layers import MaxPooling2D, Dense, Flatten, Convolution2D
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model


from facial_recognition_based__attendance_system_app.FacialRecognition import constant

# import constant

class VggModel:
    dir_path_train = r"C:\Users\becka\Desktop\FRAS\media\training_data"
    dir_path_test = r"C:\Users\becka\Desktop\FRAS\media\testing_data"
    # dir_path_train = "D:/Projects/AI Projects/Datasets/preprocessed_image/training_data"
    # dir_path_test = "D:/Projects/AI Projects/Datasets/preprocessed_image/testing_data"
    number_of_samples = 0
    all_class_names = os.listdir(dir_path_train)
    number_of_classes = len(all_class_names)

    def __init__(self, flag=True):

        if flag:
            self.init_model()
            opt = keras.optimizers.Adam(learning_rate=0.0001)
            self.vgg.compile(loss=keras.losses.binary_crossentropy,
                             optimizer=opt,
                             metrics=[constant.METRIC_ACCURACY])

    def init_model(self):

        base_model = VGG16(weights=constant.IMAGENET, include_top=False,
                           input_tensor=Input(shape=(constant.IMG_WIDTH,
                                                     constant.IMG_HEIGHT, 3)), pooling='max',
                           classes=self.number_of_classes)
        # base_model.summary()

        for layer in base_model.layers:
            layer.trainable = False

        x = base_model.get_layer('block5_pool').output
        # Stacking a new simple convolutional network on top of it
        x = Convolution2D(64, 3)(x)
        x = MaxPooling2D(pool_size=(2, 2))(x)
        x = Flatten()(x)
        x = Dense(constant.NUMBER_FULLY_CONNECTED, activation=constant.RELU_ACTIVATION_FUNCTION)(x)
        x = Dense(self.number_of_classes, activation=constant.SOFTMAX_ACTIVATION_FUNCTION)(x)

        self.vgg = Model(inputs=base_model.input, outputs=x)
        # self.vgg.summary()

    def get_model(self):  # , model_weight_url):
        saved_model = load_model("FinalTrainedModel/vgg16.h5")
        # saved_model = load_model(model_weight_url)
        return saved_model

    def train(self, num_epochs=10, num_batches=10, flag=True):

        datagen = ImageDataGenerator(rescale=1. / 255,
                                     shear_range=0.2,
                                     zoom_range=0.2,
                                     rotation_range=20,
                                     width_shift_range=0.2,
                                     height_shift_range=0.2,
                                     horizontal_flip=True,
                                     fill_mode='nearest')

        # --- FIX: Added batch_size=num_batches ---
        traindata = datagen.flow_from_directory(
            self.dir_path_train,
            target_size=(constant.IMG_WIDTH,
                         constant.IMG_HEIGHT),
            batch_size=num_batches) 
        
        self.number_of_samples = traindata.samples
        
        if flag:
            # --- FIX: Added batch_size=num_batches ---
            testdata = datagen.flow_from_directory(
                self.dir_path_test,
                target_size=(constant.IMG_WIDTH,
                             constant.IMG_HEIGHT),
                batch_size=num_batches)

            number_of_samples_test = testdata.samples

            checkpoint = ModelCheckpoint("FinalTrainedModel/vgg16.h5",
                                         monitor=constant.METRIC_ACCURACY, verbose=1, save_best_only=True,
                                         save_weights_only=False, mode='auto', save_freq='epoch')
            
            early = EarlyStopping(monitor='val_loss', min_delta=0, patience=5, verbose=1, mode='auto', restore_best_weights=True)

            self.vgg.fit(
                traindata,
                steps_per_epoch=self.number_of_samples // num_batches,
                validation_data=testdata,
                validation_steps=number_of_samples_test // num_batches, 
                epochs=num_epochs,
                callbacks=[checkpoint, early])

            # Remove the extra variable assignment that was here in your original code if not needed, 
            # or keep strictly to your structure as I have done above.

    def __process_img(self, img):

        img = image.img_to_array(img)

        return preprocess_input(expand_dims(img, axis=0))

    def predict(self, img):  # model_weight_url):
        pixels = self.__process_img(img)
        # saved_model = self.get_model(model_weight_url)
        saved_model = self.get_model()
        output = saved_model.predict(pixels)
        # output = saved_model.predict(pixels)
        # return output
        return self.print_predication_result(output)
    


    def print_predication_result(self, output):
        # 1. Map folder names to indices
        dict_of_classes = {i: self.all_class_names[i] for i in range(0, self.number_of_classes)}
        
        # 2. Get the index with the highest probability and the score itself
        index = np.argmax(output[0])
        confidence_score = output[0][index]
        
        # 3. Get the name associated with that index
        class_value = self.id_class_name(index, dict_of_classes)
        
        # 4. Display the results in the terminal for debugging
        print(f"\n--- Model Analysis ---")
        print(f"Top Prediction: {class_value}")
        print(f"Confidence Score: {confidence_score:.4f}")
        
        # 5. Return the name if confidence is at least 50%
        # Your old code required ~100%, which is why it was returning ""
        if confidence_score >= 0.50:
            return class_value
        else:
            return "Unknown (Low Confidence)"
        


    def id_class_name(self, class_id, classes):
        for key, value in classes.items():
            if class_id == key:
                return value

    def evaluate(self):
        score = self.get_model().evaluate(verbose=0)
        print("%s: %.2f%%" % (self.get_model().metrics_names[1], score[1] * 100))

    def get_number_class_samples(self):
        return self.number_of_classes, self.number_of_samples

    def plot_accuracy_loss(self, epochs):
        # loss
        acc = self.get_model().history['accuracy']
        val_acc = self.get_model().history['val_accuracy']

        loss = self.get_model().history['loss']
        val_loss = self.get_model().history['val_loss']

        epochs_range = range(epochs)

        plt.figure(figsize=(8, 8))
        plt.subplot(1, 2, 1)
        plt.plot(epochs_range, acc, label='Training Accuracy')
        plt.plot(epochs_range, val_acc, label='Validation Accuracy')
        plt.legend(loc='lower right')
        plt.title('Training and Validation Accuracy')

        plt.subplot(1, 2, 2)
        plt.plot(epochs_range, loss, label='Training Loss')
        plt.plot(epochs_range, val_loss, label='Validation Loss')
        plt.legend(loc='upper right')
        plt.title('Training and Validation Loss')
        plt.show()

    # Evaluating the model on test datasets
    def evaluating_the_model(self, test_generator):
        self.get_model().evaluate_generator(test_generator)
