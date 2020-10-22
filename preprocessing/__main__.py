import argparse
import json
import codecs
from nitf_parser.parser import NitfParser
from preprocessing.main import Preprocessing

if __name__ == '__main__':
    preprocesser = Preprocessing()
    preprocesser_image = preprocesser.do_preprocessing(r"C:\Users\Jakob\Desktop\testImages\2015-01-01-01\1988_result.jp2", "1988_result_tresh.jp2")
    preprocesser_image2 = preprocesser.do_preprocessing(
        r"C:\Users\Jakob\Desktop\testImages\2015-01-01-01\2005.jp2", "2005.jp2")
    preprocesser_image3 = preprocesser.do_preprocessing(
        r"C:\Users\Jakob\Desktop\testImages\2015-01-01-01\1988_udsnit.jp2", "1988_udsnit_tresh.jp2")

