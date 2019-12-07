# block.py - Class for representing blocks with proof-of-work through hashing.
# Adapted from https://github.com/heronyang/pychain/blob/master/chain.py
#
# Python 3.6.8 on Ubuntu 18.04.2 LTS(tux.cs.drexel.edu)
#
# Erixen Cruz ec622@drexel.edu
import hashlib
from datetime import datetime
import multiprocessing
from itertools import repeat

class block():
    def __init__(self,prevHash='0',delta=0,difficulty=4):
        '''
        prevHash - Hash of the previous block in the chain.
        delta - change in the account value.
        '''
        self.prevHash = str(prevHash)
        self.delta = str(delta)
        self.time  = str(datetime.now())
        self.nonce=0
        self.difficulty=difficulty
        self.target='0'*self.difficulty
        super(block,self).__init__()

    @property
    def hash(self):
        ''' Calculate and return the hash of the block'''
        return hashlib.sha256((\
                self.prevHash+\
                self.delta+\
                self.time+\
                str(self.nonce)).encode()).hexdigest()

    @property
    def isMined(self):
        '''Check to see if first digits are zeros.'''
        return self.hash[:self.difficulty]==self.target

    def mineSeq(self):
        '''Sequentially find the nonce that solves the block.'''
        while not self.isMined:
            self.nonce +=1

    #### functions for supporting mining in parallel are below
    def hashWithNonce(self,nonce):
        '''
        Check what the hash would be with a particular nonce. Does not
            modify the nonce of the block.
        '''
        return hashlib.sha256((\
                self.prevHash+\
                self.delta+\
                self.time+\
                str(nonce)).encode()).hexdigest()

    def hashWithNonceIsMined(self,nonce):
        return self.hashWithNonce(nonce)[:self.difficulty]==self.target

    def minePara(self,poolSize=2):
        '''Find the nonce that solves the block using multiple threads.'''
        isNonceFound = multiprocessing.Event()
        sharedNonce=multiprocessing.Value('i',lock=False)
        sharedNonce.value=-1

        def mineSeqWithStep(start,poolSize,sharedNonce):
            nonce = start
            while sharedNonce.value==-1: # nonce not found yet
                if self.hashWithNonceIsMined(nonce):
                    print('Nonce found ({}) on process {}'.format(nonce,start))
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

        self.nonce = sharedNonce.value
