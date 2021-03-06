=============================================================
``django-nailbiter`` - a storage-agnostic thumbnail generator
=============================================================

``nailbiter`` is a simple thumbnail generation field for Django,
modeled after ``sorl-thumbnail``. 


Usage
=====

First, define a model using a ``nailbiter`` thumbnail field:

In ``models.py``::

	from django.contrib.auth.models import User
	from django.db import models
	from nailbiter.fields import ImageWithThumbsField

	class Gallery(models.Model):
	    name = models.CharField(max_length=150)
		
	class Photo(models.Model):
	    uploader = models.ForeignKey(User, related_name="photos")
	    gallery = models.ForeignKey(Gallery, related_name="photos")
	    title = models.CharField(max_length=150)
	    image_file = ImageWithThumbsField(
	        upload_to = photo_upload_path,
	        generate_on_save = True,
	        thumbnail = {'size': (150, 150), 'options': ['detail']},
	        quality: 90,
	        extra_thumbnails = {
	            'headline': {'size': (300, 300), 'options': ['upscale', 'detail'], 'quality':95},
	            'avatar': {'size': (64, 64), 'options': ['crop', 'upscale', 'detail']},
	            'gallery_icon': {'size': (150, 150), 'options': ['crop', 'upscale', 'detail'], 'quality':75},
	        })
	    created_date = models.DateTimeField(default=datetime.utcnow)

To display the thumbnail in a template: ::

	<img src="{{ object.image_file.thumbnail.url }}" />
	
To display a thumbnail defined in ``extra_thumbnails``, just refer to it
by the name you defined: ::

	<img src="{{ object.image_file.extra_thumbnails.headline.url }}" />

Quality
-------

Modifying the quality of generated thumbnails has been also added (see
the example above). This can be done on a field scope (high-level) or
thumbnail-size scope (detailed-level).  Both are optional; if neither
is defined, then the default PIL save quality (75) will be used. Quality
defined for a thumbnail size will override field-level quality.

Cleanup
-------

If you want to make sure that previously uploaded files are removed when
you re-upload, handle the pre_save signal for your model.  For example: ::

	# remove previous photo files and thumbnails!
	def cleanup_photo(sender, **kwargs):
	    instance = kwargs["instance"]
	    try:
	        original = Photo.image_file.get(id=instance.id)
	        if original.photo:
	            original.image_file.delete(False)
	    except:
	        pass
	
	pre_save.connect(cleanup_photo, sender=Photo)
