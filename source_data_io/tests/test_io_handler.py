from io import StringIO

import pytest

from source_data_io.knox_source_data_io.io_handler import *
# from extras.publication import Publication, Article, Byline, Paragraph


class TestIOHandler:
    handler: IOHandler

    def setup_method(self, method):
        self.handler = IOHandler(Generator(app="This app", version=1.0), "Schema")

    def test_write_json_returns_valid_json_given_model_subclass(self):
        content_obj = SubModelObj()

        # Create StringIO object to store the output of the method
        outfile = StringIO()

        # Call method
        self.handler.write_json(content_obj, outfile)

        # Read the output
        outfile.seek(0)
        output_content = outfile.read()

        try:
            # Check to see if the output can parsed as JSON
            json.loads(output_content)
        except ValueError:
            pytest.fail("Generated string is not valid JSON")

        assert True

    def test_write_json_returns_nothing_if_obj_is_not_model_subclass(self):
        content_obj = SubModelObj()

        # Create StringIO object to store the output of the method
        outfile = StringIO()

        try:
            self.handler.write_json(content_obj, outfile)
        except ValueError as e:
            assert str(e) == "Object need to be a subclass of Model..."

    def test_write_json_adds_correct_meta_data(self):
        content_obj = SubModelObj()

        # Create StringIO object to store the output of the method
        outfile = StringIO()

        self.handler.write_json(content_obj, outfile)

        outfile.seek(0)
        json_content = json.loads(outfile.read())

        generated_generator = Generator(app=json_content['generator']['app'], version=json_content['generator']['version'])
        generated_schema_location = json_content['schema']
        generated_type = json_content['type']

        assert generated_generator.app == "This app" and generated_generator.version == 1.0\
               and generated_schema_location == "Schema"\
               and generated_type == content_obj.__class__.__name__

    def test_write_json_generates_json_with_the_correct_data(self):
        content_obj = SubModelObj()
        content_obj.email = "email@comp.com"
        content_obj.name = "name"

        # Create StringIO object to store the output of the method
        outfile = StringIO()

        self.handler.write_json(content_obj, outfile)

        outfile.seek(0)
        generated_json_content = json.loads(outfile.read())

        expected_json_content = content_obj.to_json()

        assert generated_json_content["content"]["email"] == json.loads(expected_json_content)["email"] and generated_json_content["content"]["name"] == json.loads(expected_json_content)["name"]

    def test_read_json_fails_due_to_file_not_existing(self):
        try:
            with open("/this/path/does/not/exist/and/will/cause/the/method/to/fail", 'r') as json_file:
                self.handler.read_json(json_file)
        except OSError:
            assert True

    def test_convert_to_dict_adds_all_variables_from_the_obj_to_the_dict(self):
        publication = SubModelObj()
        output = IOHandler.convert_obj_to_dict(publication)

        # Check if all attributes are represented in the dictionary
        attributes = vars(publication)
        for attribute in attributes:
            if attribute not in output:
                pytest.fail(f"The dictionary does not contain the attribute: {str(attribute)}")

        assert True

    def test_convert_to_dict_adds_class_reference_to_dict(self):
        publication = SubModelObj()
        output = IOHandler.convert_obj_to_dict(publication)

        if output.get("__class__") != publication.__class__.__name__:
            pytest.fail(f"The dictionary does not contain reference to originating class")

    def test_convert_to_dict_adds_module_reference_to_dict(self):
        publication = SubModelObj()
        output = IOHandler.convert_obj_to_dict(publication)

        if output.get("__module__") != publication.__module__:
            pytest.fail(f"The dictionary does not contain reference to originating module")

        assert True

    def test_dict_to_obj_receives_dict_with_class_and_returns_obj_of_class(self):
        sub_model = SubModelObj()
        sub_model.name = "Hans Hansen"
        sub_model.email = "hans@hansen.dk"

        dictionary = sub_model.__dict__
        dictionary["__class__"] = "SubModelObj"
        dictionary["__module__"] = "tests.test_io_handler"

        output = IOHandler.convert_dict_to_obj(dictionary)
        if not isinstance(output, SubModelObj):
            pytest.fail("The output is not of the given type")
        assert True

    def test_dict_to_obj_receives_dict_without_class_and_returns_the_same_dictionary(self):
        sub_model = SubModelObj()
        sub_model.name = "Hans Hansen"
        sub_model.email = "hans@hansen.dk"
        dictionary = sub_model.__dict__

        output = IOHandler.convert_dict_to_obj(dictionary)

        assert output == dictionary

    def test_dict_to_obj_receives_dict_with_class_and_returns_obj_with_same_variables(self):
        sub_model = SubModelObj()
        sub_model.name = "Hans Hansen"
        sub_model.email = "hans@hansen.dk"

        dictionary = sub_model.__dict__
        dictionary["__class__"] = "SubModelObj"
        dictionary["__module__"] = "tests.test_io_handler"

        output = IOHandler.convert_dict_to_obj(dictionary)
        for var in dictionary.keys():
            if not hasattr(output, var):
                pytest.fail("The output is not of the given type")

        assert True


class SubModelObj(Model):
    name: str
    email: str

    def __init__(self, values: dict = None, **kwargs):
        values = values if values is not None else kwargs
        self.name = values.get("name", "")
        self.email = values.get("email", "")
