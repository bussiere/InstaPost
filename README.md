# InstaPost
Loots an arbitrary quantity of pictures from an Instagram handle and posts it to a Wordpress blog.
You can preview and comment every image.

## Dependencies
-Python 3  
-instaLooter: https://github.com/althonos/InstaLooter for downloading Images  
-PIL (or pillow): for Image manipulation  
-wordpress_xmlrpc: https://python-wordpress-xmlrpc.readthedocs.io for Wordpress posting  
-numpy: for Ascii conversion  
(All available in PIP3 -do NOT install as root-)

## Usage:
```
python3 instaPost  
```

or

```
python3 instaPost -t  
```
(This enables a text based image preview, for SSH users and such)
