#!/usr/bin/env python

"""
Generates chromosome strurcture for SLiM simulation

"""

#package imports
import io
import random
import pandas as pd
import numpy as np
from loguru import logger

#internal imports
from shadie.mutations import MutationList
from shadie.elements import ElementList
from shadie.elements import ElementType

#default element types
from shadie.globals import NONCOD
from shadie.globals import INTRON
from shadie.globals import EXON

#default mutation types
from shadie.globals import NEUT
from shadie.globals import SYN
from shadie.globals import DEL
from shadie.globals import BEN


class Build:
    """
    Chromosome object created based on user parameters
    """

    def __init__(
    	self,
    	chromtype = "random",  #"random" or "dict" 
        genecount = None,
		exons = None,          #list of ElementTypes eligible for exon regions
        introns = None,        #list of ElementTypes eligible for intron regions
        noncoding = None,      #list of ElementTypes eligible for non-coding regions
		elementlist = None,    #read in ElementList object
		genome_size=1e6,       #will be used to calculate chromosome end (length -1)     
        ):
    
        self.type = chromtype
        self.exoncount = genecount
        self.exons = exons
        self.introns = introns
        self.noncoding = noncoding
        self.elements = elementlist
        self.gensize = genome_size

        """
        Builds the chromosome for SLiM3 simulation

        Parameters:
        -----------
        chromtype(str): default = "random"
            "random" will generate a random chromosome
            "dict" will accept a dictionary object

        exoncount(int): default = None
            Will produce a random chromosome using defaults with specified number 
            of genes (composed of exons only)

        genes(int): default = None
            Number of genes on chromosome
            Can be supplied as `int` for random chromosome generation
            or as dict object for explicit chromosome generation, e.g:

            dict(name = "name", mutations = (fitness effect,  dominance), start = bp, end = bp)
            dict(name = "a", mutations = (-.01, 0.5), start = 2000, end = 3000)

            # call simulate with details on genome structure (and which life stage selection occurs?)
            mod.simulate(
            dict(name='a', selection=-0.01, start=2000, end=3000, haploid=True),
            dict(name='b', selection=-0.02, start=5000, end=6000, haploid=True),
            dict(name='c', selection=-0.03, start=9000, end=10000, haploid=True),
            dict(name='A', selection=0.01, start=2000, end=3000, haploid=False),
            dict(name='B', selection=0.02, start=5000, end=6000, haploid=False),
            dict(name='C', selection=0.03, start=9000, end=10000, haploid=False),
            )

        exons (ElementList): default = None
           list of genomic elements that may be used as exons

        introns (ElementList): default = None
           list of genomic elements that may be used as introns

        noncoding (ElementList): default = None
           list of genomic elements that may be used as non-coding regions

        mutation_rate(int): default = 1e-7
            Chance of mutation at each nucleotide

        genome_size(int): default = =1e6
            Length of chromosome in nucleootides
        """

        if self.type == "custom":
            if isinstance(args, io.TextIOBase):
                self.genedf = pd.read_csv(args)

            elif isinstance(args, pd.DataFrame):
                self.genedf = args

            else:
                genelist = []
                for i in args:
                    if isinstance(i, dict):
                        genelist.append(i)
                self.genedf = pd.DataFrame(genelist)

        elif self.type == "random":
            pass
        

    def dict(self, genedf):
        "generates chromosome based on explicit user structure"
        for gene in self.genedf:
            #make the mutation types
            mutdict = {}
            #...
            self.mutdict = mutdict #my linter is telling me these should be defined in init

            #make the genomic element types
            elemdict = {}
            #...
            self.selemdict = elemdict

            #write the initializeGenomicElement lines to a dict
            initdict = {}
            #...
            self.initdict = initdict


    def genes(self):
        "generates a chromosome with specified number of exons"

        if self.exons is None:
            if self.exoncount is not None:
                maxexon = int(self.gensize/(self.exoncount*1.25))
                minexon = int(self.gensize)/(self.exoncount*3) 
                ncmin = int((self.gensize - (self.exoncount*maxexon))/(self.exoncount + 1))
                ncmax = int((self.gensize - (self.exoncount*minexon))/(self.exoncount + 1))

                genelements = pd.DataFrame(
                    columns=['type', 'name', 'start', 'finish', 'eltype', 'script'],
                    data=None,)
                
                while True:
                    exons = 0
                    base = int(0)

                    #make initial non-coding region
                    nc_length = np.random.randint(ncmin, ncmax)
                    genelements.loc[base, 'type'] = "noncoding"
                    genelements.loc[base, 'eltype'] = NONCOD.name
                    genelements.loc[base, 'script'] = NONCOD
                    genelements.loc[base, 'start'] = base
                    genelements.loc[base, 'finish'] = base + nc_length - 1
                    base = base + nc_length
                
                    #make first exon
                    ex_length = np.random.randint(minexon, maxexon) + 1
                    genelements.loc[base, 'type'] = "exon"
                    genelements.loc[base, 'eltype'] = EXON.name
                    genelements.loc[base, 'script'] = EXON
                    genelements.loc[base, 'start'] = base
                    genelements.loc[base, 'finish'] = base + ex_length -1
                    base = base + ex_length
                    exons += 1

                    while exons < self.exoncount:
                        nc_length = np.random.randint(ncmin, ncmax)
                        genelements.loc[base, 'type'] = "noncoding"
                        genelements.loc[base, 'eltype'] = NONCOD.name
                        genelements.loc[base, 'script'] = NONCOD
                        genelements.loc[base, 'start'] = base
                        genelements.loc[base, 'finish'] = base + nc_length - 1
                        base = base + nc_length
                    
                        #make first exon
                        ex_length = np.random.randint(minexon, maxexon) + 1
                        genelements.loc[base, 'type'] = "exon"
                        genelements.loc[base, 'eltype'] = EXON.name
                        genelements.loc[base, 'script'] = EXON
                        genelements.loc[base, 'start'] = base
                        genelements.loc[base, 'finish'] = base + ex_length -1
                        base = base + ex_length
                        exons += 1

                    #final non-coding region
                    genelements.loc[base, 'type'] = "noncoding"
                    genelements.loc[base, 'eltype'] = NONCOD.name
                    genelements.loc[base, 'script'] = NONCOD
                    genelements.loc[base, 'start'] = base
                    genelements.loc[base, 'finish'] = self.gensize - 1

                    if base > (self.gensize-1):
                        logger.info("trying again")
                        exons = 0
                        base = int(0)
                        continue
                    else:
                        break
                
                logger.debug(genelements)
                self.genelements = genelements
                self.mutationlist = MutationList(NEUT, SYN, DEL, BEN)
                self.elementlist = ElementList(self.mutationlist, EXON, NONCOD)



    def random(self):
        "generates a random chromosome"

        if self.type == "random":
            if self.exons is None:
                genelements = pd.DataFrame(
                columns=['type', 'name', 'start', 'finish', 'eltype', 'script'],
                data=None,
                )
                finalnc_length = np.random.randint(3000, 5000)
                end = self.gensize - finalnc_length
                logger.debug("Made objects: base = {base}, genelements = {}, end = {end}")

                while True:
                    base = int(0)
                    while base < end:
                        #make initial non-coding region
                        nc_length = np.random.randint(100, 5000)
                        genelements.loc[base, 'type'] = "noncoding"
                        genelements.loc[base, 'eltype'] = NONCOD.name
                        genelements.loc[base, 'script'] = NONCOD
                        genelements.loc[base, 'start'] = base
                        genelements.loc[base, 'finish'] = base + nc_length - 1
                        base = base + nc_length
                    
                        #make first exon
                        ex_length = round(np.random.lognormal(np.log(250), np.log(1.3))) + 1
                        genelements.loc[base, 'type'] = "exon"
                        genelements.loc[base, 'eltype'] = EXON.name
                        genelements.loc[base, 'script'] = EXON
                        genelements.loc[base, 'start'] = base
                        genelements.loc[base, 'finish'] = base + ex_length -1
                        base = base + ex_length
                        logger.info("Gene added")    
                        
                        while np.random.random_sample() < 0.75:  #25% probability of stopping
                            in_length = round(np.random.normal(450, 100))
                            genelements.loc[base, 'type'] = "intron"
                            genelements.loc[base, 'eltype'] = INTRON.name
                            genelements.loc[base, 'script'] = INTRON
                            genelements.loc[base, 'start'] = base
                            genelements.loc[base, 'finish'] = base + in_length -1
                            base = base + in_length
                          
                            ex_length = round(np.random.lognormal(np.log(250), np.log(1.3))) + 1
                            genelements.loc[base, 'type'] = "exon"
                            genelements.loc[base, 'eltype'] = EXON.name
                            genelements.loc[base, 'script'] = EXON
                            genelements.loc[base, 'start'] = base
                            genelements.loc[base, 'finish'] = base + ex_length -1
                            base = base + ex_length 
                              
                    #final non-coding region
                    genelements.loc[base, 'type'] = "noncoding"
                    genelements.loc[base, 'eltype'] = NONCOD.name
                    genelements.loc[base, 'script'] = NONCOD
                    genelements.loc[base, 'start'] = base
                    genelements.loc[base, 'finish'] = self.gensize - 1

                    logger.debug(genelements)
                    self.genelements = genelements
                    self.mutationlist = MutationList(NEUT, SYN, DEL, BEN)
                    self.elementlist = ElementList(self.mutationlist, EXON, INTRON, NONCOD)

                    if base > (self.gensize-1):
                        logger.info("trying again")
                        base = int(0)
                        continue
                    else:
                        break
       
            elif self.exons is not None: 
                #check the types
                for i in self.exons:
                    if isinstance(i, ElementType):
                        pass
                    else:
                        raise TypeError("exons must be ElementType class objects")

                for i in self.introns:
                    if isinstance(i, ElementType):
                        pass
                    else:
                        raise TypeError("introns must be ElementType class objects")

                #check the types
                for i in self.noncoding:
                    if isinstance(i, ElementType):
                        pass
                    else:
                        raise TypeError("noncoding must be ElementType class objects")

                genelements = pd.DataFrame(
                columns=['name', 'start', 'finish', 'eltype', 'script'],
                data=None,
                )
                finalnc_length = np.random.randint(self.gensize/300, self.gensize/200)
                end = self.gensize - finalnc_length
                logger.debug("Made objects: base = {base}, genelements = {}, end = {end}")

                while True:
                    base = int(0)
                    while base < end:
                        #make initial non-coding region
                        nc_length = np.random.randint(100, 5000)
                        choose = random.choice(self.noncoding)

                        genelements.loc[base, 'type'] = "noncoding"
                        genelements.loc[base, 'name'] = choose.altname
                        genelements.loc[base, 'eltype'] = choose.name
                        genelements.loc[base, 'script'] = self.elements.elementdict[choose.name]
                        genelements.loc[base, 'start'] = base
                        genelements.loc[base, 'finish'] = base + nc_length - 1
                        base = base + nc_length

                        #make first exon
                        ex_length = round(np.random.lognormal(np.log(250), np.log(1.3))) + 1
                        choose = random.choice(self.exons)

                        genelements.loc[base, 'type'] = "exon"
                        genelements.loc[base, 'name'] = choose.altname
                        genelements.loc[base, 'eltype'] = choose.name
                        genelements.loc[base, 'script'] = self.elements.elementdict[choose.name]
                        genelements.loc[base, 'start'] = base
                        genelements.loc[base, 'finish'] = base + ex_length -1
                        base = base + ex_length
                        logger.info("Gene added")    

                        while np.random.random_sample() < 0.75:  #25% probability of stopping
                            in_length = round(np.random.normal(450, 100))
                            choose = random.choice(self.introns)
                            genelements.loc[base, 'type'] = "intron"
                            genelements.loc[base, 'name'] = choose.altname
                            genelements.loc[base, 'eltype'] = choose.name
                            genelements.loc[base, 'script'] = self.elements.elementdict[choose.name]
                            genelements.loc[base, 'start'] = base
                            genelements.loc[base, 'finish'] = base + in_length -1
                            base = base + in_length

                            ex_length = round(np.random.lognormal(np.log(250), np.log(1.3))) + 1
                            choose = random.choice(self.exons)

                            genelements.loc[base, 'type'] = "exon"
                            genelements.loc[base, 'name'] = choose.altname
                            genelements.loc[base, 'eltype'] = choose.name
                            genelements.loc[base, 'script'] = self.elements.elementdict[choose.name]
                            genelements.loc[base, 'start'] = base
                            genelements.loc[base, 'finish'] = base + ex_length -1
                            base = base + ex_length 

                    #final non-coding region
                    choose = random.choice(self.noncoding)

                    genelements.loc[base, 'type'] = "noncoding"
                    genelements.loc[base, 'name'] = choose.altname
                    genelements.loc[base, 'eltype'] = choose.name
                    genelements.loc[base, 'script'] = self.elements.elementdict[choose.name]
                    genelements.loc[base, 'start'] = base
                    genelements.loc[base, 'finish'] = self.gensize - 1
                    logger.info(f"Base: {base}, End: {self.gensize-1}")

                    if base > (self.gensize-1):
                        logger.info("trying again")
                        base = int(0)
                        continue
                    else:
                        break

                logger.debug(genelements)
                self.genelements = genelements
                self.mutationlist = self.elements.mutationlist
                self.elementlist = self.elements

        else:
            print("'type' must be 'random' or 'dict'")


if __name__ == "__main__":

    #test custom builder:
    from shadie.mutations import MutationType

    mut1 = MutationType(0.5, "f", .03)
    mut2 = MutationType(0.5, "e", 0.4)
    mutlist = MutationList(mut1, mut2)
    eltype1 = ElementType(mut1, 1)
    eltype2 = ElementType(mut2, 1)
    mylist = ElementList(mutlist, eltype1, eltype2)

    custom = Build(exons = [eltype1, eltype2], introns = [eltype1, eltype2], 
        noncoding = [eltype1, eltype2], elementlist = mylist)

    # generate random chromosome
    init_chromosome =  Build()
    Build.random(custom)

    #chromosome with specified number of genes
    fourgenes = Build(genecount = 4)
    fourgenes.genes()
