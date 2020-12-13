# parsl-funcx
This repository contains the notebooks that were created as we wrote the blog in https://cloud4scieng.org and https://esciencegroup.com 
There is a Jupyter notebook and a copy rendered as html for each of the four experiments.

The notebook that compares parsl to dask on a single multicore VM is parsl-dask-on-azure-vm.ipynb

The notebook funcx-classify-and-check.ipynb demonstrates the BERT classifier as a funcx function.  this version uses passes the complete text of the arxiv abstract to the classifier and it does the entire test set (in 4 large batches).  The accuracy of the classifier is computed.

funcx-on-azure-k8s.ipynb is the set of experiments that measure the performance of the BERT classifier running on a small 5 node kubernetes cluster.

funcx-jetson.ipynb demonstrates running a funcx end point on a little jetson edge computing device.  
