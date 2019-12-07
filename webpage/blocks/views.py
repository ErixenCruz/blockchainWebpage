from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import Block
from .forms import blockForm
from datetime import datetime

def index(request):
    if request.GET.get('MineSeq'):
        Block.objects.get(id=int(request.GET.get('blockID'))).mineSeq()
    if request.GET.get('MinePara'):
        Block.objects.get(id=int(request.GET.get('blockID'))).minePara()
    if request.GET.get('EditBlock'):
        return editBlock(request)
    if request.GET.get('DeleteBlock'):
        Block.objects.get(id=int(request.GET.get('blockID'))).delete()
    if request.method == 'POST':
        b=Block(delta=request.POST['delta'])
        b.time=datetime.now()
        b.save()
    blockList = Block.objects.order_by('time')

    # Check if previous hashes match. This logic let's the template know
    #  whether to color green for good or red for bad.
    for i,block in enumerate(blockList):
        if i==0:
            block.prevHashMatches=True
        else:
            block.prevHash = blockList[i-1].blockHash
            block.prevHashMatches=True
        block.save()

    context = {'blockList': blockList}
    return render(request,'blocks/index.html',context)

def editBlock(request):
    if request.method == 'POST':
        form = blockForm(request.POST,instance=Block.objects.get(id=int(request.GET.get('blockID'))))
        form.save()
        return HttpResponseRedirect('/blocks/')
    form = blockForm(instance=Block.objects.get(id=int(request.GET.get('blockID'))))
    context = {'form': form}
    return render(request,'blocks/edit.html',context)
