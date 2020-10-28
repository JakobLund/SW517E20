import codecs
import configparser
import os
import re
from datetime import datetime
from xml.dom import minidom

from knox_source_data_io.io_handler import *
from xlwt import Workbook

from crawler.publication import *
from initial_ocr.teseract_module import TesseractModule
from nitf_parser.parser import NitfParser
from preprocessing.main import Preprocessing


class Crawler:
    config = configparser.ConfigParser()
    config.read('config.ini')
    nitf_parser = NitfParser()
    tesseract_module = TesseractModule()

    def _init__(self):
        pass

    def run_crawler(self, arg_object):
        """ Runs the crawler for all specified file formats and call their respected modules
        :param arg_object: object that stores the program arguments
        """
        publication = Publication()
        publication.publisher = "Nordjyske Medie"
        publication.published_at = "Some time"
        publication.publication = "A newspaper"
        publication.pages = 0

        folders = self.__manage_folder_cache(arg_object)
        folders = self.__check_and_filter_dates(arg_object, folders)

        # loops through all the folders in the path and their respective files.
        for folder in folders:
            files = self.__find_relevant_files_in_directory(folder['path'])
            self.erode_dilation_osv(files)

    def no_pre(self, files):
        wb = Workbook()
        nope = wb.add_sheet('NoPre')

        sheets = [nope]

        for sheet in sheets:
            sheet.write(0, 0, "Methods")

        i = 0
        for file in files:
            # checks if it is a .jp2 file. if true, the ocr is called
            if ".jp2" in file:
                wb = self.__testing_data_no_pre(wb, file, i)
            i += 1
        wb.save('noPre.xls')

    def thresh(self, files):
        wb = Workbook()
        mean = wb.add_sheet('Mean')
        gaussian = wb.add_sheet('Gaussian')

        sheets = [mean, gaussian]

        for sheet in sheets:
            sheet.write(0, 0, "Methods")

        i = 0
        for file in files:
            # checks if it is a .jp2 file. if true, the ocr is called
            if ".jp2" in file:
                wb = self.__testing_data_threshholding(wb, file, i)
            i += 1
        wb.save('thresholding.xls')

    def blur(self, files):
        wb = Workbook()
        median = wb.add_sheet('Median')
        gaussian = wb.add_sheet('Gaussian')
        averaging = wb.add_sheet('Averaging')

        sheets = [median, gaussian, averaging]

        for sheet in sheets:
            sheet.write(0, 0, "Methods")

        i = 0
        for file in files:
            # checks if it is a .jp2 file. if true, the ocr is called
            if ".jp2" in file:
                wb = self.__testing_data_blur(wb, file, i)
            i += 1
        wb.save('blur_without_bilateral.xls')

    def bilateral(self, files):
        wb = Workbook()
        bil = wb.add_sheet('Bilateral')

        sheets = [bil]

        for sheet in sheets:
            sheet.write(0, 0, "Methods")

        i = 0
        for file in files:
            # checks if it is a .jp2 file. if true, the ocr is called
            if ".jp2" in file:
                wb = self.__testing_data_bilateral_blur(wb, file, i)
            i += 1
        wb.save('bilateral.xls')

    def erode_dilation_osv(self, files):
        wb = Workbook()
        erode = wb.add_sheet('Erode')
        dilate = wb.add_sheet('Dilate')
        opening = wb.add_sheet('Opening')
        closing = wb.add_sheet('Closing')
        erode_mean = wb.add_sheet('Erode_mean')
        dilate_mean = wb.add_sheet('Dilate_mean')
        opening_mean = wb.add_sheet('Opening_mean')
        closing_mean = wb.add_sheet('Closing_mean')

        sheets = [erode, dilate, opening, closing, erode_mean, dilate_mean, opening_mean, closing_mean]

        for sheet in sheets:
            sheet.write(0, 0, "Methods")

        i = 0
        for file in files:
            # checks if it is a .jp2 file. if true, the ocr is called
            if ".jp2" in file:
                wb = self.__testing_data_erosion_dilation_opening_closing(wb, file, i)
            i += 1
        wb.save('erode_dilate_osv.xls')

    def deskew(self, files):
        wb = Workbook()
        deskew = wb.add_sheet('Deskew')

        deskew.write(0, 1, "With")
        deskew.write(0, 2, "Without")

        i = 1
        for file in files:
            # checks if it is a .jp2 file. if true, the ocr is called
            if ".jp2" in file:
                preprocessing = Preprocessing()
                image = preprocessing.do_preprocessing_deskew(file)
                original_image = preprocessing.do_no_preprocessing(file)
                wb.get_sheet(1).write(i, 1, self.tesseract_module.run_tesseract_on_image(image, file))
                wb.get_sheet(1).write(i, 2, self.tesseract_module.run_tesseract_on_image(original_image, file))
                i += 1
        wb.save('deskew.xls')

    def __testing_data_bilateral_blur(self, wb, file, i):
        preprocesser = Preprocessing()

        d_value = 1
        row = 1
        while d_value <= 10:
            sigma_color = 1
            while sigma_color <= 200:
                sigma_space = 1
                while sigma_space <= 200:
                    gaussian = preprocesser.do_preprocessing_bilateral(file, d_value, sigma_color, sigma_space)
                    wb.get_sheet(0).write(row, i + 5, self.tesseract_module.run_tesseract_on_image(gaussian, file))

                    if i == 0:
                        wb.get_sheet(0).write(row, 0, "Grayscale")
                        wb.get_sheet(0).write(row, 1, "Kernel: " + str(d_value))
                        wb.get_sheet(0).write(row, 2, "Sigma color: " + str(sigma_color))
                        wb.get_sheet(0).write(row, 3, "Sigma space: " + str(sigma_space))
                    row += 1
                    sigma_space += 20
                sigma_color += 20
            d_value += 1
        return wb

    def __testing_data_blur(self, wb, file, i):
        preprocesser = Preprocessing()

        kernel_value = 3
        row = 1
        gauss_row = 1
        while kernel_value <= 11:
            averaging = preprocesser.do_preprocessing_averaging(file, kernel_value)
            median = preprocesser.do_preprocessing_median(file, kernel_value)
            wb.get_sheet(0).write(row, i + 3, self.tesseract_module.run_tesseract_on_image(median, file))
            wb.get_sheet(2).write(row, i + 3, self.tesseract_module.run_tesseract_on_image(averaging, file))

            if i == 0:
                wb.get_sheet(0).write(row, 0, "Grayscale")
                wb.get_sheet(0).write(row, 1, "Kernel: " + str(kernel_value))

                wb.get_sheet(2).write(row, 0, "Grayscale")
                wb.get_sheet(2).write(row, 1, "Kernel: " + str(kernel_value))

            sigma = 1
            while sigma <= 10:
                gaussian = preprocesser.do_preprocessing_gauss_blur(file, kernel_value, sigma)
                wb.get_sheet(1).write(gauss_row, i + 4, self.tesseract_module.run_tesseract_on_image(gaussian, file))

                if i == 0:
                    wb.get_sheet(1).write(gauss_row, 0, "Grayscale")
                    wb.get_sheet(1).write(gauss_row, 1, "Kernel: " + str(kernel_value))
                    wb.get_sheet(1).write(gauss_row, 2, "Sigma: " + str(sigma))
                sigma += 1
                gauss_row += 1
            row += 1
            kernel_value += 2
        return wb

    def __testing_data_erosion_dilation_opening_closing(self, wb, file, i):
        preprocesser = Preprocessing()

        kernel_value = 3
        row = 1

        while kernel_value <= 19:
            iteration_value = 1
            while iteration_value <= 5:
                dilate_image = preprocesser.do_preprocessing_dilate(file, kernel_value, iteration_value)
                erode_image = preprocesser.do_preprocessing_erode(file, kernel_value, iteration_value)
                opening_image = preprocesser.do_preprocessing_opening(file, kernel_value, iteration_value)
                closing_image = preprocesser.do_preprocessing_closing(file, kernel_value, iteration_value)
                wb.get_sheet(0).write(row, i + 4, self.tesseract_module.run_tesseract_on_image(dilate_image, file))
                wb.get_sheet(1).write(row, i + 4, self.tesseract_module.run_tesseract_on_image(erode_image, file))
                wb.get_sheet(2).write(row, i + 4, self.tesseract_module.run_tesseract_on_image(opening_image, file))
                wb.get_sheet(3).write(row, i + 4, self.tesseract_module.run_tesseract_on_image(closing_image, file))

                mean_dilate_image = preprocesser.do_preprocessing_mean_dilation(file, kernel_value, iteration_value)
                mean_erosion_image = preprocesser.do_preprocessing_mean_erosion(file, kernel_value, iteration_value)
                mean_opening_image = preprocesser.do_preprocessing_mean_opening(file, kernel_value, iteration_value)
                mean_closing_image = preprocesser.do_preprocessing_mean_closing(file, kernel_value, iteration_value)
                wb.get_sheet(4).write(row, i + 4, self.tesseract_module.run_tesseract_on_image(mean_dilate_image, file))
                wb.get_sheet(5).write(row, i + 4, self.tesseract_module.run_tesseract_on_image(mean_erosion_image, file))
                wb.get_sheet(6).write(row, i + 4, self.tesseract_module.run_tesseract_on_image(mean_opening_image, file))
                wb.get_sheet(7).write(row, i + 4, self.tesseract_module.run_tesseract_on_image(mean_closing_image, file))

                if i == 0:
                    wb.get_sheet(0).write(row, 0, "Grayscale")
                    wb.get_sheet(0).write(row, 1, "Kernel: " + str(kernel_value))
                    wb.get_sheet(0).write(row, 2, "Dilation iteration: " + str(iteration_value))

                    wb.get_sheet(1).write(row, 0, "Grayscale")
                    wb.get_sheet(1).write(row, 1, "Kernel: " + str(kernel_value))
                    wb.get_sheet(1).write(row, 2, "Erosion iteration: " + str(iteration_value))

                    wb.get_sheet(2).write(row, 0, "Grayscale")
                    wb.get_sheet(2).write(row, 1, "Kernel: " + str(kernel_value))
                    wb.get_sheet(2).write(row, 2, "Opening iteration: " + str(iteration_value))

                    wb.get_sheet(3).write(row, 0, "Grayscale")
                    wb.get_sheet(3).write(row, 1, "Kernel:  " + str(kernel_value))
                    wb.get_sheet(3).write(row, 2, "Closing iteration: " + str(iteration_value))

                    wb.get_sheet(4).write(row, 0, "Grayscale")
                    wb.get_sheet(4).write(row, 1,  "Kernel:  " + str(kernel_value))
                    wb.get_sheet(4).write(row, 2, "Dilation iteration: " + str(iteration_value))

                    wb.get_sheet(5).write(row, 0, "Grayscale")
                    wb.get_sheet(5).write(row, 1 , "Kernel:  " + str(kernel_value))
                    wb.get_sheet(5).write(row, 2, "Erosion iteration: " + str(iteration_value))

                    wb.get_sheet(6).write(row, 0, "Grayscale")
                    wb.get_sheet(6).write(row, 1, "Kernel:  " + str(kernel_value))
                    wb.get_sheet(6).write(row, 2, "Opening iteration: " + str(iteration_value))

                    wb.get_sheet(7).write(row, 0, "Grayscale")
                    wb.get_sheet(7).write(row, 1, "Kernel:  " + str(kernel_value))
                    wb.get_sheet(7).write(row, 2, "Closing iteration: " + str(iteration_value))
                iteration_value += 1
                row += 1
            kernel_value += 2
        return wb
    
    def __testing_data_threshholding(self, wb, file, i):
        preprocesser = Preprocessing()

        value = 3
        col = 1

        while value <= 19:
            c = 1
            while c <= 10:
                gauss_image = preprocesser.do_preprocessing_gauss(file, value, c)
                mean_image = preprocesser.do_preprocessing_mean(file, value, c)
                wb.get_sheet(0).write(col, i + 3, self.tesseract_module.run_tesseract_on_image(gauss_image, file))
                wb.get_sheet(1).write(col, i + 3, self.tesseract_module.run_tesseract_on_image(mean_image, file))

                if i == 0:
                    wb.get_sheet(0).write(col, 0, "Grayscale")
                    wb.get_sheet(0).write(col, 1, "Gauss: " + str(value) + ", " + str(c))

                    wb.get_sheet(1).write(col, 0, "Grayscale")
                    wb.get_sheet(1).write(col, 1, "Mean: " + str(value) + ", " + str(c))
                c += 1
                col += 1
            value += 2
        return wb

    def __testing_data_no_pre(self, wb, file, i):
        preprocesser = Preprocessing()

        image = preprocesser.do_no_preprocessing(file)
        wb.get_sheet(0).write(1, i + 3, self.tesseract_module.run_tesseract_on_image(image, file))

        return wb

    def __testing_data_v2(self, wb, file, i):
        preprocesser = Preprocessing()

        value = 3
        noise_col = 1

        while value <= 19:
            c = 1
            while c <= 10:
                noise_value = 1
                while noise_value < 10:
                    noise_gauss_image = preprocesser.do_preprocessing_noise_gauss(file, value, c, noise_value)

                    wb.get_sheet(5).write(noise_col, i, self.tesseract_module.run_tesseract_on_image(noise_gauss_image, file))

                    if i == 0:
                        wb.get_sheet(5).write(noise_col, 5, "Grayscale")
                        wb.get_sheet(5).write(noise_col, 6, "Noise: " + str(noise_value))
                        wb.get_sheet(5).write(noise_col, 7, "Gauss: " + str(value) + ", " + str(c))
                    noise_value += 2
                    noise_col += 1
                c += 1
            value += 2
        return wb

    def __manage_folder_cache(self, arg_object):
        """ If clear cache arg is given, the cache is cleared. If not the folders are loaded
        :param arg_object:
        :return: returns the found folders
        """
        if arg_object.clearcache or not path.exists(self.config['structure']['cache_file']):
            print("Could not find cache, or clear cache flag was enabled.. Searching file structure..")
            # recalculate folders.json
            folders = self.__find_folders_recursively(arg_object.path)

            if len(folders) == 0:
                raise Exception("No files found in the input folder")

            # sorts the folders after year,month, date
            folders.sort(key=lambda folder: self.__date_to_int(folder))
            self.__save_cache_file(folders, self.config['structure']['cache_file'])
        else:
            # load folders from folders.json
            folders = self.__load_from_json(self.config['structure']['cache_file'])

        return folders

    def __check_and_filter_dates(self, arg_object, folders):
        """ Set arg_object to and from dates and verifies them. Filter the folders by date

        :param arg_object: object that represents the program arguments
        :param folders: the folders to sort
        :return: sorted folders
        """
        # if a to-date is present, we set to-date to last element
        if not hasattr(arg_object, "to_date"):
            # from = folders
            arg_object.to_date = folders[-1]

        # if a from-date is present, we set from-date to first element
        if not hasattr(arg_object, "from_date"):
            # from = folders[0]
            arg_object.from_date = folders[0]

        # checks if the to date is after the from date
        int_from_date = self.__date_to_int(arg_object.from_date)
        int_to_date = self.__date_to_int(arg_object.to_date)
        if int_from_date > int_to_date:
            raise Exception("The to-date is before the from-date.")

        # filter folders by dates
        to_date = self.__date_to_int(arg_object.to_date)
        from_date = self.__date_to_int(arg_object.from_date)
        folders = [folder for folder in folders if from_date <= self.__date_to_int(folder) <= to_date]

        return folders

    @staticmethod
    def __date_to_int(a):
        """ converts a dictionary with attributes year, month and date to an int, useful for comparing dates/sorting.

        :param a: object that has year, month, and date properties
        :return: an int that represents the objects date
        """
        return int(str(a['year']) + str(a['month']).zfill(2) + str(a['date']).zfill(2))

    def __find_folders_recursively(self, directory):
        """ recursive function that finds all the dire that contains the wanted files

        :param directory:
        :return: folder that has been found
        """
        print("Searching in " + directory)

        #  finds all sub directories in the directory
        dirs = next(os.walk(directory))[1]

        found_folders = []

        # gets regex from config file that matches the target dirs name
        pattern_strings = self.config['structure']['final-folder-regex'].split(",")
        pattern_strings = [x.split("|") for x in pattern_strings]

        regexs = [
            {
                'compiled': re.compile(pattern_string[0]),
                'original': pattern_string[0],
                'limits': [int(y) for y in pattern_string[1:7]]  # 6 because there are three sets of base and bounds
            }

            for pattern_string in pattern_strings]

        for curr_dir in dirs:
            # let's check if the current dir is a target dir by matching to regexs
            filtered_regexs = filter(lambda regex: re.match(regex['compiled'], curr_dir), regexs)
            matched_regex = next(filtered_regexs, None)
            if matched_regex is not None:
                # current dir IS a target dir, append to list to return later.
                limits = matched_regex['limits']
                found_folders.append(
                    {
                        'path': directory + "/" + curr_dir,
                        'year': int(curr_dir[limits[0]:limits[1]]),
                        'month': int(curr_dir[limits[2]:limits[3]]),
                        'date': int(curr_dir[limits[4]:limits[5]])
                    }
                )
            else:
                # current dir is NOT a target dir. Let's search that dir for target-dirs.
                found_folders.extend(self.__find_folders_recursively(directory + "/" + curr_dir))
        return found_folders

    @staticmethod
    def __save_to_json(publication):
        handler = IOHandler(Generator(app="This app", version=1.0, generated_at=datetime.now().isoformat()),
                            "http://iptc.org/std/NITF/2006-10-18/")
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'output.json')

        with open(filename, 'w') as outfile:
            handler.write_json(publication, outfile)

    @staticmethod
    def __load_from_json(filename):
        """Loads a json file and returns its data

        :param filename: json file to be loaded
        :return: data from json file
        """
        with open(filename) as json_file:
            data = json.load(json_file)
        return data

    def __find_relevant_files_in_directory(self, directory):
        """Finds all files in a directory and checks them again the file type
        white and blacklist.

        :param directory: path to directory
        :return: all found files that isn't in the blacklist/whitelist
        """

        files = self.__find_all_files_recursively(directory)
        blacklist = self.config['structure']['blacklist'].split(",")
        whitelist = self.config['structure']['whitelist'].split(",")
        # checks whether the file should be appended, by using config white- and blacklist
        found_files = []
        for file in files:
            if self.__is_string_in_list(file, blacklist) or not self.__is_string_in_list(file, whitelist):
                continue
            if ".xml" in file:
                if self.__is_file_valid_nitf(directory + "/" + file):
                    found_files.append(directory + "/" + file)
            else:
                found_files.append(directory + "/" + file)
            # Add new file-formats here!
        return found_files

    def __find_all_files_recursively(self, directory):
        """Recursively finds all files in a directory

        :param directory: path to directory
        :return: list of found files
        """
        print(f"Searching directory {directory} for files..")
        walk = next(os.walk(directory))
        files = walk[2]  # gets files from specified directory
        for walking_dir in walk[1]:  # goes through all directories from the found directories
            # calls method recursively to get sub directories
            found_files = self.__find_all_files_recursively(directory + "/" + walking_dir)
            for file in found_files:
                files.append(walking_dir + "/" + file)
        return files

    @staticmethod
    def __is_file_valid_nitf(xml_path):
        """Checks if the XML file given has the nitf:nitf tag

        :param xml_path: path to the XML file
        :return: true or false, depending on whether it's a nitf file or not
        """
        xml_doc = minidom.parse(xml_path)
        if len(xml_doc.getElementsByTagName('nitf:nitf')) != 0:
            # todo file is nitf, lets check if it is a valid article.
            return True
        return False

    @staticmethod
    def __is_string_in_list(string, checklist):
        """Checks if the string contains any words in the list (useful for black- and whitelisting)

        :param string: string to be checked
        :param checklist: white- or blacklist from config file
        :return: true or false, depending on whether the string appears in the list
        """
        for listed_item in checklist:
            if listed_item in string:
                return True
        return False

    @staticmethod
    def __save_cache_file(folders, file_name):
        """ Dumps all files from a folder
        :param folders: folders with files to dump
        :param file_name: output filename
        """
        with codecs.open(file_name, 'w', encoding="utf-8") as outfile:
            json.dump(folders, outfile, indent=4, ensure_ascii=False)  # 4 is standard indent
