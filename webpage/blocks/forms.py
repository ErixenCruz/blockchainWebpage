from django.forms import modelform_factory
from .models import Block

blockForm = modelform_factory(Block,fields =('delta',))
