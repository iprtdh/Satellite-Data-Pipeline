# Satellite-Data-Pipeline
This repository contains a project focused on astronomical imagery in FITS format and detecting Stars using a modular data pipeline.

About the FITS file used, 'hlsp_andromeda_hst_acs-wfc_halo11_f814w_v2_img.fits'(download it from here: https://drive.google.com/file/d/1Vezv1kjAr6xUm1F6ZlQ47mmnpa3_lHss/view?usp=drive_link):
 
 -> This FITS file is extracted from Deep Optical Photometry of Six Fields in the Andromeda Galaxy, 2009. This data comprises of the 'halo11' field, under program number 9453, The Age of the Andromeda Halo. The 
    main target was the Andromeda's halo which consists of 65 orbtits via F814W filter.
 
Modules:
 1) finalmethods.py: It contains the details of the FITS file used and functions that are used to store certain values related to a particular section of the FITS file data.

 2) algors.py: It contains an algorithm that merges a group of apertures forming in a very small range to avoid multiple aperture placements over a single object, and therefore contining the functions to store the 
               new values for the same.

Jupyter Notebook: This notebook contains the code cells where the fits file data is divided across 100 sections as per the shape of the data matrix and the sections corresponding to the corners of the image were processed to correct the parts of the section where the image was completely empty. Data Visualisation was implemented over a variety of sections. Then, a stack function was used to combine the required properties of the star data, computed using a function from the modules in a single numpy array to store in a dataframe which would be saved in a csv file.
