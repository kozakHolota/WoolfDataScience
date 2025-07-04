// arythmetics.S — Обчислення: 5 + 2 - 4 = 3 (ARM64/macOS)

    .section __DATA,__data
msg:    .asciz "Result: \n"
num:    .byte 0

    .section __TEXT,__text
    .globl _start

_start:
    // Обчислення: 5 + 2 - 4
    mov     x0, #5            // x0 = 5
    mov     x1, #2            // x1 = 2
    add     x2, x0, x1        // x2 = 5 + 2 = 7
    mov     x3, #4            // x3 = 4
    sub     x4, x2, x3        // x4 = 7 - 4 = 3

    // Перетворення числа x4 (3) у ASCII ('3' = 0x33)
    add     x5, x4, #0x30     // x5 = x4 + '0'

    // Зберігаємо ASCII-цифру у дані
    adrp    x6, num@PAGE
    add     x6, x6, num@PAGEOFF
    strb    w5, [x6]

    // Вивести "Result: "
    mov     x0, #1
    adrp    x1, msg@PAGE
    add     x1, x1, msg@PAGEOFF
    mov     x2, #8            // "Result: "
    mov     x16, #4
    svc     #0x80

    // Вивести цифру
    mov     x0, #1
    adrp    x1, num@PAGE
    add     x1, x1, num@PAGEOFF
    mov     x2, #1
    mov     x16, #4
    svc     #0x80

    // Вивести перевід рядка
    mov     x0, #1
    adrp    x1, msg@PAGE
    add     x1, x1, msg@PAGEOFF
    add     x1, x1, #8        // позиція \n в "Result: \n"
    mov     x2, #1
    mov     x16, #4
    svc     #0x80

    // Завершити програму
    mov     x0, #0
    mov     x16, #1
    svc     #0x80