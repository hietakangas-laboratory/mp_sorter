'''
Author: Jack Morikka.
A programme to save MP files from tiffs with imageJ MP selection
and then to place these in the corresponding output directories in an MP directory'''

import os
import logging
import shutil
import pandas
from ij import IJ
import csv


def main(tiff_dir, analysis_dir):
    logging.basicConfig(
        filename='%s/MP_sorter.log' % tiff_dir,
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%d-%m-%Y %H:%M:%S')

    logging.info('Starting vector sorter')
    py_file_loc = os.path.realpath(__file__)
    mps_path = os.path.dirname(os.path.abspath(py_file_loc))
    runmacros(tiff_dir, mps_path)
    movevectorfiles(tiff_dir, analysis_dir)
    logging.info("Process finished")

def runmacros(tiff_dir, mps_path):

    for root, dirs, files in os.walk(tiff_dir):
        for file in files:
            if file.endswith(".tiff") or file.endswith(".tif"):
                try:
                    logging.info('.tiff file discovered: %s' % file)
                    tiff_path = os.path.join(root, file)
                    IJ.runMacroFile(mps_path + r"\mp_saver.ijm", tiff_path)
                    IJ.run("Close All")
                except Exception as e:
                    logging.exception(str(e))

    logging.info("MP.csv files created")


def movevectorfiles(tiff_dir, analysis_dir):

    mp_paths = []

    for root, dirs, files in os.walk(tiff_dir):
        for file in files:
            if file.endswith("MP.txt"):
                logging.info("MP.txt file discovered: %s" % file)
                mp_path = os.path.join(root, file)
                mp_paths.append(mp_path)

    logging.info(mp_paths)
    dirpaths = []


    for root, dirs, files in os.walk(analysis_dir):
        for dir in dirs:
            dirpath = os.path.join(root, dir)
            logging.info("Sample analysis directory found: %s"% dirpath)
            dirpaths.append(dirpath)

    logging.info(dirpaths)

    logging.info("Attempting to copy MP.csv files to analysis directories")

    for mppath in mp_paths:
        for dirpath in dirpaths:
            if (os.path.basename(dirpath)).lower() in (os.path.basename(mppath)).lower():
                logging.info((os.path.basename(mppath)).lower())
                logging.info((os.path.basename(dirpath)).lower())
                try:
                    prex = os.path.basename(dirpath).lower() + '_MP_statistics'
                    mpdirpath = os.path.join(dirpath, prex)
                    logging.info("Associated directory for %s found: %s" % (mppath, dirpath))
                    logging.info("Making directory for MP statistics: %s" % mpdirpath)
                    if not os.path.exists(mpdirpath):
                        os.mkdir(mpdirpath)
                    final_dest = os.path.join(mpdirpath, os.path.basename(mppath))
                    logging.info("Moving %s to %s" % (mppath, mpdirpath))
                    shutil.move(mppath, final_dest)
                    vec_rnme = mpdirpath + "\Position.csv"
                    logging.info(vec_rnme)
                    logging.info("Removing old Vector.csv or Vector.txt files if any")
                    if os.path.exists(vec_rnme):
                        os.remove(vec_rnme)
                    logging.info("Renaming %s to %s" % (final_dest, vec_rnme))
                    os.rename(final_dest, vec_rnme)
                    df1 = pandas.read_csv(vec_rnme, header=None)
                    df1.to_csv(vec_rnme, header=["Position X", "Position Y"])
                except Exception as e:
                    logging.exception(str(e))

    logging.info("MP files moved")

#@String tiff_dir
#@String analysis_dir


main(tiff_dir, analysis_dir)

