# G channel instead of Y

It has been reported that someone is running VQMs (e.g., VMAF) by passing RGB videos instead of YUV.
The file `run_experiments_ITS4S_gbrp.sh` explores this case for the ITS4S dataset.
Just overwrite `run_experiments.sh`, rebuild the container, and look at the results.

The trick is converting the content to the gbrp pix_fmt of ffmpeg, then passing it as 444 raw-encoded content to libVMAF, which will use the first channel (G in this case) as if it were Y.

