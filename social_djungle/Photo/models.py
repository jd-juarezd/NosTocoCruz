from django.db import models
from imagekit.models import ImageModel

from django.db import models
from imagekit.specs import ImageSpec

class Photos(ImageModel):
     image = models.ImageField(upload_to = 'photos')
     author = models.ForeignKey(Users)

class IKOptions:
         spec_module = 'Photo.specs'
         cache_dir = 'photos/cache'
         image_field = 'image'
         
def thumb (self):
         if self.image:
             return '<img src=" %s ">'% self.thumbnail.url
         else:
             return ""
thumb.allow_tags = True
thumb.short_description = 'Foto'

from imagekit.specs import ImageSpec
from imagekit import processors

 # Define the thumnail procesador
class ResizeThumb (processors.Resize):
     width = 100
     height = 75
     crop = True

class ResizeDisplay (processors.Resize):
     width = 600

class ResizeBig (processors.Resize):
     width = 800

 # Define your spec
class Thumbnail (ImageSpec):
     pre_cache = True
     processors = [ResizeThumb,]

class Display (ImageSpec):
     processors = [ResizeDisplay,]

class Big (ImageSpec):
     processors = [ResizeBig,]
     
     
from django import forms
from PIL import Image

class AttachmentForm (forms. Form):
     """Form for the attachment sample. Added a simple validation
 to accept only png filas checking for 'image / jpeg' in the
 content_type of the file """
     image = forms.FileField (help_text = "add a png or jpg file")

     def clean (self):
         "Validate the entire form"
         cleaned = self.cleaned_data        
         try:
             file = cleaned ['image']
         except Exception, e:
             # Perhaps this is not a file
             raise forms.ValidationError ("Not valid file:% s"% e)
         if not file.content_type. lower () in ["image / jpeg", "image / jpeg", "image / jpg"]:            
             raise forms.ValidationError ("Just jpg oro png filas please")
         im = Image.open (file)
         if not im.formato in ['JPEG', 'PNG']:
             raise forms.ValidationError ("Just jpg oro png filas please")
         return cleaned