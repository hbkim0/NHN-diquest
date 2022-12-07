# mlp-data-service

## NFS setting
- Install nfs-client package
```
$ sudo apt-get install nfs-common
```
- Mount NFS
```
$ sudo mkdir /style_profiling
$ sudo mount -t nfs 133.186.171.5:/data/style_profiling /style_profiling
```