# InstaPost
Loots an arbitrary quantity of pictures from an Instagram handle and posts it to a Wordpress blog.
You can preview and comment every image.

## Dependencies
-instaLooter: https://github.com/althonos/InstaLooter for downloading Images  
-PIL (or pillow): for Image manipulation  
-wordpress_xmlrpc: https://python-wordpress-xmlrpc.readthedocs.io for Wordpress posting  
-numpy: for Ascii conversion  
(All available in PIP -do NOT install as root-)

## Usage:
```
python instaPost  
```

or

```
python instaPost -t  
```
(This enables a text based image preview, for SSH users and such)
