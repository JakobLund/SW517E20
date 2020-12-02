import string
from datetime import datetime, timezone
from os import environ
from xml.dom import minidom
import re
from knox_source_data_io.models.publication import Article
from pytesseract import pytesseract
from alto_segment_lib.segment_module import SegmentModule
from ocr.tesseract import TesseractModule
environ["OPENCV_IO_ENABLE_JASPER"] = "true"
import cv2


class OCRRunner:

    def run_ocr(self, file, language='dan', tesseract_path=None):

        image = cv2.imread(file.path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        segments = SegmentModule.run_segmentation(file.path.split(".")[0])

        tessdata = "dan"

        pattern = re.compile("\\d\\d\\d\\d-\\d\\d-\\d\\d")
        result = pattern.search(file.name)
        file_date = result.group(0)
        file_date = file_date.replace("-", "")

        #file_date = file.name.split("-")[1]

        if int(file_date) < 19280517:
            tessdata = "dan_best_gothic_fine_tune"

        article = Article()
        articles = []
        for segment in segments:
            if len(segments) > 300:
                break

            if segment.y1 <= segment.y2 and segment.x1 <= segment.x2:
                cropped_image = image[segment.y1:segment.y2+1, segment.x1:segment.x2+1]
            else:
                continue

            if segment.type == "headline":
                # todo implement when ordering is done
                articles.append(article)
                article = Article()
                article.page = self.__find_page_number(file.path)
                headline = TesseractModule.from_file(cropped_image, tessdata).to_paragraphs()
                if len(headline) > 0:
                    article.headline = headline[0].value

            if segment.type == "paragraph":
                paragraphs = TesseractModule.from_file(cropped_image, tessdata).to_paragraphs()
                paragraphs = self.__remove_advertisement_and_images(paragraphs)
                if len(paragraphs) > 0:
                    [article.add_paragraph(p) for p in paragraphs]
                    article.add_extracted_from(file.path)

            if segment.type == "subhead":
                # todo implement when ordering is done
                subhead = TesseractModule.from_file(cropped_image, tessdata).to_paragraphs()
                if len(subhead) > 0:
                    article.subhead = subhead[0].value

            if segment.type == "lead":
                lead = TesseractModule.from_file(cropped_image, tessdata).to_paragraphs()
                if len(lead) > 0:
                    article.lead = lead[0].value

        if article.page == 0:
            article.page = self.__find_page_number(file.path)

        articles.append(article)

        publication = self.__convert_articles_into_publication(articles, file)

        return publication

    def __convert_articles_into_publication(self, articles, file):
        publication = TesseractModule.from_articles_to_publication(articles)
        publication.publication = self.__find_publication(file.name)
        publication = self.__set_publisher("Nordjyske Medier", publication)
        publication.published_at = self.__find_published_at(file.path)
        publication = self.__remove_empty_paragraphs(publication)

        return publication

    @staticmethod
    def __set_publisher(publisher, publication):
        publication.publisher = publisher
        return publication

    @staticmethod
    def __find_publication(file_name):
        """
        Finds publisher name from file name
        @param file_name: name of file
        @return: publisher name
        """
        # todo bliver ikke sat mellemrum men ved ikke om det er vigtigt
        return file_name.split("-")[0].title()

    @staticmethod
    def __find_page_number(file_path):
        """
        Finds page number from alto.xml file
        @param file_path: name of file
        @return: page number
        """
        page_elements = minidom.parse(file_path.split('.')[0] + ".alto.xml").getElementsByTagName("Page")

        return int(page_elements[0].attributes['PHYSICAL_IMG_NR'].value)

    @staticmethod
    def __find_published_at(file_path):
        published_at = minidom.parse(file_path.split('.')[0] + ".alto.xml").\
            getElementsByTagName("fileName")[0].firstChild.data

        pattern = re.compile("\\d\\d\\d\\d-\\d\\d-\\d\\d")
        result = pattern.search(published_at)
        result = result.group(0)

        if re.match(pattern, result):
            return datetime(year=int(result[0:4]), month=int(result[5:7]), day=int(result[8:10]), tzinfo=timezone.utc)\
                .isoformat()

    @staticmethod
    def __remove_advertisement_and_images(paragraphs):
        # if text contains a lot of numbers it might be a TV guide or "aktier"
        ok_paragraphs = []

        special_chars = set(string.punctuation.replace("_", ""))
        for paragraph in paragraphs:
            num_counter = 0
            special_char_counter = 0
            total_char_count = 0

            total_char_count += len(paragraph.value.strip())
            words = paragraph.value.split(" ")
            for word in words:
                num_counter += sum(char.isdigit() for char in word)
                special_char_counter += sum(char in special_chars for char in word)

            if not (special_char_counter > total_char_count/4 or num_counter > total_char_count/2
                    or special_char_counter + num_counter > total_char_count/3):
                ok_paragraphs.append(paragraph)

        return ok_paragraphs

    @staticmethod
    def __remove_empty_paragraphs(publication):
        correct_paragraphs = []
        for article in publication.articles:
            paragraphs = article.paragraphs

            for paragraph in paragraphs:
                if len(paragraph.value) > 0:
                    correct_paragraphs.append(paragraph)

            article.paragraphs = correct_paragraphs

        return publication
