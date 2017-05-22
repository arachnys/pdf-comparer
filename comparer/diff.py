import os
from utils import Path
from PIL import Image, ImageDraw, ImageChops


class ImageDiff(object):
  def __init__(self, baseline, comparee, destination):
    self.baseline = baseline
    self.comparee = comparee

    self.destination = destination

  def path_to_diff(self):
    diff_name = Path.filename(self.baseline) + '_diff.png'
    return os.path.join(self.destination, diff_name)

  def make_transparent_overlay(self, image_size):
    # Create a fully transparent image the size of image_size
    transparent_overlay = Image.new('RGBA', image_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(transparent_overlay)
    # Draw an opaque red rectangle over the image
    draw.rectangle(((0, 0), image_size), fill=(255, 0, 0, 127))
    return transparent_overlay

  def make_diff(self, baseline_img, comparee_img):
    # Diffs need to be converted to RGB or they'll show up blank
    return ImageChops.difference(baseline_img, comparee_img).convert('RGB')

  def create(self):
    baseline_img = Image.open(self.baseline)
    comparee_img = Image.open(self.comparee)

    transparent_red_overlay = self.make_transparent_overlay(baseline_img.size)
    diffed_image = self.make_diff(baseline_img, comparee_img)

    multiplied_image = ImageChops.multiply(transparent_red_overlay, diffed_image.convert('RGBA'))
    overlay_diff = Image.alpha_composite(baseline_img, multiplied_image)

    path_to_diff = self.path_to_diff()
    overlay_diff.save(path_to_diff)

    return path_to_diff
