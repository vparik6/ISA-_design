ori $8, $0, 24
addi $9, $0, 0x40
sw_loop:
sw $8, 0x2000($9)
addi $9, $9, -4
beq $9, $0, sw_done
sll $10, $8, 24
addu $10, $10, $8
sub $8, $0, $8
xor $8, $10, $8
beq $0, $0, sw_loop
sw_done:

# Z2 is the other one
#end: beq $0, $0, end

addi $13, $0, 0x40
addi $14, $0, 0x44
loop_2:
addi $8, $0, 4
addi $9, $0, 8
	loop_1:
	lw $10, 0x2000($8)
	lw $11, 0x2000($9)
	slt $12, $11, $10
	beq $12, $0, else
		sw $11, 0x2000
		lw $11, 0x2000($8)
		sw $11, 0x2000($9)
		lw $10, 0x2000
		sw $10, 0x2000($8)
	else:
	addi $8, $8, 4
	addi $9, $9, 4 
	bne $9, $14, loop_1
addi $13, $13, -4
bne $13, $0, loop_2
