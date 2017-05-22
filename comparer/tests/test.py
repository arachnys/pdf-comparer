import unittest
import os
from ..converter import PdfToPngConverter
from ..main import PdfComparer
from ..diff import ImageDiff
from ..comparison import ImageComparison


TEST_DATA_DIR = os.path.realpath('./comparer/tests/test_data')


def _get_file_from_test_dir(file_name):
  relative_path = os.path.join(TEST_DATA_DIR, file_name)
  absolute_path = os.path.realpath(relative_path)
  return absolute_path


class ConverterTest(unittest.TestCase):
  def test_it_should_convert_each_page_of_the_pdf_to_a_png(self):
    test_pdf = _get_file_from_test_dir("converter_test.pdf")
    converter = PdfToPngConverter(test_pdf)
    pngs = converter.convert()

    relative_paths_to_pngs = [
      _get_file_from_test_dir("converter_test_001.png"),
      _get_file_from_test_dir("converter_test_002.png"),
      _get_file_from_test_dir("converter_test_003.png"),
      _get_file_from_test_dir("converter_test_004.png"),
      _get_file_from_test_dir("converter_test_005.png"),
      _get_file_from_test_dir("converter_test_006.png"),
      _get_file_from_test_dir("converter_test_007.png"),
      _get_file_from_test_dir("converter_test_008.png"),
    ]
    baseline_pngs = [os.path.realpath(p) for p in relative_paths_to_pngs]

    for baseline_png, comparee_png in zip(pngs, baseline_pngs):
      comparison = ImageComparison(baseline_png, comparee_png, max_rms_error=0)
      self.assertTrue(comparison.run())


TEST_CASES = [
  {
    'test_name': 'test_comparing_the_same_image_with_threshold_0_returns_true',
    'baseline': _get_file_from_test_dir("converter_test_001.png"),
    'comparee': _get_file_from_test_dir("converter_test_001.png"),
    'max_rms_error': 0,
    'is_similar': True,
  },
  {
    'test_name': 'test_comparing_different_images_with_threshold_0_returns_false',
    'baseline': _get_file_from_test_dir("converter_test_001.png"),
    'comparee': _get_file_from_test_dir("converter_test_002.png"),
    'max_rms_error': 0,
    'is_similar': False
  },
  {
    'test_name': 'test_comparing_slight_different_images_with_nonzero_threshold_returns_true',
    'baseline': _get_file_from_test_dir("comparison_test_001.png"),
    'comparee': _get_file_from_test_dir("comparison_test_2_001.png"),
    'max_rms_error': 10,
    'is_similar': True
  },
  {
    'test_name': 'test_comparing_very_different_images_with_nonzero_threshold_returns_false',
    'baseline': _get_file_from_test_dir("comparison_very_different_001.png"),
    'comparee': _get_file_from_test_dir("comparison_very_different_2_001.png"),
    'max_rms_error': 10,
    'is_similar': False
  }
]


class ImageComparisonMeta(type):
  def __new__(metaclass, name, bases, dict_):
    def generate_test(params):
      def test(self):
        comparison = ImageComparison(
          params['baseline'],
          params['comparee'],
          max_rms_error=params['max_rms_error']
        )

        self.assertEqual(comparison.run(), params['is_similar'])

      return test

    for params in TEST_CASES:
      dict_[params['test_name']] = generate_test(params)

    return super(ImageComparisonMeta, metaclass).__new__(metaclass, name, bases, dict_)


class ImageComparisonTest(unittest.TestCase):
  __metaclass__ = ImageComparisonMeta

  def test_there_should_be_no_reason_if_the_images_are_similar(self):
    comparison = ImageComparison(
      _get_file_from_test_dir("converter_test_001.png"),
      _get_file_from_test_dir("converter_test_001.png"),
      max_rms_error=0)

    self.assertTrue(comparison.run())
    self.assertEqual(comparison.get_reason(), [])

  def test_there_should_be_a_reason_if_the_images_are_different(self):
    comparison = ImageComparison(
      _get_file_from_test_dir("converter_test_001.png"),
      _get_file_from_test_dir("converter_test_002.png"),
      max_rms_error=0)

    self.assertFalse(comparison.run())
    self.assertTrue(comparison.get_reason())


class DiffTest(unittest.TestCase):
  def test_it_should_render_a_diff_of_the_two_images(self):
    diff = ImageDiff(
      _get_file_from_test_dir("comparison_very_different_2_001.png"),
      _get_file_from_test_dir("comparison_very_different_001.png"),
      TEST_DATA_DIR
    )

    path_to_diff = diff.create()

    comparison = ImageComparison(
      path_to_diff,
      _get_file_from_test_dir("diff_test_different.png"),
      max_rms_error=0
    )

    self.assertTrue(comparison.run())

  def test_the_diff_should_be_blank_if_the_images_are_the_same(self):
    diff = ImageDiff(
      _get_file_from_test_dir("converter_test_001.png"),
      _get_file_from_test_dir("converter_test_001.png"),
      TEST_DATA_DIR
    )

    path_to_diff = diff.create()

    comparison = ImageComparison(
      path_to_diff,
      _get_file_from_test_dir("diff_test_same.png"),
      max_rms_error=0
    )

    self.assertTrue(comparison.run())


class ComparerTest(unittest.TestCase):
  def test_it_should_return_true_if_the_reports_are_similar(self):
    comparer = PdfComparer(
      _get_file_from_test_dir("similar_report_baseline.pdf"),
      _get_file_from_test_dir("similar_report_comparee.pdf"),
      max_rms_error=10
    )

    result, reasons = comparer.compare()
    self.assertTrue(result)

  def test_it_should_return_false_if_the_reports_are_different(self):
    comparer = PdfComparer(
      _get_file_from_test_dir("different_report_baseline.pdf"),
      _get_file_from_test_dir("different_report_comparee.pdf"),
      max_rms_error=10
    )

    result, reasons = comparer.compare()
    self.assertFalse(result)


if __name__ == "__main__":
  unittest.main()
