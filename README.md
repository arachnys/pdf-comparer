### PDF-COMPARER

PDF-COMPARER is a python utility to compare pdfs, based on ghostscript and pillow.

### INSTALLATION

This package depends on ghostscript, so this must be installed on your system before you can use PDF-COMPARER.

Once this is done, installing the package is as easy as: `pip install .`

### USAGE

PDF-COMPARER can be run from the command line:

```
./compare-pdf <path_to_pdf> <path_to_another_pdf> --rms-threshold=<threshold> --diffs-destination=<destination_folder>
```

The following options are supported:

- `--rms-threshold`: How sensitive the comparison tool should be to mark a pair of pages as being dissimilar. The default value is 10.
- `--diffs-destination`: The path of the folder where diffs should be saved. The default value is `None` (i.e. the diffs won't be saved.)

PDF-COMPARER can also be used programatically:


    from comparer import PdfComparer

    comparer = PdfComparer(
      <path_to_pdf>,
      <path_to_another_pdf>,
      max_rms_error=<threshold>,
      diff_images_destination=<destination_folder>
    )

    is_similar, reasons = comparer.compare()


### RUNNING THE TESTS

```
docker build -t pdf-comparer .
docker run pdf-comparer
```