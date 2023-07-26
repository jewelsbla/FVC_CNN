# Importing packages

import os
from PIL import Image
import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt
import math
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from skimage import transform
from sys import getsizeof


# Processing functions

script_dir = os.path.dirname('__file__') #Specifying directory in which the scans can be found

#Cuts off the desired amount of slices in front and back of each scan
def cutOff(scan, frontCut, endCut):
    newSize = scan.shape[0] - frontCut - endCut
    newScan = [scan[i + frontCut] for i in range(newSize)]
    newScan = np.array(newScan) #reformatting as array
    return newScan

#Loads the mhd files and converts them into a numpy array
def makeArray(file):
    script_dir = os.path.dirname('__file__')
    fullPath = os.path.join(script_dir, file)
    array = sitk.GetArrayFromImage(sitk.ReadImage(fullPath))
    return array

#Loads the mhd files and converts them into a numpy array with adjustments included
def makeArray(file, adjustScans, frontCut, endCut):
    fullPath = os.path.join(script_dir, file)
    array = sitk.GetArrayFromImage(sitk.ReadImage(fullPath))
    if(adjustScans):
        array = cutOff(array, frontCut, endCut) #Cutting off first and last frames
        array = transform.resize(array, (newImageDepth, newImageResolution, newImageResolution)) #Rescaling
    return array

#Loads the mhd files and converts them into a numpy array with adjustments and cupe-reshaping included
def makeCubeArray(file, newImageResolution, adjustScans):
    fullPath = os.path.join(script_dir, file)
    array = sitk.GetArrayFromImage(sitk.ReadImage(fullPath))
    if(adjustScans):
        halfCut = (array.shape[0] - newImageResolution) / 2
        frontCutCube = math.floor(halfCut)
        endCutCube = math.ceil(halfCut)
        array = transform.resize(array, (newImageResolution, newImageResolution, newImageResolution)) #Rescaling   
        print(file, "loaded", array.shape, "\n")
    return array

#Adds rotated versions of the scans that are contained in an array to that array
def addRotations(scans, direction, n0, newImageResolution, newImageDepth):
    rotatedScans = scans #Temporary copy
    ScansInConstruction = makeEmptyScanArray(scans.shape[0] + n0, newImageResolution, newImageDepth) #create new empty array with size+=n0
    for j in range(scans.shape[0]):
        ScansInConstruction[j] = rotatedScans[j] #copy array from before
    for k in range(n0):
        ScansInConstruction[scans.shape[0]+k] = np.rot90(rotatedScans[k], 1, direction) #rotate previous last batch
    rotatedScans = ScansInConstruction
    print(rotatedScans.shape)
    return rotatedScans

#Adds flipped versions of the scans that are contained in an array to that array
def addFlips(scans, direction, newImageResolution, newImageDepth):
    flippedScans = scans #Temporary copy
    ScansInConstruction = makeEmptyScanArray(scans.shape[0] * 2, newImageResolution, newImageDepth) #create new empty array with size*=2
    for j in range(scans.shape[0]):
        ScansInConstruction[j] = flippedScans[j] #copy array from before
    for k in range(scans.shape[0]):
        ScansInConstruction[scans.shape[0]+k] = np.flip(flippedScans[k], direction) #rotate previous last batch
    flippedScans = ScansInConstruction
    print(flippedScans.shape)
    return flippedScans

#Creates a new epty array into which Scans can be added
def makeEmptyScanArray(length, newImageDepth, newImageResolution):
    newArray = np.zeros(shape=(length, newImageDepth, newImageResolution, newImageResolution), dtype=np.float16)
    return newArray

#Equates an integer representing the average deviation between two sets
def deviation(input, output):
    difference = input - output
    relativeDeviation = difference / input
    global SAD
    global SAD_rel
    SAD = np.sum(np.abs(difference)) / input.size
    SAD_rel = np.sum(np.abs(relativeDeviation)) / input.size
    print("SAD:", SAD)
    print("SAD relative:", SAD_rel)
        
def getSAD():
    return SAD

def getSAD_rel():
    return SAD_rel

#Displays consecutive Slices within a specified range of a Scan
def exhibit(scan, span, save):
    scan_frames = [scan[i] for i in span]
    fig = plt.figure(figsize=(100, 100))
    w = 3
    for i in range(span[-1] - span[0]):
        plt.subplot(math.ceil(10/w), w, i+1)
        plt.imshow(scan_frames[i] ,cmap='gray')
    plt.show()
    if (save):
       fig.savefig('exhibit.png')

#Plots the average slice-brightness across the slice count of a scan
def brightnessPlot(file):
    plt.rcParams.update(plt.rcParamsDefault)
    plt.rcParams['mathtext.fontset'] = 'stix'
    plt.rcParams['font.family'] = 'STIXGeneral'
    plt.rcParams.update({'font.size': 24})
    n_total = range(file.shape[0])
    brightness = [np.average(file[i]) / np.max(file[i]) for i in n_total]
    plt.plot(n_total, brightness)

#Plots the average slice-brightness across the slice count of multiple scans
def brightnessPlot(files):
    plt.figure(figsize=(20, 12), dpi=80)
    plt.rcParams.update(plt.rcParamsDefault)
    plt.rcParams['mathtext.fontset'] = 'stix'
    plt.rcParams['font.family'] = 'STIXGeneral'
    plt.rcParams.update({'font.size': 24})
    plt.grid(True)
    plt.xlim((0,175))
    plt.ylim((0,1))
    plt.ylabel('FVC')
    plt.xlabel('Scan layer')
    for file in files:
        n_total = range(file.shape[0])
        brightness = [np.average(file[i]) / np.max(file[i]) for i in n_total]
        plt.plot(n_total, brightness)    

#Re-scales Scans to have a different voxel-resolution
def adjustRersolution(Scans, newRes):
    temporaryArray = np.zeros((Scans.shape[0], newRes, newRes, newRes))
    for array in range(Scans.shape[0]):
        temporaryArray[array] = transform.resize(Scans[array], (newRes, newRes, newRes)) #Rescaling  
    Scans = tf.expand_dims(temporaryArray, axis = 4)
    return Scans

#Re-arranges a collection of Scans after augmentation so that an original scan is followed by all augmentations of it
def reSort(array, n_uniqueArrays):
    n_augmentations = int(array.shape[0] / n_uniqueArrays)
    print("n_augmentations: ", n_augmentations)
    temp = np.zeros(array.shape)
    for uniqueArray in range(n_uniqueArrays):
        for augmentation in range(n_augmentations):
            temp[uniqueArray * n_augmentations + augmentation] = array[augmentation*n_uniqueArrays + uniqueArray]
    return temp