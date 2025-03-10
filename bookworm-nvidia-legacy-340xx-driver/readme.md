# Legacy nvidia drivers for Debian bookworm

## Why?

My mac mini have too old device..

````
Mar 09 23:38:36 mmini kernel: NVRM: The NVIDIA GeForce 320M GPU installed in this system is
                              NVRM:  supported through the NVIDIA 340.xx Legacy drivers. Please
                              NVRM:  visit http://www.nvidia.com/object/unix.html for more
                              NVRM:  information.  The 535.216.01 NVIDIA driver will ignore
                              NVRM:  this GPU.  Continuing probe...
````

# Building and running
````
pashi@srv1:~/src/nvidia-legacy$ podman build -t nvidia-legacy-bookworm .
pashi@srv1:~/src/nvidia-legacy$ podman images|grep nvidia
localhost/nvidia-legacy-bookworm  latest                 dcd84a2c0472  48 seconds ago      94.4 MB
pashi@srv1:~/src/nvidia-legacy$ podman run -d --rm --name nvidia -p 20080:80 nvidia-legacy-bookworm 
24d92d6d960121e8c48f6e3b74e8e0c8b047336c2efdc71f142ecd96aab3742e
````


# Use source

````
root@mmini:~# echo 'deb [trusted=yes] http://192.168.1.6:20080/ bookworm non-free' > /etc/apt/sources.list.d/nvidia.list
root@mmini:~# apt install nvidia-legacy-340xx-driver nvidia-settings-legacy-340xx
````

## References
* https://www.pashi.net/post/2025-03-10-mac-mini/
* https://gist.github.com/Anakiev2/b828ed2972c04359d52a44e9e5cf2c63
