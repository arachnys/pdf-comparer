import tempfile
import os
import shutil


class TempDir(object):
  def __init__(self):
    self._path = tempfile.mkdtemp()

  @property
  def path(self):
    return self._path

  def list(self):
    filepaths = sorted(os.listdir(self._path))
    absolute_filepaths = [
      os.path.join(self._path, filepath) for filepath in filepaths
    ]
    return absolute_filepaths

  def remove(self):
    return shutil.rmtree(self._path)


class Path(object):
  @staticmethod
  def basename(path):
    return os.path.basename(path)

  @staticmethod
  def filename(path):
    filename, _ = os.path.splitext(os.path.basename(path))
    return filename
