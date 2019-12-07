# influenced by https://github.com/heronyang/pychain/blob/master/chain.py
from django.db import models
from .block import block
from datetime import datetime as dt
import hashlib
import time
import multiprocessing

class Block(models.Model):
    @property
    def blockHash(self):
        ''' Calculate and return the hash of the block'''
        return hashlib.sha256((
                self.prevHash+
                str(self.delta)+
                str(self.time)+
                str(self.nonce)).encode()).hexdigest()

    @property
    def isMined(self):
        '''Check to see if first digits are zeros.'''
        return self.blockHash[:5]=='0'*5 

    @property 
    def isGood(self):
        '''Both previous hash and current one are solved.'''
        return self.isMined and self.prevHash[:5]=='0'*5

    '''
    @classmethod
    @property
    def instantiationTime(self):
        return dt.now()
    '''

    def mineSeq(self):
        '''Sequentially find the nonce that solves the block.'''
        self.nonce=0
        start=time.time()
        while not self.isMined:
            self.nonce+=1
        stop=time.time()
        self.solTime=stop-start
        self.save()

    def hashWithNonce(self,nonce):
        return hashlib.sha256((
                self.prevHash+
                str(self.delta)+
                str(self.time)+
                str(nonce)).encode()).hexdigest()

    def hashWithNonceIsMined(self,nonce):
        return self.hashWithNonce(nonce)[:5]=='0'*5

    def minePara(self,poolSize=4):
        '''Find the nonce that solves the block using multiple threads.'''
        timeStart=time.time()
        sharedNonce = multiprocessing.Value('i',lock=False)
        sharedNonce.value = -1
        def mineSeqWithStep(start,poolSize,sharedNonce):
            nonce=start
            while sharedNonce.value==-1:
                if self.hashWithNonceIsMined(nonce):
                    sharedNonce.value=nonce
                    break
                else:
                    nonce+=poolSize

        procs=[]
        for i in range(poolSize):
            proc=multiprocessing.Process(target=mineSeqWithStep,\
                    args=(i,poolSize,sharedNonce))
            procs.append(proc)
            proc.start()
        for proc in procs:
            proc.join()
        self.nonce=sharedNonce.value
        end=time.time()
        self.solTime=end-timeStart
        self.save()

    prevHash = models.CharField(max_length=200,default='0'*5)
    delta = models.IntegerField(default=0)
    time = models.DateTimeField('creation date')
    nonce = models.IntegerField(default = 0)
    solTime = models.DecimalField(max_digits=5,decimal_places=3,default=0)
    prevHashMatches = models.BooleanField(default=False)
