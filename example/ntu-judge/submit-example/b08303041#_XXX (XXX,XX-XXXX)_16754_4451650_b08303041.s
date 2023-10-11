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
    bne s1, x0 , L1
    add s3, s0, s2
    jal x0, output
    
L1: addi t0, x0, 1
    jal x0, output
    
L2: addi t0, x0, 2
    bne s1, t0, L3
    jal x0, output
    
L3: addi t0, x0, 3
    beq s2, x0, division_by_zero_except
    div s3, s0, s2
    jal x0, output
    
L4: addi t0, x0, 4
    bne s1, t0, L5
    ble s0, s2, former
    add s3, s2, x0
    jal x0, output
former:
    add s3, s0, x0
    jal x0, output
    
L5: addi t0, x0, 5
    bne s1, t0, L6
    addi t0, s2, 0
    addi s3, x0, 1 
Loop:
    beq t0, x0, output
    mul s3, s3, s0
    addi t0, t0, -1
    jal x0, Loop

    
L6: 
    addi a0, s0, 0
    jal ra, func
    addi s3, a0, 0
    jal x0, output
    
func:
    addi sp, sp, -8
    sw a0, 0(sp)
    sw ra, 4(sp)
    bge a0, t0, rec
    addi a0, x0, 1
    addi sp, sp, 8
    jalr x0, 0(ra)
rec:
    addi a0, a0, -1
    jal ra, func
    addi t0, a0, 0
    lw a0, 0(sp)
    lw ra, 4(sp)
    addi sp, sp, 8
    mul a0, a0, t0
    jalr x0, 0(ra)
    
###################################
    

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