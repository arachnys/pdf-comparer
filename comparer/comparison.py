import itertools
import math
from PIL import Image, ImageChops


def build_comparer(baseline_paths, comparee_paths, max_rms_error):
  length_comparison = LengthComparison(baseline_paths, comparee_paths)

  image_pairs = itertools.izip(baseline_paths, comparee_paths)
  image_comparisons = [
      ImageComparison(baseline_path, comparee_path, max_rms_error)
      for baseline_path, comparee_path in image_pairs
  ]

  return ComparisonRunner([length_comparison] + image_comparisons)


class Comparison(object):
  def __init__(self):
    self.reason = []
    self.comparison_has_run = False

  def get_reason(self):
    if not self.comparison_has_run:
      raise ValueError('Must run comparison first.')

    return self.reason


class LengthComparison(Comparison):
  def __init__(self, baseline_paths, comparee_paths):
    super(LengthComparison, self).__init__()

    self.baseline_paths = baseline_paths
    self.comparee_paths = comparee_paths

  def run(self):
    self.comparison_has_run = True
    are_lengths_equal = len(self.baseline_paths) == len(self.comparee_paths)

    if not are_lengths_equal:
      self.reason.append('LENGTH_NOT_EQUAL')

    return are_lengths_equal


class ImageComparison(Comparison):
  def __init__(self, baseline, comparee, max_rms_error):
    super(ImageComparison, self).__init__()

    self.baseline = baseline
    self.comparee = comparee

    self.max_rms_error = max_rms_error

  def _squares_for_channel(self, channel_values):
    return [frequency * (colour_value**2) for colour_value, frequency in enumerate(channel_values)]

  def _calculate_rms(self):
    baseline_img = Image.open(self.baseline)
    comparee_img = Image.open(self.comparee)

    diff = ImageChops.difference(baseline_img, comparee_img)

    histogram = diff.histogram()

    red_channel_squares = self._squares_for_channel(histogram[:256])
    green_channel_squares = self._squares_for_channel(histogram[256:512])
    blue_channel_squares = self._squares_for_channel(histogram[512:768])
    alpha_channel_squares = self._squares_for_channel(histogram[768:])

    sum_of_squares = sum(
        red_channel_squares + green_channel_squares + blue_channel_squares + alpha_channel_squares
    )

    baseline_x, baseline_y = baseline_img.size
    root_mean_square_error = math.sqrt(sum_of_squares / float(baseline_x * baseline_y))

    return root_mean_square_error

  def run(self):
    self.comparison_has_run = True
    rms_error = self._calculate_rms()

    if rms_error > self.max_rms_error:
      self.reason.append('RMSE_EXCEEDED')
      return False
    return True


class ComparisonRunner(object):
  def __init__(self, comparisons):
    self.comparisons = comparisons

  def run(self):
    result = all([comparison.run() for comparison in self.comparisons])

    reasons = reduce(
        lambda reason, agg: agg + reason,
        [comparison.get_reason() for comparison in self.comparisons]
    )

    return result, reasons
