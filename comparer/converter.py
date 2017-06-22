import subprocess

from utils import TempDir, Path


class PdfToPngConverter(object):
  def __init__(self, path):
    self.path = path
    self.temp_dir = TempDir()

  def _page_name_template(self):
    return u"{temp_dir}/{filename}_%03d.png".format(
        temp_dir=self.temp_dir.path, filename=Path.filename(self.path)
    )

  def _convert(self):
    args = ['gs', '-sDEVICE=pngalpha', '-o', self._page_name_template(), '-r300', self.path]

    subprocess.check_output(args)

  def convert(self):
    self._convert()
    converted_files = self.temp_dir.list()
    return converted_files

  def __enter__(self):
    return self.convert()

  def __exit__(self, type, value, traceback):
    return self.temp_dir.remove()
