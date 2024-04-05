# FVC_CNN

Convolutional neural network (CNN) determining the fiber volume content (FVC) of 3D CT scans of carbon fiber reinforced polyamide 6.

***

## Disclaimer 
The paper describing the scientific background and the methods underlying this repository is: 

Juliane Blarr, Philipp Kunze, Noah Kresin, Wilfried V. Liebig, Kaan Inal, Kay A. Weidenmann,
Novel thresholding method and convolutional neural network for fiber volume content determination from 3D μCT images,
NDT & E International,
Volume 144,
2024,
103067,
ISSN 0963-8695,
https://doi.org/10.1016/j.ndteint.2024.103067,
https://www.sciencedirect.com/science/article/pii/S096386952400032X.
Abstract: In order to determine fiber volume contents (FVC) of low contrast CT images of carbon fiber reinforced polyamide 6, a novel thresholding method and a convolutional neural network are implemented with absolute deviations from experimental values of 2.7% and, respectively, 1.46% on average. The first method is a sample thickness based adjustment of the Otsu threshold, the so-called “average or above (AOA) thresholding”, and the second is a mixed convolutional neural network (CNN) that directly takes 3D scans and the experimentally determined FVC values as input. However, the methods are limited to the specific material combination, process-dependent microstructure and scan quality but could be further developed for different material types.
Keywords: X-ray tomography; Carbon fiber reinforced polymers; Thermoplastics; Low contrast; Deep learning


If you use the code in this repository, please cite the paper accordingly.

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


