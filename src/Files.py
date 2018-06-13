
# encoding: utf-8

import cv2, os
import TextInterface as txtIf

delimiter = '\\'
datasetPath = '..'+delimiter+'sources'+delimiter+'dataset'
facesDatasetPath = '..'+delimiter+'sources'+delimiter+'facesDataset'
xmlFolderPath = '..'+delimiter+'sources'+delimiter+'xml'
xmlFile = 'haarcascade_frontalface_default.xml'
recognizerFolderPath = ".." + delimiter + 'sources' + delimiter + 'recognizer'
ymlFile = 'trainedData.yml'
recognizerDict = 'dictionary_ID_labels.txt'
recognizerInfo = 'info.txt'
extensionJPG = '.jpg'
extensionPNG = '.png'
defaultImage = "default" + extensionPNG
defaultImagePath = '..'+delimiter+'sources'
fileDelimiter = ', '

def getFileName(defaultFile=defaultImage, folder=defaultImagePath):
    return folder + delimiter + defaultFile

def loadImage(fullName=getFileName()):
    txtIf.printMessage(txtIf.MESSAGES.LOADING_FILE, fullName)
    return cv2.imread(fullName)

def getLoadedXml():
    return cv2.CascadeClassifier(getFileName(xmlFile, xmlFolderPath))

def getReco():
    return cv2.face.LBPHFaceRecognizer_create()

def loadInfo(nameImage=None):
    name = " - "; age = " - "; birth_place = " - "; job = " - "
    if nameImage is not None:
        with open(recognizerFolderPath + delimiter + recognizerInfo) as f:
            for line in f:
                # Ejemplo de lo que nos encontramos en este fichero
                # alexandra_daddario, Alexandra Daddario, 32, Nueva York, Actriz
                p = line.split(fileDelimiter)

                # Para quitar la primera parte del nombre (face_) y quedarnos con el resto
                # print(p[0].split("face_",1)[1])

                if p[0].__eq__(nameImage):
                    name = p[1];
                    age = p[2];
                    birth_place = p[3];
                    job = p[4]
                    break
    info = {"name": name, "age": age, "birth_place": birth_place, "job": job}
    return info

def filesOnDir(path=datasetPath):
    return os.listdir(path)

def saveImage(image, path):
    txtIf.printMessage(txtIf.MESSAGES.SAVING_IMAGE, path)
    cv2.imwrite(path, image);

def writeInfoNewImage(stringInfo):
    with open(recognizerFolderPath + delimiter + recognizerInfo, "a") as f:
        f.write(stringInfo)

def removeLine(nameImage):
    with open(recognizerFolderPath + delimiter + recognizerInfo, "r") as f:
        lines = f.readlines()
    with open(recognizerFolderPath + delimiter + recognizerInfo, "w") as f:
        for line in lines:
            if line.split(fileDelimiter)[0] != nameImage:
                f.write(line)
            else:
                txtIf.printError(txtIf.ERRORS.IMAGE_ALREADY_ON_DATABASE)

def doWhenNewImage(img):
    # info: iName, name, age, bPlace, job
    info = txtIf.askInfoNewImage()
    # Sobreescribimos la línea que corresponda a la misma imagen
    removeLine(info[0])
    writeInfoNewImage('\n' + info[0] + fileDelimiter + info[1] + fileDelimiter + info[2] + fileDelimiter + info[3] + fileDelimiter + info[4])
    saveImage(img, datasetPath + delimiter + info[0] + extensionJPG)
