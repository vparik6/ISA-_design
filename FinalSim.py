from math import log, ceil
import random

def twoComplement(string):
    if(string[0] == '1'):
        imm = 65535 - int(string, 2)
        imm +=1
        imm = -imm
    else:
        imm = int(string, 2)
    return imm

class Statistics:
    def __init__(self, debugMode):
         self.I= ""               #current instruction being executed
         self.name = ""           # name of the instruction
         self.cycle = 0           # Total cycles in simulation
         self.slowCycle = 0       # Total cycles in slow pipeline 
         self.fastCycle = 0       # Total cycles in fast pipeline
         #self.isSlow = False      # Boolean to check if slow pipeline is currently being run
         #self.isFast = False      # Boolean to check if fast pipeline is currently being run
         self.DIC = 0             # Total Dynamic Instr Count
         self.threeCycles= 0      # How many instr that took 3 cycles to execute
         self.fourCycles = 0      #                          4 cycles
         self.fiveCycles = 0      #                          5 cycles
         self.DataHazardSlow = 0      #number of data hazards in slow pipeline
         self.ControlHazardSlow = 0   #number of control hazards in slow pipeline
         self.DataHazardFast = 0    #number of data hazards in fast pipeline
         self.ControlHazardFast = 0 #number of control hazards in fast pipeline
         #self.CompBranchHazard = False #Boolean value to check if data hazard is a CompBranch or not
         self.NOPcount = 0        #keeps track of NOP
         self.flushCount = 0      #keeps track of flush
         self.stallCount = 0      #keeps track of stall count
         self.debugMode = debugMode
         self.multiS = []
         self.slowS = []
         self.fastS = []
         for i in range(4):
             self.multiS.append(" ")
             self.slowS.append(" ")
             self.fastS.append(" ")
             
            
    def log(self,I,name,cycle,slowCycle,fastCycle,pc):
        self.I = I
        self.name = name
        self.pc = pc
        self.cycle +=  cycle
        self.slowCycle += slowCycle
        self.fastCycle += fastCycle
        # Instead of having 1 cycle variable, we might need 3. One each for multi-cycle, slow pipeline, and fast pipeline
        self.DIC += 1
        self.threeCycles += 1 if (cycle == 3) else 0
        self.fourCycles += 1 if (cycle == 4) else 0
        self.fiveCycles += 1 if (cycle == 5) else 0
   
#If the debugger mode is on then this function will print line by line output
    def print(self, userMode):
        if(self.debugMode == 1):
            imm  = int(self.I[16:32],2) if self.I[16]=='0' else twoComplement(self.I[16:32])
            imm = str(imm)
            s = str(int(self.I[6:11],2))         #read in the register - RS
            t = str(int(self.I[11:16],2))        #read in ther other register - Rt
            d = str(int(self.I[16:21] ,2))       #reads in the register RD
            PcCount = "{:<4}".format(self.pc*4)         #This line is to help with the printout below - PC counts will always be 4 digits
            
            self.multiS.append(self.name)
            self.slowS.append(self.name)
            self.fastS.append(self.name)
            if(userMode == "1"):
                if((self.name  == "addi") | (self.name == "ori")):
                    print("{:<3}".format(self.cycle-4)+" |PC: "+" " +PcCount + self.name +" $"+ t + ", $ " + s + ", " + imm + "   Taking 4 cycles " + self.print_multiState())
                elif((self.name == "slt") | (self.name == "sltu")):
                    print(  "{:<3}".format(self.cycle-4)+ " |PC: "+" " +PcCount + self.name+" $" + d + ", $" + s + ", $" + t + "   Taking 4 cycles "+ self.print_multiState())
                elif((self.name == "add") | (self.name == "or") | (self.name == "sub") | (self.name == "and") | (self.name == "xor") | (self.name == "addu") ):
                    print(  "{:<3}".format(self.cycle-4)+" |PC: "+" "+PcCount + self.name+" $" + d + ", $" + s + " , $" + t + "   Taking 4 cycles "+ self.print_multiState())
                elif((self.name == "sll") | (self.name == "slr")):
                    print(  "{:<3}".format(self.cycle-4) +" |PC: "+" "+ PcCount+ self.name+ " $" + d + ", $" + t + ", $" + imm + "   Taking 4 cycles "  + self.print_multiState())
                elif((self.name == "beq") | (self.name == "bne")):
                    print(  "{:<3}".format(self.cycle-3)+ " |PC: " +" "+PcCount + self.name+ " $" + s + ", $" + t + "," + imm + "   Taking 3 cycles " + self.print_multiState())
                elif(self.name == "sw" ):
                    print(  "{:<3}".format(self.cycle-4)+ " |PC :" +" "+PcCount +"sw  $" + t  + ", {:<4}".format(hex(int(imm)))+ "($" + s + ")" + "   Taking 4 cycles " + self.print_multiState() )
                elif(self.name == "lw"):
                    print(  "{:<3}".format(self.cycle-5)+ " |PC :" +" "+PcCount + "lw $" + t + ", {:<4}".format(hex(int(imm))) + "($" + s + ")" + "   Taking 5 cycles "+ self.print_multiState() )
                else:
                    print("")

            if(userMode == "2"):
                if((self.name  == "addi") | (self.name == "ori")):
                    print("Slow Cycle: " +"{:<3}".format(self.slowCycle-1)+" |PC: "+" " +PcCount + self.name +" $"+ t + ", $ " + s + ", " + imm + "   Taking 1 cycle " +self.print_slowState())
                elif((self.name == "slt") | (self.name == "sltu")):
                    print("Slow Cycle: " +"{:<3}".format(self.slowCycle-1)+" |PC: "+" " +PcCount + self.name +" $"+ t + ", $ " + s + ", " + imm + "   Taking 1 cycle "+self.print_slowState())
                elif((self.name == "add") | (self.name == "or") | (self.name == "sub") | (self.name == "and") | (self.name == "xor") | (self.name == "addu") ):
                    print("Slow Cycle: " +"{:<3}".format(self.slowCycle-1)+" |PC: "+" " +PcCount + self.name +" $"+ t + ", $ " + s + ", " + imm + "   Taking 1 cycle "+self.print_slowState())
                elif((self.name == "sll") | (self.name == "slr")):
                    print("Slow Cycle: " +"{:<3}".format(self.slowCycle-1)+" |PC: "+" " +PcCount + self.name +" $"+ t + ", $ " + s + ", " + imm + "   Taking 1 cycle "+self.print_slowState() )
                elif((self.name == "beq") | (self.name == "bne")):
                    if((s == "0") and (t == "0")): # Check if beq is at the end of the program
                        print("Slow Cycle: " +"{:<3}".format(self.slowCycle-5)+" |PC: "+" " +PcCount + self.name +" $"+ t + ", $ " + s + ", " + imm + "   Taking 4 cycles " +self.print_slowState())
                    else:
                        print("Slow Cycle: " +"{:<3}".format(self.slowCycle-1)+" |PC: "+" " +PcCount + self.name +" $"+ t + ", $ " + s + ", " + imm + "   Taking 1 cycle "+self.print_slowState())
                elif(self.name == "sw" ):
                    print("{:<3}".format(self.slowCycle-1)+" |PC: "+" " +PcCount + self.name +" $"+ t + ", $ " + s + ", " + imm + "   Taking 1 cycle " +self.print_slowState())
                elif(self.name == "lw"):
                    print("Slow Cycle: " +"{:<3}".format(self.slowCycle-1)+" |PC: "+" " +PcCount + self.name +" $"+ t + ", $ " + s + ", " + imm + "   Taking 1 cycle" +self.print_slowState())
                else:
                    print("")

            if(userMode == "3"):
                if((self.name  == "addi") | (self.name == "ori")):
                    print("Fast Cycle: " +"{:<3}".format(self.fastCycle-1)+" |PC: "+" " +PcCount + self.name +" $"+ t + ", $ " + s + ", " + imm + "   Taking 1 cycle " +self.print_fastState())
                elif((self.name == "slt") | (self.name == "sltu")):
                    print("Fast Cycle: " +"{:<3}".format(self.fastCycle-1)+" |PC: "+" " +PcCount + self.name +" $"+ t + ", $ " + s + ", " + imm + "   Taking 1 cycle " +self.print_fastState())
                elif((self.name == "add") | (self.name == "or") | (self.name == "sub") | (self.name == "and") | (self.name == "xor") | (self.name == "addu") ):
                    print("Fast Cycle: " +"{:<3}".format(self.fastCycle-1)+" |PC: "+" " +PcCount + self.name +" $"+ t + ", $ " + s + ", " + imm + "   Taking 1 cycle " +self.print_fastState())
                elif((self.name == "sll") | (self.name == "slr")):
                    print("Fast Cycle: " +"{:<3}".format(self.fastCycle-1)+" |PC: "+" " +PcCount + self.name +" $"+ t + ", $ " + s + ", " + imm + "   Taking 1 cycle " +self.print_fastState())
                elif((self.name == "beq") | (self.name == "bne")):
                    if((s == "0") and (t == "0")): # Check if beq is at the end of the program
                        print("Fast Cycle: " +"{:<3}".format(self.fastCycle-5)+" |PC: "+" " +PcCount + self.name +" $"+ t + ", $ " + s + ", " + imm + "   Taking 4 cycle " +self.print_fastState())
                    else:
                        print("Fast Cycle: " +"{:<3}".format(self.fastCycle-1)+" |PC: "+" " +PcCount + self.name +" $"+ t + ", $ " + s + ", " + imm + "   Taking 1 cycle " +self.print_fastState())
                elif(self.name == "sw" ):
                    print("Fast Cycle: " +"{:<3}".format(self.fastCycle-1)+" |PC: "+" " +PcCount + self.name +" $"+ t + ", $ " + s + ", " + imm + "   Taking 1 cycle " +self.print_fastState())
                elif(self.name == "lw"):
                    print("Fast Cycle: " +"{:<3}".format(self.fastCycle-1)+" |PC: "+" " +PcCount + self.name +" $"+ t + ", $ " + s + ", " + imm + "   Taking 1 cycle " +self.print_fastState())
                else:
                    print("")



	# Functions to print the pipeline stages each instruction is in
    def print_multiState(self):
        return "\nF : " + self.multiS[len(self.multiS)-1] + " D : " + self.multiS[len(self.multiS)-2] + " E : " + self.multiS[len(self.multiS)-3] + " M : " + self.multiS[len(self.multiS)-4] + " W : " + self.multiS[len(self.multiS)-5] +"\n"
    def print_slowState(self):
        return "\nF : " + self.slowS[len(self.slowS)-1] + " D : " + self.slowS[len(self.slowS)-2] + " E : " + self.slowS[len(self.slowS)-3] + " M : " + self.slowS[len(self.slowS)-4] + " W : " + self.slowS[len(self.slowS)-5] + "\n"
    def print_fastState(self):
        return "\nF : " + self.fastS[len(self.fastS)-1] + " D : " + self.fastS[len(self.fastS)-2] + " E : " + self.fastS[len(self.fastS)-3] + " M : " + self.fastS[len(self.fastS)-4] + " W : " + self.fastS[len(self.fastS)-5] + "\n"
          
#The function below will print out the values stored into the registers and memory locations at the end of the the program
    def finalOutput(self, reg, mem, PC, hit, miss, userMode):
        print("\n======================STATISTICS=========================")
        if(userMode == "1"):
            print("====================MULTI-CYCLE=======================")
            print("Total # of cycles: " + str(self.cycle))
            print("Dynamic Instruction count = {0:<4}\n".format(self.DIC)+ "Dynamic Instruction Breakdown: ")
            print("         " + str(self.threeCycles) + " instructions take 3 cycles" )  
            print("         " + str(self.fourCycles) + " instructions take 4 cycles" )
            print("         " + str(self.fiveCycles) + " instructions take 5 cycles\n" )
        
        if(userMode == "2"):
            print("=====================SLOW PIPELINE========================")
            print("Total # of cycles: " + str(4) + " + " + str(self.DIC) + " + " + str(self.NOPcount) + " = " + str(self.DIC+4+self.NOPcount))
            print("Total Instruction entering pipeline = {0:<4}".format(self.DIC))
            print("Finishing up the last instruction: 4")
            print("Total NOPs = {:<3}".format(self.NOPcount))
            print("Dynamic Instruction count = {0:<4}\n".format(self.DIC))
            print("NOP Breakdown: ")
            print("         " + str(self.DataHazardSlow) + " Data Hazards")
            print("         " + str(self.ControlHazardSlow) + " Control Hazards")

        if(userMode == "3"):
            if(self.ControlHazardFast != 0): #To account for the extra looping in the fast_pipe function
                self.ControlHazardFast -= 2
            #if(self.CompBranchHazard == True): #To account for the extra loop when the instruction is run when the branch will not be taken
            #    self.DataHazardFast -= 1
            print("==================FAST PIPELINE===========================")
            print("Total # of cycles: " + str(4) + " + " + str(self.DIC) + " + " + str(self.ControlHazardFast) + " + " + str(self.DataHazardFast) +" = " + str(self.DIC+4+self.ControlHazardFast+self.DataHazardFast))
            print("Total Instruction entering pipeline = {0:<4}".format(self.DIC))
            print("Finishing up the last instruction: 4")
            #print("Total NOPs = {:<3}".format(self.NOPcount))
            print("Dynamic Instruction count = {0:<4}\n".format(self.DIC))
            print("Delay Breakdown: ")
            print("         " + str(self.DataHazardFast) + " Data Hazards")
            print("         " + str(self.ControlHazardFast) + " Control Hazards")
            print("Multi-Cycle Comparison: Fast Pipeline is " + str((self.cycle) - (self.DIC+4+self.ControlHazardFast+self.DataHazardFast)) + " cycles faster")
            print("Slow Pipeline Comparison: Fast Pipeline is " + str((self.DIC+4+self.NOPcount) - (self.DIC+4+self.ControlHazardFast+self.DataHazardFast)) + " cycles faster")

        if((userMode == "2") | (userMode == "3")): #cache outputs
            print("\n=======================Cache=========================")
            print("Cache Hit  = " + str(hit))
            print("Cache Miss  = " + str(miss))
            print(" % Hit rate  = " + str(hit/(hit+miss)* 100) + "% ")

        print("========================REGISTER VALUE=========================")
        n = 0
        while (n < 32):
            print("${:<2} = {:<8}     ${:<2} = {:<8}    ${:<2} = {:<8}     ${:<2} = {:<8}".format(n, reg[n], n+1, reg[n+1], n+2, reg[n+2], n+3, reg[n+3]))
            n = n + 4

        print("========================Memory VALUE===========================")
        n = 0
        c = 8192
        while (n < 129):
            print("${:<2} = {:<12}     ${:<2} = {:<12}    ${:<2} = {:<12}     ${:<2} = {:<12}".format(hex(c), mem[n], hex(c+4), mem[n+4], hex(c+8), mem[n+8], hex(c+12), mem[n+12]))
            n = n + 16
            c = c + 16





    #check for hazards and update NOPcount, stallCount, flushCount and other statistics
    def slow_pipe(self, currentInst, prevInst, prevPrevInst, userMode):
        cRs = currentInst[6:11]     #current instruction register Rs
        cRt = currentInst[11:16]    #currentcurreint register Rt 
        if ((prevInst != "")  & (prevInst[0:6] != "000000")):        #if the previous instruction is R-type or I-type choose pRd appropriately
            pRd=prevInst[11:16]      
        else :
            pRd = prevInst[16:21]
        if prevPrevInst[0:6] != "000000":    #if the prevPrevInst  R-type or I-type choose ppRd approproately
            ppRd = prevPrevInst[11:16] 
        else : 
            ppRd=prevPrevInst[16:21]
        if(prevInst != ""):
            if((prevInst[0:6] != "000100") & (prevInst[0:6] != "000101")):
                if((pRd == cRs) | (pRd == cRt)): 
                   self.NOPcount += 2
                   self.DataHazardSlow +=2
                   self.slowS.append("NOP")
                   self.slowS.append("NOP")                    
                   if((self.debugMode == 1) & (userMode  == "2")):
                      print("Slow Cycle: " +  "{:<3}".format(self.slowCycle)+ " |PC: "+" {:<4}".format(self.pc*4) + "NOP taking 2 cycles")
                   self.slowCycle +=2
                elif((ppRd != prevInst[6:11])|(ppRd != prevInst[11:16])):
                    if((ppRd == cRs) | (ppRd == cRt)):
                        self.NOPcount +=1
                        self.DataHazardSlow +=1
                        self.slowS.append("NOP")
                        if((self.debugMode == 1) & (userMode  == "2")):
                            print("Slow Cycle: " +  "{:<3}".format(self.slowCycle)+ " |PC: "+" {:<4}".format(self.pc*4) + "NOP taking 1 cycle") 
                        self.slowCycle +=1
            else:  #if the curent instruction is beq or bne add 3 NOPs
                self.NOPcount += 3
                self.ControlHazardSlow += 3
                self.slowS.append("NOP")
                self.slowS.append("NOP")
                self.slowS.append("NOP")
                if((self.debugMode == 1) & (userMode  == "2")):
                    print("Slow Cycle: " +  "{:<3}".format(self.slowCycle)+ " |PC: "+" {:<4}".format(self.pc*4) + "NOP taking 3 cycles")
                self.slowCycle += 3
        
    def fast_pipe(self, currentInst, prevInst, prevPrevInst):
        cRs = currentInst[6:11]     #current instruction register Rs
        cRt = currentInst[11:16]    #currentcurreint register Rt
        #self.DataHazard = 0
        #self.ControlHazard = 0
        #self.NOPcount = 0
        if ((prevInst != "")  & (prevInst[0:6] != "000000")):        #if the previous instruction is R-type or I-type choose pRd appropriately
            pRd=prevInst[11:16]      
        else :  
            pRd = prevInst[16:21]
        if prevPrevInst[0:6] != "000000":    #if the prevPrevInst  R-type or I-type choose ppRd approproately
            ppRd = prevPrevInst[11:16] 
        else : 
            ppRd=prevPrevInst[16:21]
        if(prevInst != ""): 
            if((currentInst[0:6] == "000100") | (currentInst[0:6] == "000101")): # Calculate branch hazard
                self.ControlHazardFast += 1 #if the curent instruction is beq or bne, there is a delay of 1 cycle
                self.fastS.append("Delay")
                if(self.debugMode == 1):
                    print("Fast Cycle: " +  "{:<3}".format(self.fastCycle)+ " |PC: "+" {:<4}".format(self.pc*4) + "Control Hazard: Taken branch delay taking 1 cycle")
                self.fastCycle += 1
                if((pRd == cRs) | (pRd == cRt)): # Check if previous instruction uses same registers as the branch instruction
                    #self.CompBranchHazard = True
                    self.DataHazardFast +=1
                    self.fastS.append("Delay")
                    if(self.debugMode == 1):
                        print("Fast Cycle: " +  "{:<3}".format(self.fastCycle)+ " |PC: "+" {:<4}".format(self.pc*4) + "Data Hazard: Compute-branch delay taking 1 cycle")
                    self.fastCycle += 1
            elif(prevInst[0:6] == "100011"): # lw-use hazard
                if((pRd == cRs) | (pRd == cRt)): # Check if the current instruction uses the same registers as the previous LW instruction
                    self.DataHazardFast +=1
                    self.fastS.append("Delay")
                    if(self.debugMode == 1):
                        print("Fast Cycle: " +  "{:<3}".format(self.fastCycle)+ " |PC: "+" {:<4}".format(self.pc*4) + "Data Hazard: LW-use delay taking 1 cycle")
                    self.fastCycle += 1
            # Still need to get output for the fast pipeline implementation
            #Keep track of which instructions are still in a 5-stage pipeline
            #Add additional information for what hazards occur and what forward path is used
            #Include total cycle count as well as how many cycles faster fast pipeline is that multi-cycle
            #and slow pipeline implementations. Also how many control/data hazards there were 

    #Cache Staring here
class Block():
    def __init__(self, wordsPerBlock, whichSet, debugMode):
        self.data  = [0]*wordsPerBlock
        self.size = wordsPerBlock
        self.setIndex = format(whichSet, 'b') 
        self.valid = False
        self.tag = "undefined"
        self.debugMode = debugMode
    def loadBlock(self, memIndex, tag, mem):
        if(self.debugMode == 1):
            print("memIndex: " + str(hex(memIndex)) + " Tag: " + format(tag, "b"))
        self.tag = tag
        self.valid = True
        for i in range(self.size):
            self.data[i] = mem[(i*4)+memIndex-int(8192)]
    def checkBlockTag(self, tag):
        if (self.valid == False):
            return -1
        if (self.tag != tag):
            return -1
    def readBlock(self, offset, tag):
        if(self.debugMode == 1):
            print("Tag: " + format(tag, "b"))
        return self.data[int(offset/4)]

class cache:
    def __init__(self, b, numberOfSets, nWays, debugMode):
        self.wordOffset = ceil(log(b, 2))
        self.wordsPerBlock = int(b/4)
        self.wordsInByte = b
        self.cache=[]
        self.debugMode = debugMode
        self.nWays = nWays
        if(nWays != 1):
            self.lruArr= [[0 for x in range(nWays)] for y in range(numberOfSets)] #create a list of numberOfsets each with nWays arr
        self.currentIndex = [0]*numberOfSets                                    #initialize currentIndex for all of them to 0
        self.numberOfSets = numberOfSets
        tempBlock = []
        self.hit = 0
        self.miss = 0
        self.cache = [[Block(self.wordsPerBlock, i,self.debugMode) for i in range(nWays)]for j in range(numberOfSets)]
        self.blockCount = numberOfSets * nWays
        self.current = 0

    def grab_LRU(self, setIndex):             #returns the LRU tag
        return self.lruArr[setIndex][0]

    def update(self, tag, setIndex):    #this is called when the blocks are full and there is no hit with the tags
        for i in range(self.nWays):
            if(self.lruArr[setIndex][i] == tag):
                for i in range(self.nWays-1):
                    self.lruArr[setIndex][i] = self.lruArr[setIndex][i+1]
                self.lruArr[setIndex][self.nWays-1]= tag

    def LRU(self, tag, setIndex):
        for i in range(self.nWays-1):
            self.lruArr[setIndex][i] = self.lruArr[setIndex][i+1]
            self.lruArr[setIndex][self.nWays-1]= tag

    def printB(self, setIndex, blockNum):
        print("Block = [", end=" ")
        for j in range(self.wordsPerBlock):
           print(str(self.cache[setIndex][blockNum].data[j])+ ", ", end="")
        print("]", end="")
        print("")

    def getHit(self):
        return self.hit
    def getMiss(self):
        return self.miss

    def accessCache(self, addr, mem, val):
        inBlkOffset =int(addr[-self.wordOffset:],2)
        if(self.numberOfSets == 1):
            setIndex = 0
        else:
            setIndex = int(addr[-(int(ceil(log(self.numberOfSets,2))) + self.wordOffset):-self.wordOffset],2)
        tag = int(addr[:-(self.wordOffset +ceil(log(self.numberOfSets,2)))],2)
        memIndex = int(addr,2)
        found = False

        if(self.nWays != 1):
            for i in range(self.nWays):
                if(self.cache[setIndex][i].checkBlockTag(tag) != -1 ):   #looks for a matching tag
                    if(self.debugMode == 1):
                        print("Cache HIT!! Reading a block...")
                    self.hit+=1
                    found = True
                    data = self.cache[setIndex][i].readBlock(inBlkOffset, tag)
                    self.printB(setIndex, i)
                    return
            for i in range(self.nWays):
                if((self.cache[setIndex][i].tag == "undefined")):     #looks for empty block
                    if(self.debugMode == 1):
                        print("Cache MISS!! Loading a block...")
                    self.miss +=1
                    self.lruArr[setIndex][self.currentIndex[setIndex]] = tag
                    self.currentIndex[setIndex] += 1
                    self.cache[setIndex][i].loadBlock(memIndex, tag, mem)
                    self.printB(setIndex, i)
                    return
            if(found == False): #blocks are full so we have to use LRU list element 0 and move it to the fron
                if(self.debugMode == 1):
                    print("Cache MISS!! Loading a block...")
                self.miss +=1
                for i in range(self.nWays):
                    if(self.lruArr[setIndex][0] == self.cache[setIndex][i].tag):
                        self.cache[setIndex][i].loadBlock(memIndex, tag, mem)
                        self.LRU(tag, setIndex)
                        self.printB(setIndex, i)
                        return
        else:
            if(self.cache[setIndex][0].tag == tag):
                if(self.debugMode == 1):
                    print("Cache HIT  Reading Block...")
                self.hit +=1
                self.cache[setIndex][0].readBlock(inBlkOffset, tag)
                if(self.debugMode == 1):
                    self.printB(setIndex,0)
            elif(self.cache[setIndex][0].tag != tag):
                if(self.debugMode == 1):
                    print("Cache MISS Loading Block...")
                self.miss+=1
                self.cache[setIndex][0].loadBlock(memIndex, tag, mem)
                if(self.debugMode == 1):
                    self.printB(setIndex, 0)


def disassemble(instructions, debugMode): 
    line = 0                          #keeps track of what line of of instrcution form the txt file is being run
    finished = False                        #is the program finished?
    reg = [0]*32                            #declare register array all initialized to 0
    mem = [0]*1000                            #memory from 0x2000 ot 0x2050
    fetch = instructions[line]
    stats = Statistics(debugMode)
    #fetch = instructio i or current instruction
    prevInst = ""                   #instruction i-1
    prevPrevInst = ""               #instruction i-2
    instNameArr = []
    tmpOffset = 0 #this is a dummy vriable

    userMode = input("What mode Do u want to run 1:Multi Cycle     2:Slow Pipeline     3:Fast Pipelin  : ")
    print("")
    if((userMode == "2") | (userMode == "3")):
        wordsPerBlock = int(input("Enter the block size b(# of bytes): "))
        numberOfSets = int(input("Enter the number of sets S:  "))
        nWays = int(input("Enter N: "))
        _cache = cache(wordsPerBlock, numberOfSets, nWays, debugMode)


    while(not finished):
        fetch = instructions[line]
        s = int(fetch[6:11], 2)         #read in the register - RS
        t = int(fetch[11:16], 2)        #read in ther other register - Rt
        d = int(fetch[16:21], 2)        #reads in the register RD

        if((userMode == "2")  | (userMode == "3")):
            stats.slow_pipe(fetch, prevInst, prevPrevInst,userMode)
        if(userMode == "3"):
            stats.fast_pipe(fetch, prevInst, prevPrevInst)
        if(fetch[0:6] == "001000"):             #addi
            reg[t] = reg[s] + twoComplement(str(fetch[16:33]))  # Rt = Rs + imm
            stats.log(fetch, "addi", 4, 1, 1, line)
            prevPrevInst = prevInst
            prevInst = fetch
            line += 1
        elif (fetch[0:6] == "001101"):           #ori
            reg[t] = reg[s] | int(fetch[16:32],2)       #Rt = Rs | imm
            stats.log(fetch, "ori", 4, 1, 1, line)
            prevPrevInst = prevInst
            prevInst = fetch
            line +=1
        elif(fetch[0:6] == "000000"):           # R-type registers
            if (fetch[26:32] == "101010"):      #SLT
                if(reg[s] < reg[t]):            # Rd = Rs < Rt
                    reg[d] = 1                  #Rd = 1
                else:
                    reg[d] = 0                  # Rd = 0
                stats.log(fetch, "slt", 4, 1, 1, line)
                prevPrevInst = prevInst
                prevInst = fetch
                line +=1
            elif(fetch[26:32] == "101011"):       #SLTU
                if(reg[s] < (reg[t] + 2**32)):            # Rd = Rs < Rt
                    reg[d] = 1                  #Rd = 1
                else:
                    reg[d] = 0
                prevPrevInst = prevInst
                prevInst = fetch
                line +=1
                stats.log(fetch, "sltu", 4, 1, 1, line)
            elif (fetch[26:32] == "100000"):     #add
                reg[d] = reg[s] + reg[t]         #Rd = Rs + Rt
                stats.log(fetch, "add", 4, 1, 1, line)
                prevPrevInst = prevInst
                prevInst = fetch
                line +=1
            elif (fetch[26:32] == "100001"):      #addu
                reg[d] = twoComplement(format(reg[s],"32b")) + twoComplement(format(reg[t], "32b"))          #Rd = Rs + Rt
                temp = 0xffffffff
                reg[d] = reg[d] & temp
                temp = format(reg[d], "32b")
                if(temp[0] == '1'):
                    reg[d] = -(2**32)+reg[d]
                stats.log(fetch, "addu", 4, 1, 1, line)
                prevPrevInst = prevInst
                prevInst = fetch
                line +=1
            elif (fetch[26:32] == "100101"):       #or
                reg[t] = reg[s] | reg[t]           #Rd = Rs | Rt
                stats.log(fetch, "or", 4, 1, 1, line)
                prevPrevInst = prevInst
                prevInst = fetch
                line +=1
            elif (fetch[26:32] == "100010"):       #SUB
                reg[d] = reg[s] - reg[t]           #Rd = Rs - Rt
                stats.log(fetch, "sub", 4, 1, 1, line)
                prevPrevInst = prevInst
                prevInst = fetch
                line +=1
            elif(fetch[26:32] == "100110"):        #XOR
                reg[d] = reg[s] ^ reg[t]           #Rd = Rs ^ Rt
                tmp = format(reg[d], "32b")
                if(tmp[0] == 1):
                    reg[d] = reg[d] + (2**32)
                stats.log(fetch, "xor", 4, 1, 1, line)
                prevPrevInst = prevInst
                prevInst = fetch
                line+= 1
            elif(fetch[26:32] == "100100"):        #AND
                reg[d] = reg[s] & reg[t]           #Rd = RS & Rt
                stats.log(fetch, "and", 4, 1, 1, line)
                prevPrevInst = prevInst
                prevInst = fetch
                line +=1
            elif(fetch[26:32] == "000000"):
                imm = int(fetch[21:26], 2)         #SLL
                reg[d]  = reg[t] << imm            #Rd = Rt <<imm
                temp = 0xffffffff
                reg[d] = reg[d] & temp
                temp = format(reg[d], "32b")
                if(temp[0] == '1'):
                    reg[d] = -(2**32)+reg[d]
                stats.log(fetch, "sll", 4, 1, 1, line)
                prevPrevInst = prevInst
                prevInst = fetch
                line +=1
        elif(fetch[0:6] == "000100"):               #BEQ
            if(fetch[6:32] =="00000000001111111111111111" ): # Check if beq is at the end of the program
                stats.log(fetch, "beq", 3, 4, 4, line) # Infinite loop beq for program end
            else:
                stats.log(fetch, "beq", 3, 1, 1, line) # Regular beq instruction
            prevPrevInst = prevInst
            prevInst = fetch
            line+=1
            if(reg[s] == reg[t]):
                offset = twoComplement(fetch[16:32])
                line = line + offset
            if(fetch[6:32] =="00000000001111111111111111" ):
                stats.print(userMode)
                if((userMode == "2") | (userMode == "3")):
                    stats.finalOutput(reg, mem, line, _cache.getHit(), _cache.getMiss(), userMode)
                else:
                    stats.finalOutput(reg, mem, line,0, 0, userMode)
                finished = True
        elif(fetch[0:6] == "000101"):               #BNE
            stats.log(fetch, "bne", 3, 1, 1, line)
            prevPrevInst = prevInst
            prevInst = fetch
            line +=1
            if(reg[s] != reg[t]):
                tmpOffset = twoComplement(fetch[16:32])
                line = line + tmpOffset
        elif(fetch[0:6] == "101011"):               #SW
            stats.log(fetch, "sw", 4, 1, 1, line)
            prevPrevInst = prevInst
            prevInst = fetch
            line +=1
            offset = twoComplement(str(fetch[16:32]))           
            mem[int(reg[s] + offset) - int(8192)] = reg[t]
            #8192  = 0x2000, it indicates that our mem[0] = mem[0x2000], the fist element in mem array is our memory location [0x2000] ]
            if((userMode == "2") | (userMode == "3")):
                addr = format(reg[s]+offset, "032b")
                _cache.accessCache(addr, mem, 0)

        elif(fetch[0:6] == "100011"):               #LW
            stats.log(fetch, "lw", 5, 1, 1, line)
            prevPrevInst = prevInst
            prevInst = fetch
            line +=1
            offset = twoComplement(str(fetch[16:32]))
            reg[t] = mem[reg[s] + offset - int(8192)]
            if((userMode == "2") | (userMode == "3")):
                addr = format(reg[s]+offset, "032b")
                _cache.accessCache(addr, mem, 1)
        else:
            finished = True
        if(not finished):
            stats.print(userMode)

def main():
   # openFile = str(input("Enter the name of the file with the extention .txt : "))
    inFile = open("testCase1XHex.txt", "r")       #opens the file
    instructions = []                       #declares an array
    
    for line in inFile:
        if(line == "\n" or line[0] == '#'): 
            continue
        line = line.replace('\n', '')
        line = format(int(line, 16), "032b")    #formats tthe number as 32bits and uses 0 as filler
        instructions.append(line)   
    inFile.close()

    debugMode = int(input("1: Debug Mode \n0: Normal Mode : "))
    print("")
    disassemble(instructions, debugMode) 
main()

