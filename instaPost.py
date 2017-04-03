import os, os.path, time, configuration, shutil, sys, numpy
from PIL import Image, ImageDraw, ImageFont
from instaLooter import InstaLooter
from wordpress_xmlrpc import *
from wordpress_xmlrpc.methods import media, posts
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost

image_as_text=False

if len(sys.argv)==2:
    if (sys.argv[1]=='-t') or (sys.argv[1]=='-T'):
        image_as_text=True

#For SSH users, you can print the image to review in ASCII form
#For testing purposes only
def print_ascii(image):
    chars = numpy.asarray(list(' .,:;irsXA253hMHGS#9B&@'))
    escala, luminosidad = (1/10), 2
    S = (round(image.size[0]*escala*(7.0/4.0)),round(image.size[1]*escala))
    image = numpy.sum(numpy.asarray(image.resize(S)),axis=2)
    image -= image.min()
    image = (1.0-image/image.max())**luminosidad*(chars.size-1)
    os.system('clear')
    print( "\n".join( ("".join(r) for r in chars[image.astype(int)]) ) )

def watermark(image_file,text):
    image = Image.open(image_file).convert('RGBA')
    width, height = image.size
    draw = ImageDraw.Draw(image)
    rect = Image.new('RGBA', image.size, (255,255,255,0))
    fontsize = 1
    fraction = 0.33
    font = ImageFont.truetype(configuration.font, fontsize)
    while font.getsize(text)[0] < fraction*image.size[0]:
        # Iterate until the text size is just larger than the criteria
        fontsize += 1
        font = ImageFont.truetype(configuration.font, fontsize)
    fontsize -= 1
    font = ImageFont.truetype(configuration.font, fontsize)
    textwidth, textheight = draw.textsize(text, font)
    margin = 10
    x = width - textwidth - margin
    y = height - textheight - margin
    draw = ImageDraw.Draw(rect)
    draw.rectangle(((x, y),(x+textwidth,y+textheight)), fill=(0, 0, 0, 100))
    draw.text((x, y), text, font=font)
    out = Image.alpha_composite(image, rect)
    out.save(image_file)

handle = input('Enter a valid Instagram handle (no @): ')

while True:
    try:
        quantity = int(input('Enter the number of pictures to download: '))
    except ValueError:
        print('It has to be a number.')
        continue
    else:
        break

print('Looting pictures...')
looter = InstaLooter(profile=handle,directory=configuration.temp_path)
looter.download_pictures(media_count=quantity)

os.system('clear')
#Iterates and watermarks every downloaded picture

watermark_text='Your own text'

print('Watermarking...')
for filename in os.listdir(configuration.temp_path):
    if filename.endswith('jpg'):
        watermark(configuration.temp_path+filename,watermark_text)
os.system('clear')

size = 800, 600
comments={}

for filename in os.listdir(configuration.temp_path):
    os.system('clear')
    if filename.endswith('jpg'):
        image = Image.open(configuration.temp_path+filename)
        image.thumbnail(size, Image.ANTIALIAS)
        if image_as_text:
            print_ascii(image)
        else:
            image.show()
        ans = input("d/D to DELETE - c/C to COMMENT under the picture:")
        if (ans=='d') or (ans=='D'):
            os.remove(configuration.temp_path+filename)
        elif (ans=='c') or (ans=='C'):
            comments[filename]=input('Comment: ')

title = input('Enter a Title for your post: ')

while True:
    os.system('clear')
    print('The title is:')
    print('"'+title+'"')
    ans = input('Want to change it? c/C:\n')
    if (ans=='c') or (ans=='C'):
        title=input('Enter a Title for your post: ')
        continue
    else:
        break

responses=[]

wp = Client(configuration.xmlrpc_path, configuration.user, configuration.password)

#There probably is a better way to do this!
quantity=0
actual=1

for filename in os.listdir(configuration.temp_path):
    if filename.endswith('jpg'):
        quantity+=1

for filename in os.listdir(configuration.temp_path):
    if filename.endswith('jpg'):
        os.system('clear')
        print('Uploading file '+str(actual)+'/'+str(quantity))
        actual+=1
        data = {
                'name': filename,
                'type': 'image/jpeg',  # mimetype
        }
        print('Filename: '+filename)
        with open(configuration.temp_path+filename, 'rb') as img:
            data['bits'] = xmlrpc_client.Binary(img.read())
            responses.append(wp.call(media.UploadFile(data)))

text=''
alt=''

for response in responses:
    text+="<img src=\""+response['url']+"\"alt=\""+alt+"\" /> "+' '
    if response['title'] in comments:
        text+= "<strong>" + comments[response['title']]

text+="<br> <br><a href=\"https://instagram.com/"+handle+"\">Follow @"+handle+" on Instagram.</a> <br>"
post = WordPressPost()
post.id = wp.call(NewPost(post))
post.title=title
post.terms_names = {'post_tag': ['your','tags'],'category': ['your category']}#Change this
post.content = text
post.comment_status='open'
post.excerpt=''#Change this
post.post_type = 'post'
post.post_status = 'publish'#Posts automatically, careful!
post.thumbnail=responses[0]['id']
#You can also add custom fields, for Yoast SEO, etc.
#post.custom_fields=[]
#post.custom_fields.append ({
#    'key': '_yoast_wpseo_focuskw',
#    'value': handle + ' pictures'
#})
#post.custom_fields.append ({
#    'key': '_yoast_wpseo_focuskeywords',
#    'value': '[{"keyword":"'+ handle + ' instagram", "score":"good"}, {"keyword":"'+ handle + ' something", "score":"good"}]'
#})

wp.call(posts.EditPost(post.id, post))
print('Post ready!')
shutil.rmtree(configuration.temp_path)
