#!/usr/bin/env python

from __future__ import print_function
import logging
import os
import pandas as pd
import SimpleITK as sitk
import yaml
import radiomics
from radiomics import featureextractor, getFeatureClasses, imageoperations
import argparse

def main():
  outPath = './'
  dataDir = '../../../data'

  outputFilepath = os.path.join(outPath, outputname)
  progress_filename = os.path.join(outPath, 'pyrad_log.txt')
  params = os.path.join(dataDir, parametername)

  # Configure logging
  rLogger = logging.getLogger('radiomics')

  # Set logging level
  # rLogger.setLevel(logging.INFO)  # Not needed, the default log level of logger is INFO

  # Here create the handler for writing to log file
  handler = logging.FileHandler(filename=progress_filename, mode='w')
  handler.setFormatter(logging.Formatter('%(levelname)s:%(name)s: %(message)s'))
  rLogger.addHandler(handler)

  # Initialize logging for batch log messages
  logger = rLogger.getChild('batch')

  # Set verbosity level for output to stderr (default level = WARNING)
  radiomics.setVerbosity(logging.INFO)

  logger.info('pyradiomics version: %s', radiomics.__version__)

  if os.path.isfile(params):
    extractor = featureextractor.RadiomicsFeatureExtractor(params)  #the future to calculate on the entries
    with open(params) as f:
      parameters = yaml.safe_load(f)  #access settings needed for interpolation and resampling
      #print(var['setting']['binWidth']) To access to different values from yaml file this is the way
      #Need of this 2 for resampling if needed
      settings=parameters['setting']
      interpolator = settings['interpolator']
      resampledPixelSpacing = settings['resampledPixelSpacing']
      
      
  else:  # Parameter file not found, use hardcoded settings instead
    settings = {}
    settings['binWidth'] = 25
    settings['resampledPixelSpacing'] = [1,1,1] # e.g. [1,1,1]  
    settings['interpolator'] = sitk.sitkBSpline
    settings['enableCExtensions'] = True
    #Need of this 2 for resampling if needed
    interpolator = settings.get('interpolator')
    resampledPixelSpacing = settings.get('resampledPixelSpacing')
    
    extractor = featureextractor.RadiomicsFeatureExtractor(**settings)
    # extractor.enableInputImages(wavelet= {'level': 2})

  logger.info('Enabled input images types: %s', extractor.enabledImagetypes)
  logger.info('Enabled features: %s', extractor.enabledFeatures)
  logger.info('Current settings: %s', extractor.settings)

  # Instantiate a pandas data frame to hold the results of all patients
  results = pd.DataFrame()
  
  logger.info('Loading Image and its Segmentation')
  imageFilepath = input_image
  maskFilepath = input_mask
  logger.info('Loading Done!')
  #IDentry = flists[entry]['ID']
  if (imageFilepath is not None) and (maskFilepath is not None):
    dict = {'Image' : os.path.basename(imageFilepath),
        'Mask' : os.path.basename(maskFilepath)
        }
    # create series from dictionary
    featureVector = pd.Series(dict)
    #Using sitk obj cause we might need some resampling or filter to the image/mask
    image = sitk.ReadImage(imageFilepath)
    mask = sitk.ReadImage(maskFilepath)
    label=None  
    #
    # If enabled, resample image (resampled image is automatically cropped.
    #
    if interpolator is not None and resampledPixelSpacing is not None:
      image, mask = imageoperations.resampleImage(image, mask, **settings)

    bb, correctedMask = imageoperations.checkMask(image, mask)
    if correctedMask is not None:
      mask = correctedMask
    image, mask = imageoperations.cropToTumorMask(image, mask, bb)

    try:
      # PyRadiomics returns the result as an ordered dictionary, which can be converted to a pandas Series
      # The keys in the dictionary will be used as the index (the labels for the rows), with the values of the features
      # as the values in the rows.
      result = pd.Series(extractor.execute(image, mask, label))
      featureVector = featureVector.append(result)
    except Exception:
      logger.error('FEATURE EXTRACTION FAILED:', exc_info=True)

      # To add the calculated features for this case to our data frame, the series must have a name (which will be the
      # name of the column)
    # featureVector.name = entry      
    # print(featureVector)
    # By specifying an 'outer' join, all calculated features are added to the data frame, including those not
    # calculated for previous cases. This also cause for the first patient it is 'joined' with the empty data frame
    # so we want to avoi having an empty one
    # results = results.join(featureVector, how='outer')  # If feature extraction failed, results will be all NaN
    
    ####  need to put names in order to convert to pd dataframe. ######
    featureVector.name=''
    results = results.join(featureVector, how='outer')  # If feature extraction failed, results will be all NaN

    #results=pandas.
    # print(results)
  logger.info('Extraction complete, writing CSV')
  
  # .T transposes the data frame, so that each line will represent one patient, with the extracted features as columns
  results=results.T
  # Exporting dataframe in csv
  results.to_csv(outputFilepath, index=False, na_rep='NaN')
  # logresult.to_csv(outputFilepath1, index=False, na_rep='NaN')
  logger.info('CSV writing complete')


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Process radiomics features from nrrd files',
                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("-1", "--inputimage", 
                    help="Path of the input image file",
                    default="/home/carollo/myScratch/projects/zlatko/Radiomics/data/Test/Testlauf003/testlauf3_image.nrrd",
                    required=False)
  parser.add_argument("-2", "--inputmask",
                    help="Path of the input mask file",
                    default="/home/carollo/myScratch/projects/zlatko/Radiomics/data/Test/Testlauf003/testlauf3_label.nrrd",
                    required=False)
  parser.add_argument("-3", "--outputfilename",
                    help="Name of the output result file",
                    default="radiomics_features_test.csv",
                    required=False)
  parser.add_argument("-4", "--setting",
                    help="Name of the parameter file to use for the analysis",
                    default="params.yml",
                    required=False)
  parser.add_argument("-R", "--resume",
                    help="Resume pipeline",
                    default="again",                        
                    action="store_true")
  args = parser.parse_args()
  input_image = args.inputimage
  input_mask = args.inputmask
  outputname = args.outputfilename
  parametername = args.setting
  resume = args.resume
  main()