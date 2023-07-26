# FVC_CNN

Convolutional neural network (CNN) determining the fiber volume content (FVC) of 3D CT scans of carbon fiber reinforced polyamide 6.

***

## Disclaimer 
The paper describing the scientific background and the methods underlying this repository is: 

XXX

This code was published alongside the raw data of the CT scans and the evaluated tensor data first as research data set here: XXX

If you use the code in this repository, please cite both DOIs.

## Content

CT scans of glass fiber reinforced polymers are used to determine the fiber volume content (FVC) through image processing. However, in the case of carbon fiber reinforced polymers (CFRP), the contrast between the polymer matrix existing of C-atoms and the carbon fibers existing of C-atoms is very low. Additionally, as carbon fibers have a small diameter of 5-7 µm, the resolution has to be high in order to resolve the fibers. Both effects lead to noisy images. As conventional thresholding methods struggle to reliably differentiate between matrix and fibers, the authors tested a convolutional neural network for the FVC determination from 3D CT images. The model directly takes the 3D CT scans and the experimentally measured FVC as an input and outputs one single value as predicted FVC for a specific scan and hence specimen. The network architecture can be seen below:

<p align="center">
  <img src="https://github.com/jewelsbla/FVC_CNN/blob/main/images/network_architecture_no_background.png">
</p>

## Version

This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg


