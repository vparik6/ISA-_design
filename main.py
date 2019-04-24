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
         self.CompBranchHazard = False #Boolean value to check if data hazard is a CompBranch or not
         self.NOPcount = 0        #keeps track of NOP
         self.flushCount = 0      #keeps track of flush
         self.stallCount = 0      #keeps track of stall count
         self.debugMode = debugMode
         
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
    def print(self):
        if(self.debugMode == 1):
            imm  = int(self.I[16:32],2) if self.I[16]=='0' else twoComplement(self.I[16:32])
            imm = str(imm)
            s = str(int(self.I[6:11],2))         #read in the register - RS
            t = str(int(self.I[11:16],2))        #read in ther other register - Rt
            d = str(int(self.I[16:21] ,2))       #reads in the register RD
            PcCount = "{:<4}".format(self.pc*4)         #This line is to help with the printout below - PC counts will always be 4 digits

            if((self.name  == "addi") | (self.name == "ori")):
                print("Cycle: " +"{:<3}".format(self.cycle-4)+" |PC: "+" " +PcCount + self.name +" $"+ t + ", $ " + s + ", " + imm + "   Taking 4 cycles " + multiS())
                print("Slow Cycle: " +"{:<3}".format(self.slowCycle-1)+" |PC: "+" " +PcCount + self.name +" $"+ t + ", $ " + s + ", " + imm + "   Taking 1 cycle " +slowS())
            elif((self.name == "slt") | (self.name == "sltu")):
                print("Cycle: " +  "{:<3}".format(self.cycle-4)+ " |PC: "+" " +PcCount + self.name+" $" + d + ", $" + s + ", $" + t + "   Taking 4 cycles "+ multiS())
                print("Slow Cycle: " +"{:<3}".format(self.slowCycle-1)+" |PC: "+" " +PcCount + self.name +" $"+ t + ", $ " + s + ", " + imm + "   Taking 1 cycle "+slowS())
            elif((self.name == "add") | (self.name == "or") | (self.name == "sub") | (self.name == "and") | (self.name == "xor") | (self.name == "addu") ):
                print("Cycle: " +  "{:<3}".format(self.cycle-4)+" |PC: "+" "+PcCount + self.name+" $" + d + ", $" + s + " , $" + t + "   Taking 4 cycles "+ multiS())
                print("Slow Cycle: " +"{:<3}".format(self.slowCycle-1)+" |PC: "+" " +PcCount + self.name +" $"+ t + ", $ " + s + ", " + imm + "   Taking 1 cycle "+slowS())
            elif((self.name == "sll") | (self.name == "slr")):
                print("Cycle: " +  "{:<3}".format(self.cycle-4) +" |PC: "+" "+ PcCount+ self.name+ " $" + d + ", $" + t + ", $" + imm + "   Taking 4 cycles "  + multiS())
                print("Slow Cycle: " +"{:<3}".format(self.slowCycle-1)+" |PC: "+" " +PcCount + self.name +" $"+ t + ", $ " + s + ", " + imm + "   Taking 1 cycle "+slowS() )
            elif((self.name == "beq") | (self.name == "bne")):
                print("Cycle: " +  "{:<3}".format(self.cycle-3)+ " |PC: " +" "+PcCount + self.name+ " $" + s + ", $" + t + "," + imm + "   Taking 3 cycles " + multiS())
                if((s == "0") and (t == "0")): # Check if beq is at the end of the program
                    print("Slow Cycle: " +"{:<3}".format(self.slowCycle-5)+" |PC: "+" " +PcCount + self.name +" $"+ t + ", $ " + s + ", " + imm + "   Taking 4 cycles " +slowS())
                print("Slow Cycle: " +"{:<3}".format(self.slowCycle-1)+" |PC: "+" " +PcCount + self.name +" $"+ t + ", $ " + s + ", " + imm + "   Taking 1 cycle "+slowS())
            elif(self.name == "sw" ):
                print("Cycle: " +  "{:<3}".format(self.cycle-4)+ " |PC :" +" "+PcCount +"sw  $" + t  + ", {:<4}".format(hex(int(imm)))+ "($" + s + ")" + "   Taking 4 cycles " + multiS() )
                print("Slow Cycle: " +"{:<3}".format(self.slowCycle-1)+" |PC: "+" " +PcCount + self.name +" $"+ t + ", $ " + s + ", " + imm + "   Taking 1 cycle " +slowS())
            elif(self.name == "lw"):
                print("Cycle: " +  "{:<3}".format(self.cycle-5)+ " |PC :" +" "+PcCount + "lw $" + t + ", {:<4}".format(hex(int(imm))) + "($" + s + ")" + "   Taking 5 cycles "+ multiS() )
                print("Slow Cycle: " +"{:<3}".format(self.slowCycle-1)+" |PC: "+" " +PcCount + self.name +" $"+ t + ", $ " + s + ", " + imm + "   Taking 1 cycle" +slowS())
            else:
                print("")
            print("\n")

    def print_multiState(self):
        return "F : " + self.multiS[length(self.multiS)-1] + " D : " + self.multiS[length(self.multiS)-2] + " E : " + self.multiS[length(self.multiS)-3] + " M : " + self.multiS[length(self.multiS)-4] + " W : " + self.multiS[length(self.multiS)-5]
    def print_slowState(self):
        return "F : " + self.slowS[length(self.slowS)-1] + " D : " + self.slowS[length(self.slowS)-2] + " E : " + self.slowS[length(self.slowS)-3] + " M : " + self.slowS[length(self.slowS)-4] + " W : " + self.slowS[length(self.slowS)-5]
    def print_fastState(self):
        return "F : " + self.fastS[length(self.fastS)-1] + " D : " + self.fastS[length(self.fastS)-2] + " E : " + self.fastS[length(self.fastS)-3] + " M : " + self.fastS[length(self.fastS)-4] + " W : " + self.fastS[length(self.fastS)-5]
          
#The function below will print out the values stored into the registers and memory locations at the end of the the program
    def finalOutput(self, reg, mem, PC):
        print("\n===============STATISTICS===============\n")
        print("===SLOW PIPELINE===")
        print("Total # of cycles: " + str(4) + " + " + str(self.DIC) + " + " + str(self.NOPcount) + " = " + str(self.DIC+4+self.NOPcount))
        print("Total Instruction entering pipeline = {0:<4}".format(self.DIC))
        print("Finishing up the last instruction: 4")
        print("Total NOPs = {:<3}".format(self.NOPcount))
        print("Dynamic Instruction count = {0:<4}\n".format(self.DIC)+ "Dynamic Instruction Breakdown: ")
        print("         " + str(self.threeCycles) + " instructions take 3 cycles" )  
        print("         " + str(self.fourCycles) + " instructions take 4 cycles" )
        print("         " + str(self.fiveCycles) + " instructions take 5 cycles" )
        print("NOP Breakdown: ")
        print("         " + str(self.DataHazardSlow) + " Data Hazards")
        print("         " + str(self.ControlHazardSlow) + " Control Hazards")
        
        if(self.ControlHazardFast != 0): #To account for the extra looping in the fast_pipe function
            self.ControlHazardFast -= 2
        if(self.CompBranchHazard == True): #To account for the extra loop when the instruction is run when the branch will not be taken
            self.DataHazardFast -= 1
        print("\n===FAST PIPELINE===")
        print("Total # of cycles: " + str(4) + " + " + str(self.DIC) + " + " + str(self.ControlHazardFast) + " + " + str(self.DataHazardFast) +" = " + str(self.DIC+4+self.ControlHazardFast+self.DataHazardFast))
        print("Total Instruction entering pipeline = {0:<4}".format(self.DIC))
        print("Finishing up the last instruction: 4")
        #print("Total NOPs = {:<3}".format(self.NOPcount))
        print("Dynamic Instruction count = {0:<4}\n".format(self.DIC)+ "Dynamic Instruction Breakdown: ")
        print("         " + str(self.threeCycles) + " instructions take 3 cycles" )  
        print("         " + str(self.fourCycles) + " instructions take 4 cycles" )
        print("         " + str(self.fiveCycles) + " instructions take 5 cycles" )
        print("Delay Breakdown: ")
        print("         " + str(self.DataHazardFast) + " Data Hazards")
        print("         " + str(self.ControlHazardFast) + " Control Hazards")
        #print("Multi-Cycle Comparison: " + str((MULTICYCLE CALCULATION) - (self.DIC+4+self.ControlHazardFast+self.DataHazardFast)) + " cycles faster")
        print("Slow Pipeline Comparison: " + str((self.DIC+4+self.NOPcount) - (self.DIC+4+self.ControlHazardFast+self.DataHazardFast)) + " cycles faster")
        
        print("\n===OTHER TESTING===")
        print("Slow Pipeline Cycles: " + str(self.slowCycle))
        print("Fast Pipeline Cycles: " + str(self.fastCycle))
    #check for hazards and update NOPcount, stallCount, flushCount and other statistics
    def slow_pipe(self, currentInst, prevInst, prevPrevInst):
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
                   if(self.debugMode == 1):
                      print("Cycle: " +  "{:<3}".format(self.cycle)+ " |PC: "+" {:<4}".format(self.pc*4) + "NOP  Takes 1 cycle")
                      print("Cycle: " +  "{:<3}".format(self.cycle)+ " |PC: "+" {:<4}".format(self.pc*4) + "NOP  Takes 1 cycle")
                elif((ppRd == cRs) | (ppRd == cRt)):
                    self.NOPcount +=1
                    self.DataHazardSlow +=1
                    if(self.debugMode == 1):
                        print("Cycle: " +  "{:<3}".format(self.cycle)+ " |PC: "+" {:<4}".format(self.pc*4) + "NOP  Takes 1 cycle")   
            else:  #if the curent instruction is beq or bne add 3 NOPs
                self.NOPcount += 3
                self.ControlHazardSlow += 3
                if(self.debugMode == 1):
                    print("Cycle: " +  "{:<3}".format(self.cycle)+ " |PC: "+" {:<4}".format(self.pc*4) + "NOP  Taking 1 cycle")
                    print("Cycle: " +  "{:<3}".format(self.cycle)+ " |PC: "+" {:<4}".format(self.pc*4) + "NOP  Taking 1 cycle")
                    print("Cycle: " +  "{:<3}".format(self.cycle)+ " |PC: "+" {:<4}".format(self.pc*4) + "NOP  Taking 1 cycle")
        
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
                if(self.debugMode == 1):
                    print("Fast Cycle: " +  "{:<3}".format(self.cycle)+ " |PC: "+" {:<4}".format(self.pc*4) + "Control Hazard: Taken branch delay taking 1 cycle")
                if((pRd == cRs) | (pRd == cRt)): # Check if previous instruction uses same registers as the branch instruction
                    self.CompBranchHazard = True
                    self.DataHazardFast +=1
                    if(self.debugMode == 1):
                        print("Fast Cycle: " +  "{:<3}".format(self.cycle)+ " |PC: "+" {:<4}".format(self.pc*4) + "Data Hazard: Compute-branch delay taking 1 cycle")
            elif(prevInst[0:6] == "100011"): # lw-use hazard
                if((pRd == cRs) | (pRd == cRt)): # Check if the current instruction uses the same registers as the previous LW instruction
                    self.DataHazardFast +=1
                    if(self.debugMode == 1):
                        print("Fast Cycle: " +  "{:<3}".format(self.cycle)+ " |PC: "+" {:<4}".format(self.pc*4) + "Data Hazard: LW-use delay taking 1 cycle")
            
            # Still need to get output for the fast pipeline implementation
            #Keep track of which instructions are still in a 5-stage pipeline
            #Add additional information for what hazards occur and what forward path is used
            #Include total cycle count as well as how many cycles faster fast pipeline is that multi-cycle
            #and slow pipeline implementations. Also how many control/data hazards there were 

def disassemble(instructions, debugMode): 
    line = 0                          #keeps track of what line of of instrcution form the txt file is being run
    finished = False                        #is the program finished?
    reg = [0]*33                            #declare register array all initialized to 0
    mem = [0]*21                            #memory from 0x2000 ot 0x2050
    fetch = instructions[line]
    stats = Statistics(debugMode)
    #fetch = instructio i or current instruction
    prevInst = ""                   #instruction i-1
    prevPrevInst = ""               #instruction i-2
    instNameArr = []

    while(not finished):
        fetch = instructions[line]
        s = int(fetch[6:11], 2)         #read in the register - RS
        t = int(fetch[11:16], 2)        #read in ther other register - Rt
        d = int(fetch[16:21], 2)        #reads in the register RD

        if(fetch == "11111111111111111111111111111111"):
            finished = True
            stats.finalOutput(reg, mem, line)
        stats.slow_pipe(fetch, prevInst, prevPrevInst)
        #stats.fast_pipe(fetch, prevInst, prevPrevInst)
        if(fetch[0:6] == "001000"):             #addi
            reg[t] = reg[s] + twoComplement(str(fetch[16:33]))  # Rt = Rs + imm
            stats.log(fetch, "addi", 4, 1, 1, line)
            prevPrevInst = prevInst
            prevInst = fetch
            line += 1
        elif(fetch[0:6] == "001111"):           #LUI    
            reg[t] = reg[int(fetch[16:332],2)] << 16    #Rt = imm <<16
            stats.log(fetch, "lui", 4, 1, 1, line)
            prevPrevInst = prevInst
            prevInst = fetch
            line+=1
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
                reg[d] = reg[s] + reg[t]          #Rd = Rs + Rt
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
                if(reg[t] <0):
                    reg[d] = reg[t]
                else:
                    reg[d] = reg[s]^reg[t]            #Rd = Rs ^ Rt
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
                i = 0
                if(reg[d] > (2**31)-1):
                   while(reg[d] > 0 ):
                        reg[d] -= (2**(32+i))
                        i = i +1
                stats.log(fetch, "sll", 4, 1, 1, line)
                prevPrevInst = prevInst
                prevInst = fetch
                line +=1
            elif(fetch[26:32] == "000010"):         #SLR
                imm = int(fetch[21:26], 2)
                stats.log(fetch, "slr", 4, 1, 1, line)
                prevPrevInst = prevInst
                prevInst = fetch
                line +=1
                #if the value is negetive follow the opposite logic of SLL
                i = 0
                temp = reg[t]                       #Rd = Rd >> h
                while(temp < 0):
                    temp += (2**(32+i))
                    i = i + 1
                reg[d]  = temp >> imm

        elif(fetch[0:6] == "000100"):               #BEQ
            if(fetch[6:32] =="00000000001111111111111111" ): # Check if beq is at the end of the program
                stats.log(fetch, "beq", 0, 4, 4, line) # Infinite loop beq for program end
            stats.log(fetch, "beq", 3, 1, 1, line) # Regular beq instruction
            prevPrevInst = prevInst
            prevInst = fetch
            if(reg[s] == reg[t]):
                if fetch[16] == '1':
                   offset = -( 65536 - int( fetch[16:32],2 ))
                else: 
                    offset = int(fetch[16:32],2)
                line = line + offset
            if(fetch[6:32] =="00000000001111111111111111" ):
                stats.print()
                stats.finalOutput(reg, mem, line)
                finished = True
                line +=1
        elif(fetch[0:6] == "000101"):               #BNE
            stats.log(fetch, "bne", 3, 1, 1, line)
            prevPrevInst = prevInst
            prevInst = fetch
            line +=1
            if(reg[s] != reg[t]):
                if fetch[16] == '1':
                   offset = -( 65536 - int( fetch[16:32],2 ) )
                line = line + offset
        elif(fetch[0:6] == "101011"):               #SW
            stats.log(fetch, "sw", 4, 1, 1, line)
            prevPrevInst = prevInst
            prevInst = fetch
            line +=1
            offset = twoComplement(str(fetch[16:32]))           
            mem[int((offset + int(reg[s]/4) - int(8192)))] = reg[t]             #8192  = 0x2000, it indicates that our mem[0] = mem[0x2000]
                                                                                #the fist element in mem array is our memory location [0x2000]

        elif(fetch[0:6] == "100011"):               #LW
            stats.log(fetch, "lw", 5, 1, 1, line)
            prevPrevInst = prevInst
            prevInst = fetch
            line +=1
            offset = twoComplement(str(fetch[16:32]))
            reg[t] = mem[int(int(reg[s]/4) - int(8192) + offset)]               #8192  = 0x2000, it indicates that our mem[0] = mem[0x2000]
                                                                                #the fist element in mem array is our memory location [0x2000]
        else:
            finished = True
        if(not finished):
            stats.print()

def main():
   # openFile = str(input("Enter the name of the file with the extention .txt : "))
    inFile = open("case3Hex.txt", "r")       #opens the file
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
