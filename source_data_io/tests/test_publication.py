import pytest
import json

from source_data_io.knox_source_data_io.models.publication import Publication, Article, Paragraph


class TestPublication:
    article: Article
    publication: Publication

    def setup_method(self, method):
        """ setup any state tied to the execution of the given method in a
        class.  setup_method is invoked for every test method of a class.
        """
        self.article = Article()
        self.publication = Publication()

    def test_add_article_adds_article_given_article(self):
        article = Article()
        self.publication.add_article(article)
        assert self.publication.articles.__len__() == 1

    def test_add_article_does_not_add_article_given_string(self):
        self.publication.add_article("string")
        assert self.publication.articles.__len__() < 1

    def test_add_paragraph_adds_paragraph_given_paragraph(self):
        paragraph = Paragraph()
        self.article.add_paragraph(paragraph)
        assert self.article.paragraphs.__len__() == 1

    def test_add_paragraph_does_not_add_paragraph_given_string(self):
        self.article.add_paragraph("string")
        assert self.article.paragraphs.__len__() < 1

    def test_publication_to_json_gives_valid_json_on_call(self):
        output = self.publication.to_json()
        try:
            # Check to see if the output can parsed as JSON
            json.loads(output)
            assert True
        except ValueError:
            pytest.fail("Generated string is not valid JSON")

    def test_byline_is_none_by_default(self):
        assert self.article.byline is None

    def test_add_byline_only_by_name(self):
        self.article.add_byline("Hans Hansen")

        if self.article.byline is not None and len(self.article.byline.name) > 0:
            assert True
        else:
            assert False

    def test_add_byline_only_by_name_and_email(self):
        self.article.add_byline("Hans Hansen", "hans@hansen.dk")
        assert self.article.byline is not None and len(self.article.byline.name) > 0 and len(self.article.byline.email) > 0

    def test_extracted_from_is_empty_list_by_default(self):
        assert isinstance(self.article.extracted_from, list) and len(self.article.extracted_from) is 0

    def test_extracted_from_insert_single_entry_success(self):
        self.article.add_extracted_from("/some/path")
        assert len(self.article.extracted_from) is 1

    def test_extracted_from_insert_single_entry_success(self):
        self.article.add_extracted_from("/some/path")
        assert len(self.article.extracted_from) is 1

    def test_extracted_from_insert_mulitple_entry_success(self):
        self.article.add_extracted_from("/some/path")
        self.article.add_extracted_from("/some/other/path")
        assert len(self.article.extracted_from) is 2

    def test_extracted_from_insert_wrong_type_not_added(self):
        self.article.add_extracted_from(10)
        self.article.add_extracted_from(True)
        assert len(self.article.extracted_from) is 0

    def test_extracted_from_insert_same_link_twice_only_one_added(self):
        self.article.add_extracted_from("/some/path")
        self.article.add_extracted_from("/some/path")

        if len(self.article.extracted_from) > 1:
            assert False
        else:
            assert True

    def teardown_method(self, method):
        """ teardown any state that was previously setup with a setup_method
        call.
        """

