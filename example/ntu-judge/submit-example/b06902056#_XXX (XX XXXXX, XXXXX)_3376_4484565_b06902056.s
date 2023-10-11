.globl __start

.rodata
    division_by_zero: .string "division by zero"

.text
__start:
    # Read first operand
    li a0, 5
    ecall
    mv s0, a0
    # Read operation
    li a0, 5
    ecall
    mv s1, a0
    # Read second operand
    li a0, 5
    ecall
    mv s2, a0

###################################
#  TODO: Develop your calculator  #
#                                 #
###################################
    bne s1,x0,L1
    add s3,s0,s2
    jal x0,output
L1:
    addi x20,x0,1
    bne s1,x20,L2
    sub s3,s0,s2
    jal x0,output
L2:
    addi x20,x0,2
    bne s1,x20,L3
    mul s3,s0,s2
    jal x0,output
L3:
    addi x20,x0,3
    bne s1,x20,L4
    beq s2,x0,division_by_zero_except
    div s3,s0,s2
    jal x0,output
L4:
    addi x20,x0,4
    bne s1,x20,L5
    blt s0,s2,L40
    add s3,s2,x0
    jal x0,output
L40:
    add s3,s0,x0
    jal x0,output

L5:
    addi x20,x0,5
    bne s1,x20,L6
    addi x21,x0,1
L50:
    blt x0,s2,L51
    add s3,x0,x21
    jal x0,output
L51:
    addi s2,s2,-1
    mul x21,x21,s0
    jal x0,L50

L6:
    addi x20,x0,6
    bne s1,x20,exit
    blt s0,x0,exit
    addi x21,x0,1
L60:
    blt x0,s0,L61
    add s3,x0,x21
    jal x0,output
L61:
    mul x21,x21,s0
    addi s0,s0,-1
    jal x0,L60
    






output:
    # Output the result
    li a0, 1
    mv a1, s3
    ecall

exit:
    # Exit program(necessary)
    li a0, 10
    ecall

division_by_zero_except:
    li a0, 4
    la a1, division_by_zero
    ecall
    jal zero, exit
