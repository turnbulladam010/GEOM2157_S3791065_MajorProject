#Import modules required to retrieve html strings and download data
import urllib.request
from bs4 import BeautifulSoup, SoupStrainer
import requests

#Import QGIS modules and algorithms
from qgis.core import QgsProcessingRegistry #QgsRasterLayer, QgsApplication, QgsProject
from qgis.analysis import QgsNativeAlgorithms

import os
from qgis.core import (
     QgsApplication
)

#Initiates the QGIS application without a GUI
QgsApplication.setPrefixPath('/usr', True)
qgs = QgsApplication([], False) #Setting this to True would launch the GUI
qgs.initQgis()

from processing.core.Processing import Processing
Processing.initialize()
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())
import processing

#This list includes the possible dates within the NCI Sentinel catalogue
date_list = ["2015-07-12", "2015-07-25", "2015-07-31", "2015-08-01", "2015-08-04", "2015-08-05", "2015-08-10", "2015-08-11", "2015-08-12", "2015-08-14", "2015-08-15", "2015-08-18", "2015-08-20", "2015-08-21", "2015-08-22", "2015-08-23", "2015-08-25", "2015-08-26", "2015-08-27", "2015-08-28", "2015-08-29", "2015-08-30", "2015-08-31", "2015-09-02", "2015-09-03", "2015-09-04", "2015-09-05", "2015-09-08", "2015-09-09", "2015-09-10", "2015-09-11", "2015-09-12", "2015-09-13", "2015-09-14", "2015-09-15", "2015-09-19", "2015-09-22", "2015-09-23", "2015-09-29", "2015-09-30", "2015-10-01", "2015-10-02", "2015-10-03", "2015-10-04", "2015-10-05", "2015-10-06", "2015-10-07", "2015-10-08", "2015-10-19", "2015-10-20", "2015-10-21", "2015-10-22", "2015-10-23", "2015-10-24", "2015-10-28", "2015-11-11", "2015-11-12", "2015-11-13", "2015-11-14", "2015-11-15", "2015-11-17", "2015-11-18", "2015-11-20", "2015-11-21", "2015-11-22", "2015-11-23", "2015-11-24", "2015-11-25", "2015-11-26", "2015-11-27", "2015-11-28", "2015-11-29", "2015-11-30", "2015-12-01", "2015-12-03", "2015-12-04", "2015-12-05", "2015-12-06", "2015-12-07", "2015-12-08", "2015-12-09", "2015-12-10", "2015-12-11", "2015-12-16", "2015-12-17", "2015-12-18", "2015-12-19", "2015-12-21", "2015-12-22", "2015-12-23", "2015-12-24", "2015-12-25", "2015-12-26", "2015-12-27", "2015-12-28", "2015-12-29", "2015-12-30", "2015-12-31", "2016-01-01", "2016-01-02", "2016-01-03", "2016-01-04", "2016-01-05", "2016-01-06", "2016-01-07", "2016-01-08", "2016-01-09", "2016-01-10", "2016-01-11", "2016-01-12", "2016-01-13", "2016-01-14", "2016-01-15", "2016-01-16", "2016-01-17", "2016-01-18", "2016-01-19", "2016-01-20", "2016-01-21", "2016-01-22", "2016-01-23", "2016-01-24", "2016-01-25", "2016-01-26", "2016-01-29", "2016-01-30", "2016-01-31", "2016-02-01", "2016-02-02", "2016-02-03", "2016-02-04", "2016-02-05", "2016-02-06", "2016-02-08", "2016-02-09", "2016-02-10", "2016-02-11", "2016-02-12", "2016-02-13", "2016-02-14", "2016-02-15", "2016-02-16", "2016-02-17", "2016-02-18", "2016-02-19", "2016-02-20", "2016-03-02", "2016-03-03", "2016-03-04", "2016-03-05", "2016-03-06", "2016-03-07", "2016-03-08", "2016-03-09", "2016-03-10", "2016-03-11", "2016-03-12", "2016-03-14", "2016-03-15", "2016-03-16", "2016-03-17", "2016-03-18", "2016-03-19", "2016-03-20", "2016-03-21", "2016-03-22", "2016-03-23", "2016-03-24", "2016-03-25", "2016-03-27", "2016-03-28", "2016-03-29", "2016-03-30", "2016-04-01", "2016-04-02", "2016-04-03", "2016-04-05", "2016-04-06", "2016-04-07", "2016-04-08", "2016-04-09", "2016-04-10", "2016-04-11", "2016-04-12", "2016-04-13", "2016-04-14", "2016-04-15", "2016-04-16", "2016-04-17", "2016-04-18", "2016-04-19", "2016-04-20", "2016-04-21", "2016-04-22", "2016-04-23", "2016-04-24", "2016-04-25", "2016-04-26", "2016-04-27", "2016-04-28", "2016-04-29", "2016-04-30", "2016-05-01", "2016-05-02", "2016-05-03", "2016-05-04", "2016-05-05", "2016-05-06", "2016-05-07", "2016-05-08", "2016-05-09", "2016-05-10", "2016-05-11", "2016-05-12", "2016-05-13", "2016-05-14", "2016-05-15", "2016-05-16", "2016-05-18", "2016-05-19", "2016-05-20", "2016-05-21", "2016-05-22", "2016-05-23", "2016-05-24", "2016-05-25", "2016-05-26", "2016-05-27", "2016-05-28", "2016-05-29", "2016-05-30", "2016-05-31", "2016-06-02", "2016-06-03", "2016-06-04", "2016-06-05", "2016-06-06", "2016-06-07", "2016-06-08", "2016-06-09", "2016-06-10", "2016-06-11", "2016-06-12", "2016-06-13", "2016-06-14", "2016-06-15", "2016-06-16", "2016-06-17", "2016-06-18", "2016-06-19", "2016-06-20", "2016-06-21", "2016-06-22", "2016-06-23", "2016-06-24", "2016-06-25", "2016-06-26", "2016-06-27", "2016-06-28", "2016-06-29", "2016-06-30", "2016-07-01", "2016-07-02", "2016-07-03", "2016-07-05", "2016-07-06", "2016-07-07", "2016-07-08", "2016-07-09", "2016-07-10", "2016-07-11", "2016-07-12", "2016-07-13", "2016-07-14", "2016-07-15", "2016-07-16", "2016-07-17", "2016-07-18", "2016-07-19", "2016-07-20", "2016-07-21", "2016-07-22", "2016-07-23", "2016-07-24", "2016-07-25", "2016-07-26", "2016-07-27", "2016-07-28", "2016-07-29", "2016-07-30", "2016-07-31", "2016-08-01", "2016-08-02", "2016-08-03", "2016-08-04", "2016-08-05", "2016-08-06", "2016-08-07", "2016-08-08", "2016-08-09", "2016-08-10", "2016-08-11", "2016-08-12", "2016-08-13", "2016-08-14", "2016-08-15", "2016-08-16", "2016-08-17", "2016-08-18", "2016-08-19", "2016-08-20", "2016-08-21", "2016-08-22", "2016-08-23", "2016-08-24", "2016-08-25", "2016-08-26", "2016-08-27", "2016-08-28", "2016-08-29", "2016-08-30", "2016-08-31", "2016-09-01", "2016-09-02", "2016-09-03", "2016-09-04", "2016-09-05", "2016-09-06", "2016-09-07", "2016-09-08", "2016-09-09", "2016-09-10", "2016-09-11", "2016-09-12", "2016-09-13", "2016-09-14", "2016-09-15", "2016-09-16", "2016-09-17", "2016-09-18", "2016-09-19", "2016-09-20", "2016-09-21", "2016-09-22", "2016-09-23", "2016-09-24", "2016-09-25", "2016-09-26", "2016-09-27", "2016-09-28", "2016-09-29", "2016-09-30", "2016-10-01", "2016-10-02", "2016-10-03", "2016-10-04", "2016-10-05", "2016-10-06", "2016-10-07", "2016-10-08", "2016-10-09", "2016-10-10", "2016-10-11", "2016-10-12", "2016-10-13", "2016-10-14", "2016-10-15", "2016-10-16", "2016-10-17", "2016-10-18", "2016-10-19", "2016-10-20", "2016-10-21", "2016-10-22", "2016-10-23", "2016-10-24", "2016-10-25", "2016-10-26", "2016-10-27", "2016-10-28", "2016-10-29", "2016-10-30", "2016-10-31", "2016-11-01", "2016-11-02", "2016-11-03", "2016-11-04", "2016-11-05", "2016-11-06", "2016-11-07", "2016-11-08", "2016-11-09", "2016-11-10", "2016-11-11", "2016-11-12", "2016-11-13", "2016-11-14", "2016-11-15", "2016-11-16", "2016-11-17", "2016-11-18", "2016-11-19", "2016-11-20", "2016-11-21", "2016-11-22", "2016-11-23", "2016-11-24", "2016-11-25", "2016-11-26", "2016-11-27", "2016-11-28", "2016-11-29", "2016-11-30", "2016-12-01", "2016-12-02", "2016-12-03", "2016-12-04", "2016-12-05", "2016-12-06", "2016-12-07", "2016-12-08", "2016-12-09", "2016-12-10", "2016-12-11", "2016-12-12", "2016-12-13", "2016-12-14", "2016-12-15", "2016-12-16", "2016-12-17", "2016-12-18", "2016-12-19", "2016-12-20", "2016-12-21", "2016-12-22", "2016-12-23", "2016-12-24", "2016-12-25", "2016-12-26", "2016-12-27", "2016-12-28", "2016-12-29", "2016-12-30", "2016-12-31", "2017-01-01", "2017-01-02", "2017-01-03", "2017-01-04", "2017-01-05", "2017-01-06", "2017-01-07", "2017-01-08", "2017-01-09", "2017-01-11", "2017-01-12", "2017-01-13", "2017-01-14", "2017-01-15", "2017-01-16", "2017-01-17", "2017-01-18", "2017-01-19", "2017-01-20", "2017-01-24", "2017-01-25", "2017-01-26", "2017-01-27", "2017-01-28", "2017-01-29", "2017-01-30", "2017-01-31", "2017-02-01", "2017-02-02", "2017-02-03", "2017-02-04", "2017-02-05", "2017-02-06", "2017-02-07", "2017-02-08", "2017-02-09", "2017-02-10", "2017-02-11", "2017-02-12", "2017-02-13", "2017-02-14", "2017-02-15", "2017-02-16", "2017-02-17", "2017-02-18", "2017-02-19", "2017-02-20", "2017-02-21", "2017-02-22", "2017-02-23", "2017-02-24", "2017-02-25", "2017-02-26", "2017-02-27", "2017-02-28", "2017-03-01", "2017-03-02", "2017-03-03", "2017-03-04", "2017-03-05", "2017-03-06", "2017-03-07", "2017-03-08", "2017-03-09", "2017-03-10", "2017-03-11", "2017-03-12", "2017-03-13", "2017-03-14", "2017-03-15", "2017-03-16", "2017-03-17", "2017-03-18", "2017-03-19", "2017-03-20", "2017-03-21", "2017-03-22", "2017-03-23", "2017-03-24", "2017-03-25", "2017-03-26", "2017-03-27", "2017-03-28", "2017-03-29", "2017-03-30", "2017-03-31", "2017-04-01", "2017-04-02", "2017-04-03", "2017-04-04", "2017-04-05", "2017-04-06", "2017-04-07", "2017-04-08", "2017-04-09", "2017-04-10", "2017-04-11", "2017-04-12", "2017-04-13", "2017-04-14", "2017-04-15", "2017-04-16", "2017-04-17", "2017-04-18", "2017-04-19", "2017-04-20", "2017-04-21", "2017-04-22", "2017-04-23", "2017-04-24", "2017-04-25", "2017-04-26", "2017-04-27", "2017-04-28", "2017-04-29", "2017-04-30", "2017-05-01", "2017-05-02", "2017-05-03", "2017-05-04", "2017-05-05", "2017-05-06", "2017-05-07", "2017-05-08", "2017-05-09", "2017-05-10", "2017-05-11", "2017-05-12", "2017-05-13", "2017-05-14", "2017-05-15", "2017-05-16", "2017-05-17", "2017-05-18", "2017-05-19", "2017-05-20", "2017-05-21", "2017-05-22", "2017-05-23", "2017-05-24", "2017-05-25", "2017-05-26", "2017-05-27", "2017-05-28", "2017-05-29", "2017-05-30", "2017-05-31", "2017-06-01", "2017-06-02", "2017-06-03", "2017-06-04", "2017-06-05", "2017-06-06", "2017-06-07", "2017-06-08", "2017-06-09", "2017-06-10", "2017-06-11", "2017-06-12", "2017-06-13", "2017-06-14", "2017-06-15", "2017-06-16", "2017-06-17", "2017-06-18", "2017-06-19", "2017-06-20", "2017-06-21", "2017-06-22", "2017-06-23", "2017-06-24", "2017-06-25", "2017-06-26", "2017-06-27", "2017-06-28", "2017-06-29", "2017-06-30", "2017-07-01", "2017-07-02", "2017-07-03", "2017-07-04", "2017-07-05", "2017-07-06", "2017-07-07", "2017-07-08", "2017-07-09", "2017-07-10", "2017-07-11", "2017-07-12", "2017-07-13", "2017-07-14", "2017-07-15", "2017-07-16", "2017-07-17", "2017-07-18", "2017-07-19", "2017-07-20", "2017-07-21", "2017-07-22", "2017-07-23", "2017-07-24", "2017-07-25", "2017-07-26", "2017-07-27", "2017-07-28", "2017-07-29", "2017-07-30", "2017-07-31", "2017-08-01", "2017-08-02", "2017-08-03", "2017-08-04", "2017-08-05", "2017-08-06", "2017-08-07", "2017-08-08", "2017-08-09", "2017-08-10", "2017-08-11", "2017-08-12", "2017-08-13", "2017-08-14", "2017-08-15", "2017-08-16", "2017-08-17", "2017-08-18", "2017-08-19", "2017-08-20", "2017-08-21", "2017-08-22", "2017-08-23", "2017-08-24", "2017-08-25", "2017-08-26", "2017-08-27", "2017-08-28", "2017-08-29", "2017-08-30", "2017-08-31", "2017-09-01", "2017-09-02", "2017-09-03", "2017-09-04", "2017-09-05", "2017-09-06", "2017-09-07", "2017-09-08", "2017-09-09", "2017-09-10", "2017-09-11", "2017-09-12", "2017-09-13", "2017-09-14", "2017-09-15", "2017-09-16", "2017-09-17", "2017-09-18", "2017-09-19", "2017-09-20", "2017-09-21", "2017-09-22", "2017-09-23", "2017-09-24", "2017-09-25", "2017-09-26", "2017-09-27", "2017-09-28", "2017-09-29", "2017-09-30", "2017-10-01", "2017-10-02", "2017-10-03", "2017-10-04", "2017-10-05", "2017-10-06", "2017-10-07", "2017-10-08", "2017-10-09", "2017-10-10", "2017-10-11", "2017-10-12", "2017-10-13", "2017-10-14", "2017-10-15", "2017-10-16", "2017-10-17", "2017-10-18", "2017-10-19", "2017-10-20", "2017-10-21", "2017-10-22", "2017-10-23", "2017-10-24", "2017-10-25", "2017-10-26", "2017-10-27", "2017-10-28", "2017-10-29", "2017-10-30", "2017-10-31", "2017-11-01", "2017-11-02", "2017-11-03", "2017-11-04", "2017-11-05", "2017-11-06", "2017-11-07", "2017-11-08", "2017-11-09", "2017-11-10", "2017-11-11", "2017-11-12", "2017-11-13", "2017-11-14", "2017-11-15", "2017-11-16", "2017-11-17", "2017-11-18", "2017-11-19", "2017-11-20", "2017-11-21", "2017-11-22", "2017-11-23", "2017-11-24", "2017-11-25", "2017-11-26", "2017-11-27", "2017-11-28", "2017-11-29", "2017-11-30", "2017-12-01", "2017-12-02", "2017-12-03", "2017-12-04", "2017-12-05", "2017-12-06", "2017-12-07", "2017-12-08", "2017-12-09", "2017-12-10", "2017-12-11", "2017-12-12", "2017-12-13", "2017-12-14", "2017-12-15", "2017-12-16", "2017-12-17", "2017-12-18", "2017-12-19", "2017-12-20", "2017-12-21", "2017-12-22", "2017-12-23", "2017-12-24", "2017-12-25", "2017-12-26", "2017-12-27", "2017-12-28", "2017-12-29", "2017-12-30", "2017-12-31", "2018-01-01", "2018-01-02", "2018-01-03", "2018-01-04", "2018-01-05", "2018-01-06", "2018-01-07", "2018-01-08", "2018-01-09", "2018-01-10", "2018-01-11", "2018-01-12", "2018-01-13", "2018-01-14", "2018-01-15", "2018-01-16", "2018-01-17", "2018-01-18", "2018-01-19", "2018-01-20", "2018-01-21", "2018-01-22", "2018-01-23", "2018-01-24", "2018-01-25", "2018-01-26", "2018-01-27", "2018-01-28", "2018-01-29", "2018-01-30", "2018-01-31", "2018-02-01", "2018-02-02", "2018-02-03", "2018-02-04", "2018-02-05", "2018-02-06", "2018-02-07", "2018-02-08", "2018-02-09", "2018-02-10", "2018-02-11", "2018-02-12", "2018-02-13", "2018-02-14", "2018-02-15", "2018-02-16", "2018-02-17", "2018-02-18", "2018-02-19", "2018-02-20", "2018-02-21", "2018-02-22", "2018-02-23", "2018-02-24", "2018-02-25", "2018-02-26", "2018-02-27", "2018-02-28", "2018-03-01", "2018-03-02", "2018-03-03", "2018-03-04", "2018-03-05", "2018-03-06", "2018-03-07", "2018-03-08", "2018-03-09", "2018-03-10", "2018-03-11", "2018-03-12", "2018-03-13", "2018-03-14", "2018-03-15", "2018-03-16", "2018-03-17", "2018-03-18", "2018-03-19", "2018-03-20", "2018-03-21", "2018-03-22", "2018-03-23", "2018-03-24", "2018-03-25", "2018-03-26", "2018-03-27", "2018-03-28", "2018-03-29", "2018-03-30", "2018-03-31", "2018-04-01", "2018-04-02", "2018-04-03", "2018-04-04", "2018-04-05", "2018-04-06", "2018-04-07", "2018-04-08", "2018-04-09", "2018-04-10", "2018-04-11", "2018-04-12", "2018-04-13", "2018-04-14", "2018-04-15", "2018-04-16", "2018-04-17", "2018-04-18", "2018-04-19", "2018-04-20", "2018-04-21", "2018-04-22", "2018-04-23", "2018-04-24", "2018-04-25", "2018-04-26", "2018-04-27", "2018-04-28", "2018-04-29", "2018-05-01", "2018-05-02", "2018-05-03", "2018-05-04", "2018-05-05", "2018-05-06", "2018-05-07", "2018-05-08", "2018-05-09", "2018-05-10", "2018-05-11", "2018-05-12", "2018-05-13", "2018-05-14", "2018-05-15", "2018-05-16", "2018-05-17", "2018-05-18", "2018-05-19", "2018-05-20", "2018-05-21", "2018-05-22", "2018-05-23", "2018-05-24", "2018-05-25", "2018-05-26", "2018-05-27", "2018-05-28", "2018-05-29", "2018-05-30", "2018-05-31", "2018-06-01", "2018-06-02", "2018-06-03", "2018-06-04", "2018-06-05", "2018-06-06", "2018-06-07", "2018-06-08", "2018-06-09", "2018-06-10", "2018-06-11", "2018-06-12", "2018-06-13", "2018-06-14", "2018-06-15", "2018-06-16", "2018-06-17", "2018-06-18", "2018-06-19", "2018-06-20", "2018-06-21", "2018-06-22", "2018-06-23", "2018-06-24", "2018-06-25", "2018-06-26", "2018-06-27", "2018-06-28", "2018-06-29", "2018-06-30", "2018-07-01", "2018-07-02", "2018-07-03", "2018-07-04", "2018-07-05", "2018-07-06", "2018-07-07", "2018-07-08", "2018-07-09", "2018-07-10", "2018-07-11", "2018-07-12", "2018-07-13", "2018-07-14", "2018-07-15", "2018-07-16", "2018-07-17", "2018-07-18", "2018-07-19", "2018-07-20", "2018-07-21", "2018-07-22", "2018-07-23", "2018-07-24", "2018-07-25", "2018-07-26", "2018-07-27", "2018-07-28", "2018-07-29", "2018-07-30", "2018-07-31", "2018-08-01", "2018-08-02", "2018-08-03", "2018-08-04", "2018-08-05", "2018-08-06", "2018-08-07", "2018-08-08", "2018-08-09", "2018-08-10", "2018-08-11", "2018-08-12", "2018-08-13", "2018-08-14", "2018-08-15", "2018-08-16", "2018-08-17", "2018-08-18", "2018-08-19", "2018-08-20", "2018-08-21", "2018-08-22", "2018-08-23", "2018-08-24", "2018-08-25", "2018-08-26", "2018-08-27", "2018-08-28", "2018-08-29", "2018-08-30", "2018-08-31", "2018-09-01", "2018-09-02", "2018-09-03", "2018-09-04", "2018-09-05", "2018-09-06", "2018-09-07", "2018-09-08", "2018-09-09", "2018-09-10", "2018-09-11", "2018-09-12", "2018-09-13", "2018-09-14", "2018-09-15", "2018-09-16", "2018-09-17", "2018-09-18", "2018-09-19", "2018-09-20", "2018-09-21", "2018-09-22", "2018-09-23", "2018-09-24", "2018-09-25", "2018-09-26", "2018-09-27", "2018-09-28", "2018-09-29", "2018-09-30", "2018-10-01", "2018-10-02", "2018-10-03", "2018-10-04", "2018-10-05", "2018-10-06", "2018-10-07", "2018-10-08", "2018-10-09", "2018-10-10", "2018-10-11", "2018-10-12", "2018-10-13", "2018-10-14", "2018-10-15", "2018-10-16", "2018-10-17", "2018-10-18", "2018-10-19", "2018-10-20", "2018-10-21", "2018-10-22", "2018-10-23", "2018-10-24", "2018-10-25", "2018-10-26", "2018-10-27", "2018-10-28", "2018-10-29", "2018-10-30", "2018-10-31", "2018-11-01", "2018-11-02", "2018-11-03", "2018-11-04", "2018-11-05", "2018-11-06", "2018-11-07", "2018-11-08", "2018-11-09", "2018-11-10", "2018-11-11", "2018-11-12", "2018-11-13", "2018-11-14", "2018-11-15", "2018-11-16", "2018-11-17", "2018-11-18", "2018-11-19", "2018-11-20", "2018-11-21", "2018-11-22", "2018-11-23", "2018-11-24", "2018-11-25", "2018-11-26", "2018-11-27", "2018-11-28", "2018-11-29", "2018-11-30", "2018-12-01", "2018-12-02", "2018-12-03", "2018-12-04", "2018-12-05", "2018-12-06", "2018-12-07", "2018-12-08", "2018-12-09", "2018-12-10", "2018-12-11", "2018-12-12", "2018-12-13", "2018-12-14", "2018-12-15", "2018-12-16", "2018-12-17", "2018-12-18", "2018-12-19", "2018-12-20", "2018-12-21", "2018-12-22", "2018-12-23", "2018-12-24", "2018-12-25", "2018-12-26", "2018-12-27", "2018-12-28", "2018-12-29", "2018-12-30", "2018-12-31", "2019-01-01", "2019-01-02", "2019-01-03", "2019-01-04", "2019-01-05", "2019-01-06", "2019-01-07", "2019-01-08", "2019-01-09", "2019-01-10", "2019-01-11", "2019-01-12", "2019-01-13", "2019-01-14", "2019-01-15", "2019-01-16", "2019-01-17", "2019-01-18", "2019-01-19", "2019-01-20", "2019-01-21", "2019-01-22", "2019-01-23", "2019-01-24", "2019-01-25", "2019-01-26", "2019-01-27", "2019-01-28", "2019-01-29", "2019-01-30", "2019-01-31", "2019-02-01", "2019-02-02", "2019-02-03", "2019-02-04", "2019-02-05", "2019-02-06", "2019-02-07", "2019-02-08", "2019-02-09", "2019-02-10", "2019-02-11", "2019-02-12", "2019-02-13", "2019-02-14", "2019-02-15", "2019-02-16", "2019-02-17", "2019-02-18", "2019-02-19", "2019-02-20", "2019-02-21", "2019-02-22", "2019-02-23", "2019-02-24", "2019-02-25", "2019-02-26", "2019-02-27", "2019-02-28", "2019-03-01", "2019-03-02", "2019-03-03", "2019-03-04", "2019-03-05", "2019-03-06", "2019-03-07", "2019-03-08", "2019-03-09", "2019-03-10", "2019-03-11", "2019-03-12", "2019-03-13", "2019-03-14", "2019-03-15", "2019-03-16", "2019-03-17", "2019-03-18", "2019-03-19", "2019-03-20", "2019-03-21", "2019-03-22", "2019-03-23", "2019-03-24", "2019-03-25", "2019-03-26", "2019-03-27", "2019-03-28", "2019-03-29", "2019-03-30", "2019-03-31", "2019-04-01", "2019-04-02", "2019-04-03", "2019-04-04", "2019-04-05", "2019-04-06", "2019-04-07", "2019-04-08", "2019-04-09", "2019-04-10", "2019-04-11", "2019-04-12", "2019-04-13", "2019-04-14", "2019-04-15", "2019-04-16", "2019-04-17", "2019-04-18", "2019-04-19", "2019-04-20", "2019-04-21", "2019-04-22", "2019-04-23", "2019-04-24", "2019-04-25", "2019-04-26", "2019-04-27", "2019-04-28", "2019-04-29", "2019-04-30", "2019-05-01", "2019-05-02", "2019-05-03", "2019-05-04", "2019-05-05", "2019-05-06", "2019-05-07", "2019-05-08", "2019-05-09", "2019-05-10", "2019-05-11", "2019-05-12", "2019-05-13", "2019-05-14", "2019-05-15", "2019-05-16", "2019-05-17", "2019-05-18", "2019-05-19", "2019-05-20", "2019-05-21", "2019-05-22", "2019-05-23", "2019-05-24", "2019-05-25", "2019-05-26", "2019-05-27", "2019-05-28", "2019-05-29", "2019-05-30", "2019-05-31", "2019-06-01", "2019-06-02", "2019-06-03", "2019-06-04", "2019-06-05", "2019-06-06", "2019-06-07", "2019-06-08", "2019-06-09", "2019-06-10", "2019-06-11", "2019-06-12", "2019-06-13", "2019-06-14", "2019-06-15", "2019-06-16", "2019-06-17", "2019-06-18", "2019-06-19", "2019-06-20", "2019-06-21", "2019-06-22", "2019-06-23", "2019-06-24", "2019-06-25", "2019-06-26", "2019-06-27", "2019-06-28", "2019-06-29", "2019-06-30", "2019-07-02", "2019-07-03", "2019-07-04", "2019-07-05", "2019-07-06", "2019-07-07", "2019-07-08", "2019-07-09", "2019-07-10", "2019-07-11", "2019-07-12", "2019-07-13", "2019-07-14", "2019-07-15", "2019-07-16", "2019-07-17", "2019-07-18", "2019-07-19", "2019-07-20", "2019-07-21", "2019-07-22", "2019-07-23", "2019-07-24", "2019-07-25", "2019-07-26", "2019-07-27", "2019-07-28", "2019-07-29", "2019-07-30", "2019-07-31", "2019-08-01", "2019-08-02", "2019-08-03", "2019-08-04", "2019-08-05", "2019-08-06", "2019-08-07", "2019-08-08", "2019-08-09", "2019-08-10", "2019-08-11", "2019-08-12", "2019-08-13", "2019-08-14", "2019-08-15", "2019-08-16", "2019-08-17", "2019-08-18", "2019-08-19", "2019-08-20", "2019-08-26", "2019-08-27", "2019-08-28", "2019-08-29", "2019-08-30", "2019-08-31", "2019-09-01", "2019-09-02", "2019-09-03", "2019-09-04", "2019-09-05", "2019-09-06", "2019-09-07", "2019-09-08", "2019-09-09", "2019-09-10", "2019-09-11", "2019-09-12", "2019-09-13", "2019-09-14", "2019-09-15", "2019-09-16"]

#Strings to be concatenated into html paths
date_url_pref = 'http://dap.nci.org.au/thredds/remoteCatalogService?catalog=http://dapds00.nci.org.au/thredds/catalog/if87/'
date_url_suff = '/catalog.xml'
gen_url_pref = 'http://dap.nci.org.au'
cellCode = 'T50JLL'

#Define numerous lists to be populated later
cellList = []
qaLinkList = []
fMaskLinkList = []
finalLinkList = []
noDataThresh = 20.0
cloudThresh = 20.0
cShadThresh = 20.0
finalDLList = []
fCellList = []
NBARTLinkList = []
B02LinkList = []
B03LinkList = []
B04LinkList = []
finB02LinkList = []
finB03LinkList = []
finB04LinkList = []

#For each date a html path is created, retrieved and converted to a useable format
for date in date_list:
    linkList = []
    date_url = date_url_pref + date + date_url_suff
    #print(date_url)
    url_content = requests.get(date_url)
    url_convert = url_content.text
    soup = BeautifulSoup(url_convert)
    #All the links in the date html are stored in a list
    for link in soup.find_all('a'):
        linkList.append(link.get('href'))
    #Each link in the list is searched for the UTM cell code
    res = [i for i in linkList if cellCode in i]
    #If the UTM cell code is found that link is stored in a list of htmls for the desired UTM cell
    if res != []:
        stringyRes = str(res)
        strippyRes = stringyRes[2:-2]
        cellUrl = gen_url_pref + strippyRes
        cellList.append(cellUrl)
#print(cellList)
 
#Each UTM cell html is retrieved and converted to a useable format
for cellLink in cellList:
    linkList2 = []
    cell_content = requests.get(cellLink)
    cell_convert = cell_content.text
    cellSoup = BeautifulSoup(cell_convert)
    #All the links in the UTM cell html are stored in a list
    for link in cellSoup.find_all('a'):
        linkList2.append(link.get('href'))
    #Each link is searched for the substring 'QA'
    qaSearch = 'QA'
    res2 = [i for i in linkList2 if qaSearch in i]
    #If the substring 'QA" is found that link is stored in a list of htmls for the quality assurance page of the desired UTM cell
    if res2 != []:
        stringyRes2 = str(res2)
        strippyRes2 = stringyRes2[2:-2]
        qaUrl = gen_url_pref + strippyRes2
        qaLinkList.append(qaUrl)
#print(qaLinkList)

#Each UTM cell quality assurance page html is retrieved and converted to a useable format
for qaLink in qaLinkList:
    linkList3 = []
    qa_content = requests.get(qaLink)
    qa_convert = qa_content.text
    qaSoup = BeautifulSoup(qa_convert)
    #All the links in the UTM cell quality assurance page html are stored in a list
    for link in qaSoup.find_all('a'):
        linkList3.append(link.get('href'))
    #If the substring 'FMASK' is found that link is stored in a list of htmls for the Fmask page of the desired UTM cell
    fmSearch = 'FMASK'
    res3 = [i for i in linkList3 if fmSearch in i]
    if res3 != []:
        stringyRes3 = str(res3)
        strippyRes3 = stringyRes3[2:-2]
        fmUrl = gen_url_pref + strippyRes3
        fMaskLinkList.append(fmUrl)
#print(fMaskLinkList)

#Each UTM cell Fmask page html is retrieved and converted to a useable format
for fmLink in fMaskLinkList:
    linkList4 = []
    fm_content = requests.get(fmLink)
    fm_convert = fm_content.text
    fmSoup = BeautifulSoup(fm_convert)
    #All the links in the UTM cell Fmask page html are stored in a list
    for link in fmSoup.find_all('a'):
        linkList4.append(link.get('href'))
    #If the substring 'FMASK' is found that link is stored in a list of Fmask download links
    finSearch = 'FMASK'
    res4 = [i for i in linkList4 if finSearch in i]
    if res4 != []:
        stringyRes4 = str(res4)
        strippyRes4 = stringyRes4[2:-2]
        #finUrl = gen_url_pref + strippyRes4
        finalLinkList.append(strippyRes4)
#print(finalLinkList)    
 
#Each download link is accessed, saving the file into a unique path derived from the download link's date
for finLink in finalLinkList:
    strFinLink = str(finLink)
    suffixAdd = strFinLink[50:-139]
    suffixClean = suffixAdd.replace("-","")
    filePath = 'D:/Geospatial programming/Major_Project/Sentinel/' + cellCode + '_fmask_' +suffixClean + '.tif'
    urllib.request.urlretrieve(finLink, filePath)

#Each Fmask that has been downloaded is accessed, the file name is restructured into a new save path for the pixel report html
for filename in os.listdir('D:/Geospatial programming/Major_Project/Sentinel/'):
    fileNameSanSuff = filename[0:-4]
    htmlFilePath = 'D:/Geospatial programming/Major_Project/HTMLs/'
    inputFilePath = 'D:/Geospatial programming/Major_Project/Sentinel/'
    htmlSuff = '.html'
    fullHTML = htmlFilePath + fileNameSanSuff + htmlSuff
    fullInput = inputFilePath + filename 
    # Create pixel report using the QGIS raster layer unique values algorithm.
    # Fmask raster is the input and the output is html file that contains totals of the coded pixel values
    processing.run("native:rasterlayeruniquevaluesreport", {'INPUT':fullInput,'BAND':1,'OUTPUT_HTML_FILE':fullHTML})

#Each pixel report html that has been generated is accessed and converted to useable string format
for htmlFile in os.listdir('D:/Geospatial programming/Major_Project/HTMLs/'):
    htmlFilePath = 'D:/Geospatial programming/Major_Project/HTMLs/'
    fullHTMLDir = htmlFilePath + htmlFile
    with open(fullHTMLDir, 'r') as file:
        strHTML = file.read().replace('\n', '')
    #Boolean tests to see if any no data, cloud or cloud shadow pixels were detected
    noDataTest = "</p><p>NODATA" in strHTML
    cloudTest = "</tr><tr><td>2</td><td>" in strHTML
    cShadTest = "</tr><tr><td>3</td><td>" in strHTML
    #Left and right strip around the total pixel number
    totPixelSplit1 = strHTML.split("<p>Total pixel count: ",1)[1]
    totPixelSplit2 = totPixelSplit1.rsplit("</p><p>NODATA", 1)[0]
    fltTotPix = float(totPixelSplit2)
    #Strip to extract no data value and calculation of percent no data coverage
    if noDataTest == True:
        noDataSplit1 = strHTML.split("<p>NODATA pixel count: ",1)[1]
        noDataSplit2 = noDataSplit1.rsplit("</p><table>", 1)[0]
        fltNDPix = float(noDataSplit2)
        noDatPerc = (fltNDPix/fltTotPix)*100
        #print(noDatPerc)
    else:
        noDatPerc = 0
    #Strip to extract cloud cover value and calculation of percent cloud coverage
    if cloudTest == True:
        cloudSplit1 = strHTML.split("</tr><tr><td>2</td><td>",1)[1]
        cloudSplit2 = cloudSplit1.rsplit("</td><td>", 1)[0]
        for i in range(10):
            cloudSplit2 = cloudSplit2.rsplit("</td><td>", 1)[0]
        fltCloudPix = float(cloudSplit2)
        cloudPerc = (fltCloudPix/fltTotPix)*100
        #print(cloudPerc)
    else:
        cloudPerc = 0
    #Strip to extract cloud shadow cover value and calculation of percent cloud shadow coverage
    if cShadTest == True:
        cShadSplit1 = strHTML.split("</tr><tr><td>3</td><td>",1)[1]
        cShadSplit2 = cShadSplit1.rsplit("</td><td>", 1)[0]
        for i in range(10):
            cShadSplit2 = cShadSplit2.rsplit("</td><td>", 1)[0]
        fltCShad = float(cShadSplit2)
        cShadPerc = (fltCShad/fltTotPix)*100
        #print(cloudSplit2)
    else:
        cShadPerc = 0
    #If the coverage of no data, cloud and cloud shadow are all under the specified threshold the date is added to a list for download of the final product
    if noDatPerc <= noDataThresh and cloudPerc <= cloudThresh and cShadPerc <= cShadThresh:
        forListSplit1 = htmlFile.split("_fmask_",1)[1]
        #print(forListSplit1)
        forListSplit2 = forListSplit1.rsplit(".html", 1)[0]
        #print(forListSplit1)
        forListSpacer1 = forListSplit2[:4] + '-' + forListSplit2[4:]
        #print(forListSplit1)
        forListSpacer2 = forListSpacer1[:7] + '-' + forListSpacer1[7:]
        #print(forListSplit1)
        finalDLList.append(forListSpacer2)
#print(finalDLList)

#For each date in the list of dates for product download the corresponding date html in the NCI catalogue is accessed
#A html path is created, retrieved and converted to a useable format
for fDate in finalDLList:
    linkList5 = []
    fDate_url = date_url_pref + fDate + date_url_suff
    #print(date_url)
    fURL_content = requests.get(fDate_url)
    fURL_convert = fURL_content.text
    fSoup = BeautifulSoup(fURL_convert)
    #All the links in the date html are stored in a list
    for link in fSoup.find_all('a'):
        linkList5.append(link.get('href'))
    #If the UTM cell code is found that link is stored in a final list of htmls for the desired UTM cell
    res5 = [i for i in linkList5 if cellCode in i]
    if res5 != []:
        stringyRes5 = str(res5)
        strippyRes5 = stringyRes5[2:-2]
        fCellUrl = gen_url_pref + strippyRes5
        fCellList.append(fCellUrl)
#print(fCellList)

#Each UTM cell html in the final cell list is retrieved and converted to a useable format
for fCellLink in fCellList:
    linkList6 = []
    fCell_content = requests.get(fCellLink)
    fCell_convert = fCell_content.text
    fCellSoup = BeautifulSoup(fCell_convert)
    #All the links in the UTM cell html are stored in a list
    for link in fCellSoup.find_all('a'):
        linkList6.append(link.get('href'))
    #Each link is searched for the substring 'NBART'
    NBARTSearch = 'NBART'
    res6 = [i for i in linkList6 if NBARTSearch in i]
    #If the substring 'NBART" is found that link is stored in a list of htmls for the NBART product page of the desired UTM cell
    if res6 != []:
        stringyRes6 = str(res6)
        strippyRes6 = stringyRes6[2:-2]
        NBARTUrl = gen_url_pref + strippyRes6
        NBARTLinkList.append(NBARTUrl)
#print(NBARTLinkList)

#Each NBART product page html is retrieved and converted to a useable format
for NBARTLink in NBARTLinkList:
    linkList7 = []
    NBART_content = requests.get(NBARTLink)
    NBART_convert = NBART_content.text
    NBARTSoup = BeautifulSoup(NBART_convert)
    #All the links in the NBART product page html are stored in a list
    for link in NBARTSoup.find_all('a'):
        linkList7.append(link.get('href'))
    #Each link is searched for the substrings 'B02', 'B03' or 'B04'
    #If one of these substrings is found that link is stored in a list of htmls for the band product download page of the desired UTM cell
    B02Search = 'B02'
    B03Search = 'B03'
    B04Search = 'B04'
    res7A = [i for i in linkList7 if B02Search in i]
    if res7A != []:
        stringyRes7A = str(res7A)
        strippyRes7A = stringyRes7A[2:-2]
        B02Url = gen_url_pref + strippyRes7A
        B02LinkList.append(B02Url)
    res7B = [i for i in linkList7 if B03Search in i]
    if res7B != []:
        stringyRes7B = str(res7B)
        strippyRes7B = stringyRes7B[2:-2]
        B03Url = gen_url_pref + strippyRes7B
        B03LinkList.append(B03Url)
    res7C = [i for i in linkList7 if B04Search in i]
    if res7C != []:
        stringyRes7C = str(res7C)
        strippyRes7C = stringyRes7C[2:-2]
        B04Url = gen_url_pref + strippyRes7C
        B04LinkList.append(B04Url)
#print(fMaskLinkList)

#Each band 2 product page html is retrieved and converted to a useable format
for B02Link in B02LinkList:
    linkList8A = []
    B02_content = requests.get(B02Link)
    B02_convert = B02_content.text
    B02Soup = BeautifulSoup(B02_convert)
    #All the links in the band 2 product page html are stored in a list
    for link in B02Soup.find_all('a'):
        linkList8A.append(link.get('href'))
    #Each link is searched for the substring 'B02'
    B02Search = 'B02'
    res8A = [i for i in linkList8A if B02Search in i]
    #If the substring 'B02' is found that link is stored in a list of band 2 product download links
    if res8A != []:
        stringyRes8A = str(res8A)
        strippyRes8A = stringyRes8A[2:-2]
        #finUrl = gen_url_pref + strippyRes4
        finB02LinkList.append(strippyRes8A)
#print(finB02LinkList) 

#Each band 3 product page html is retrieved and converted to a useable format
for B03Link in B03LinkList:
    linkList8B = []
    B03_content = requests.get(B03Link)
    B03_convert = B03_content.text
    B03Soup = BeautifulSoup(B03_convert)
    #All the links in the band 3 product page html are stored in a list
    for link in B03Soup.find_all('a'):
        linkList8B.append(link.get('href'))
    B03Search = 'B03'
    res8B = [i for i in linkList8B if B03Search in i]
    #If the substring 'B03' is found that link is stored in a list of band 3 product download links
    if res8B != []:
        stringyRes8B = str(res8B)
        strippyRes8B = stringyRes8B[2:-2]
        #finUrl = gen_url_pref + strippyRes4
        finB03LinkList.append(strippyRes8B)
#print(finB03LinkList) 
   
#Each band 4 product page html is retrieved and converted to a useable format     
for B04Link in B04LinkList:
    linkList8C = []
    B04_content = requests.get(B04Link)
    B04_convert = B04_content.text
    B04Soup = BeautifulSoup(B04_convert)
    #All the links in the band 4 product page html are stored in a list
    for link in B04Soup.find_all('a'):
        linkList8C.append(link.get('href'))
    B04Search = 'B04'
    res8C = [i for i in linkList8C if B04Search in i]
    #If the substring 'B04' is found that link is stored in a list of band 4 product download links
    if res8C != []:
        stringyRes8C = str(res8C)
        strippyRes8C = stringyRes8C[2:-2]
        #finUrl = gen_url_pref + strippyRes4
        finB04LinkList.append(strippyRes8C)
#print(finB04LinkList) 
 
#Each band 2 product download link is accessed, saving the file into a unique path derived from the download link's date        
for finB02Link in finB02LinkList:
    lenB02 = len(finB02Link)
    if lenB02 == 199:
        strFinLink2 = str(finB02Link)
        suffixAdd2 = strFinLink2[50:-139]
        suffixClean2 = suffixAdd2.replace("-","")
        filePath02 = 'D:/Geospatial programming/Major_Project/Sentinel/' + cellCode + '_B02_' + suffixClean2 + '.tif'
    if lenB02 == 166:
        strFinLink2 = str(finB02Link)
        suffixAdd2 = strFinLink2[50:-106]
        suffixClean2 = suffixAdd2.replace("-","")
        filePath02 = 'D:/Geospatial programming/Major_Project/Sentinel/' + cellCode + '_B02_' + suffixClean2 + '.tif'
    urllib.request.urlretrieve(finB02Link, filePath02)
    #print(filePath02)
    
#Each band 3 product download link is accessed, saving the file into a unique path derived from the download link's date        
for finB03Link in finB03LinkList:
    lenB03 = len(finB03Link)
    if lenB03 == 199:
        strFinLink3 = str(finB03Link)
        suffixAdd3 = strFinLink3[50:-139]
        suffixClean3 = suffixAdd3.replace("-","")
        filePath03 = 'D:/Geospatial programming/Major_Project/Sentinel/' + cellCode + '_B03_' + suffixClean3 + '.tif'
    if lenB03 == 166:
        strFinLink3 = str(finB03Link)
        suffixAdd3 = strFinLink3[50:-106]
        suffixClean3 = suffixAdd3.replace("-","")
        filePath03 = 'D:/Geospatial programming/Major_Project/Sentinel/' + cellCode + '_B03_' + suffixClean3 + '.tif'
    urllib.request.urlretrieve(finB03Link, filePath03)
    #print(filePath03)
    
#Each band 4 product download link is accessed, saving the file into a unique path derived from the download link's date        
for finB04Link in finB04LinkList:
    lenB04 = len(finB04Link)
    if lenB04 == 199:
        strFinLink4 = str(finB04Link)
        suffixAdd4 = strFinLink4[50:-139]
        suffixClean4 = suffixAdd4.replace("-","")
        filePath04 = 'D:/Geospatial programming/Major_Project/Sentinel/' + cellCode + '_B04_' + suffixClean4 + '.tif'
    if lenB04 == 166:
        strFinLink4 = str(finB04Link)
        suffixAdd4 = strFinLink4[50:-106]
        suffixClean4 = suffixAdd4.replace("-","")
        filePath04 = 'D:/Geospatial programming/Major_Project/Sentinel/' + cellCode + '_B04_' + suffixClean4 + '.tif'
    urllib.request.urlretrieve(finB04Link, filePath04)
    #print(filePath04)