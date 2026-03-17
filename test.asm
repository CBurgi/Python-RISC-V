start:
    li x3 1
    li x4 10
count_loop:
    beq x3 x4 done
    jal x1 increment
    j count_loop
increment:
    addi x3 x3 1
    jalr x0 x1 0
done:
    j done
