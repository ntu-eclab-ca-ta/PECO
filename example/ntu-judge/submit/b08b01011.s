.globl __start

.rodata
    division_by_zero: .string "division by zero"
    unexpected_operator: .string "invalid operator"
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
    # +,0
    addi t0,x0,0
    beq s1,t0,addop
    # -,1
    addi t0,x0,1
    beq s1,t0,minusop
    # *,2
    addi t0,x0,2
    beq s1,t0,mulop
    # /,3
    addi t0,x0,3
    beq s1,t0,divop
    # min,4
    addi t0,x0,4
    beq s1,t0,minop
    # ^,5
    addi t0,x0,5
    ## init the result to 1 
    addi s3,x0,1
    beq s1,t0,powop
    # !,6
    addi t0,x0,6
    ## init the result to 1
    addi s3,x0,1
    # s4=1
    addi s4,x0,1
    beq s1,t0,fracop
    # invalid output
    beq x0,x0,invaid_op_except
    
addop:
    # +,0
    add s3,s0,s2
    beq x0,x0,output
minusop:
    # -,1
    sub s3,s0,s2
    beq x0,x0,output
mulop:
    # *,2
    mul s3,s0,s2
    beq x0,x0,output
divop:
    # /,3
    beq x0,s2,division_by_zero_except
    div s3,s0,s2
    beq x0,x0,output
minop:
    # min,4
    # t0=(s0<s2)?1:0
    slt t0,s0,s2
    addi s3,s2,0
    # if 0 means s2>=s0
    beq x0,t0,output
    addi s3,s0,0
    # if 1 means s0<s2
    beq x0,x0,output
    
powop: 
    # ^,5
    # result=result*A
    mul s3,s3,s0
    # s2--
    addi s2,s2,-1
    #continue if s2>0
    bgt s2,x0,powop
    addi s2,s2,1
    #if s2 is now 1, means origin s2>0
    bgt s2,x0,output
    # if s2 is now 0, means origin s2==0,s0^0==1
    addi s3,x0,1
    beq s2,x0,output
    
fracop:
    # !,6
    # if n<=1 return a1
    ble s0,s4,output
    # result=result*n
    mul s3,s3,s0
    # n=n-1
    addi s0,s0,-1
    # continue 
    beq x0,x0,fracop

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
invaid_op_except:
    li a0, 4
    la a1, unexpected_operator
    ecall
    jal zero, exit