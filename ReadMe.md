***Sparse Matrix Implementation***

This is the repository for my Data structures and algorithm Assignment
That is in  charge of parsing and processing Matrix by providing a cli for performing these operations : 
adding matrixes
addition on them (make sure they have the same dimensions)
substrcation on them (make sure they have the same dimensions)
multiplication on them
and after suggesting the putput directory 

Example:
Copyrows=8433
cols=3180
(0, 381, -694)
(0, 128, -838)
(0, 639, 857)
Usage

Clone the repository:
Copygit clone <repository-url>

Navigate to the project directory:
Copycd sparse-matrix

Run the program:
Copypython main.py

Follow the on-screen prompts to:

Select an operation (addition, subtraction, or multiplication)
Provide input file paths for the matrices
Specify the output file path



Implementation Details
The implementation uses a dictionary to store matrix elements, with tuple keys (row, col) mapping to the element values. This approach:

Only stores non-zero elements, making it memory-efficient
Provides O(1) average-case lookup time
Simplifies operations by only processing non-zero elements