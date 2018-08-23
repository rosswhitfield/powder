# [POWDER](https://neutrons.ornl.gov/powder) (HB-2A) data reduction

* `load_and_plot.py` will load the data and plot per anode and then all the data combined but not rebinned
* `reduce_old.py` reproduces the data reduction as done by [Graffiti](http://neutron.ornl.gov/spice/User_Downloads.html) (run with `./reduce_old.py datafile output_directory`)
* `read_metadata.py` is an example of loading in all the metadata from a file
* `reduce.py` is the new data reduction in just python, rebinning the data
* `reduce_to_mantid.py` is the data reduction outputing to mantid workspaces
