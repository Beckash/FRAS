from PIL import Image
from PIL import Image as im
from matplotlib import pyplot
from mtcnn import MTCNN
from numpy import asarray
from numpy import savetxt

# import constant
from facial_recognition_based__attendance_system_app.FacialRecognition.vggModelFinal import VggModel

# from vggModelFinal import VggModel


class MTCnnDetector:
    # answer = [0, 0, [0, 0]]
    answer = ""

    def __init__(self, image_path, store_flag=False, plot=False):
        self.detector = MTCNN()
        self.image = image_path
        self.store_flag = store_flag
        self.process_image(plot)

    @staticmethod
    def control_all(image_path, store_flag=False, plot=False):
        face_detector = MTCnnDetector(image_path, store_flag, plot)
        return face_detector.answer

    def process_image(self, plot):
        faces = self.__detect_face()
        resized_face_list = []
        index = 1
        for f in faces:
            extracted_face = self.__extract_face(f)
            resized_face = self.__resize_img_to_face(extracted_face)
            resized_face_list.append(resized_face)
            index = index + 1
            self.select_store_or_predict(resized_face, index)
            if plot:
                self.__plot_face(resized_face)
        return resized_face_list

    def select_store_or_predict(self, face, index):
        if self.store_flag:
            self._save_images_format(face, index)
        else:
            model = VggModel()
            self.answer = model.predict(face)

    def _save_images_format(self, face, index):
        sample_images_nomalized = face
        data = im.fromarray(sample_images_nomalized)  # creating image object of above sample_images_nomalized
        if index < 10:
            image_name = "E:/Final Project/Implementation/FinalProject/dataset/datasetFinal/butera/bute" + str(
                index) + ".jpg"
            data.save(image_name)  # saving the final output as a PNG file
        else:
            image_name = "E:/Final Project/Implementation/FinalProject/dataset/datasetFinal/butera/sisay" + str(
                index) + ".jpg"
            data.save(image_name)  # saving the final output as a PNG file

    def _save_images_csv(self, face, index):
        sample_images = face
        sample_images = sample_images.reshape(1, -1)  # To make it 2D
        image_name = "C:/Users/Hello/FR/photos/nomalizedImages/" + str(index) + "dataedited.csv"
        savetxt(image_name, sample_images, delimiter=',')

    def __detect_face(self):
        return self.detector.detect_faces(self.image)

    def __extract_face(self, face):
        x1, y1, width, height = face['box']
        x2, y2 = x1 + width, y1 + height
        return self.image[y1:y2, x1:x2]

    def __resize_img_to_face(self, face):
        image = Image.fromarray(face)
        image = image.resize((243, 320))
        return asarray(image)

    def __plot_face(self, face):
        pyplot.imshow(face)
        pyplot.show()
