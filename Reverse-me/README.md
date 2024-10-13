# Cybersecurity Piscine: Reverse Engineering Project

## Summary

This project is designed to introduce you to the art of **Reverse Engineering**. The primary objective is to analyze binary programs (executables) without access to their source code, understand how they work, and ultimately find the passwords required to validate them. You will also gain experience in **patching binaries** to alter their behavior.

---

## Project Structure

1. **Mandatory Part**
   - Reverse 2 out of 3 provided binary programs.
   - Write a C program that replicates the algorithm of the binaries you analyze.
   - For each binary:
     - Include a `password` file containing the password to validate the binary.
     - Include a `source.c` file representing the logic of the binary in C.
   - Organize your work in folders named after the difficulty of the binary.

2. **Bonus Part**
   - Patch each binary to accept any password.
   - Explain the patching method and provide documentation justifying your changes.
   - No function overrides or cheating with `LD_PRELOAD` or similar tricks.

3. **Submission**
   - Submit your work through a Git repository. Only the content in your repository will be evaluated.

---

## Concepts and Tools You'll Need

### 1. **Binary Analysis & Reverse Engineering**
   - **Objective**: Learn to analyze how binary executables work by breaking them down and understanding their internal logic.
   - **Tools**:
     - [IDA Pro](https://www.hex-rays.com/ida-pro/) - The industry-standard disassembler for reverse engineering.
     - [GDB (GNU Debugger)](https://sourceware.org/gdb/) - A debugger to trace binary execution and inspect memory.
     - [objdump](https://linux.die.net/man/1/objdump) - Command-line tool for disassembling binaries.
   - **Learning Resources**:
     - Book: *Practical Reverse Engineering* by Bruce Dang.
     - [Open Security Training - Reverse Engineering](https://opensecuritytraining.info/IntroX86.html).

### 2. **Assembly Language**
   - **Objective**: Gain familiarity with assembly language, since reverse engineering often involves analyzing machine code.
   - **Learning Resources**:
     - Book: *Programming from the Ground Up* by Jonathan Bartlett.
     - [x86 Assembly Tutorial](https://cs.lmu.edu/~ray/notes/x86assembly/).
     - Tool: [NASM Assembler](https://nasm.us/) to write and test assembly code.

### 3. **GDB Debugging**
   - **Objective**: Learn to use GDB to set breakpoints, examine memory, and step through the execution of a binary.
   - **Learning Resources**:
     - [GDB Official Documentation](https://sourceware.org/gdb/current/onlinedocs/gdb/).
     - [GDB Beginner Tutorial](https://www.cs.cmu.edu/~gilpin/tutorial/).
     - Video: [GDB Debugger Basics](https://www.youtube.com/watch?v=PorfLSr3DDI).

### 4. **C Programming**
   - **Objective**: Write a C program that mimics the logic of the binary executable.
   - **Tools**: Use GCC for compiling C programs and `valgrind` to check for memory issues.
   - **Learning Resources**:
     - Book: *The C Programming Language* by Brian Kernighan and Dennis Ritchie.
     - [Learn C Programming](https://www.learn-c.org/).
     - [CS50 Introduction to C](https://cs50.harvard.edu/).

### 5. **Binary Patching**
   - **Objective**: Modify the binary to bypass password checks or change its functionality.
   - **Tools**:
     - [Radare2](https://radare.org/n/) - An open-source reverse engineering framework.
     - Hex editors for manual binary patching.
   - **Learning Resources**:
     - [Binary Patching with Radare2](https://0x00sec.org/t/radare2-tutorial-series-3-binary-patching/3276).
     - Video: [Binary Patching Using GDB](https://www.youtube.com/watch?v=ZVfXGZdfk-c).

### 6. **Linux Environment**
   - **Objective**: Set up and use a Linux environment to run and analyze binaries.
   - **Tools**: Use a virtual machine with Linux or a dedicated Linux environment.
   - **Learning Resources**:
     - [Linux Command Line Basics](https://linuxjourney.com/lesson/command-line-basics).
     - [edX - Introduction to Linux](https://www.edx.org/course/introduction-to-linux).

---

## Key Commands and Usage

- **GDB Basic Commands**:
  - `gdb ./binary_name` – Launch GDB with the target binary.
  - `break main` – Set a breakpoint at the `main` function.
  - `run` – Start running the program in GDB.
  - `next` – Step over the next instruction.
  - `info registers` – View register values.
  - `x/20x $esp` – Examine 20 hexadecimal values at the stack pointer.
  
- **Useful Linux Commands**:
  - `objdump -d binary_name` – Disassemble a binary to view its assembly code.
  - `strings binary_name` – Extract readable strings from the binary (can reveal passwords or hints).

---

## Project Example Layout

```
Reverse-me/
│
├── level1/              # Easy difficulty binary folder
│   ├── password         # Discovered password file
│   └── source.c         # C program replicating the binary's logic
│
├── level2/              # Medium difficulty binary folder
│   ├── password
│   └── source.c
│
├── patch/               # Folder for binary patches
│   └── explanation.txt  # Document explaining how each patch was applied
│
└── README.md            # This README file
```

---

## Bonus: Patching Binaries

To achieve a perfect submission, patch each binary to accept any password. You must:
- Modify the binary in such a way that it always validates successfully, regardless of the input password.
- **Documentation**: Explain your modifications and provide a step-by-step guide on how the patch works.

---

## Conclusion

By the end of this project, you will have learned the essential skills required for **reverse engineering** and **binary patching**. You'll have gained experience working with tools like GDB, IDA Pro, and Radare2, and you'll deepen your understanding of assembly language and low-level program analysis.
