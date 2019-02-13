// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

(NOKEY_LOOP)
@KBD
D=M
@NOKEY_LOOP
D;JEQ

//Key Pressedd
@8191
D=A
(B_LOOP)
@SCREEN
A=A+D
M=-1
@B_LOOP
D=D-1;JGE

//Screen black. Watch for key to be unpressed
(KEY_LOOP)
@KBD
D=M
@KEY_LOOP
D;JNE

//Key Unpressed
@8191
D=A
(W_LOOP)
@SCREEN
A=A+D
M=0
@W_LOOP
D=D-1;JGE

@NOKEY_LOOP
0;JMP