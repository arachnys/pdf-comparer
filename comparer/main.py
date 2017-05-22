import itertools
from comparison import build_comparer
from diff import ImageDiff
from converter import PdfToPngConverter


class PdfComparer(object):
  def __init__(self,
               path_to_baseline,
               path_to_comparee,
               max_rms_error,
               diff_images_destination=None,
               ):
    self.path_to_baseline = path_to_baseline
    self.path_to_comparee = path_to_comparee

    self.max_rms_error = max_rms_error
    self.diff_images_destination = diff_images_destination

  def should_save_diffs(self):
    return self.diff_images_destination is not None

  def compare(self):
    baseline_converter = PdfToPngConverter(self.path_to_baseline)
    comparee_converter = PdfToPngConverter(self.path_to_comparee)

    with baseline_converter as baseline_paths, comparee_converter as comparee_paths:
      comparison_runner = build_comparer(baseline_paths, comparee_paths, self.max_rms_error)

      result, reasons = comparison_runner.run()

      if self.should_save_diffs():
        self.save_diffs(baseline_paths, comparee_paths)

      return (result, reasons)

  def save_diffs(self, baseline_paths, comparee_paths):
    def create_diff(pairs):
      diff = ImageDiff(*pairs, destination=self.diff_images_destination)
      diff.create()

    comparison_pairs = itertools.izip(baseline_paths, comparee_paths)
    map(create_diff, comparison_pairs)
