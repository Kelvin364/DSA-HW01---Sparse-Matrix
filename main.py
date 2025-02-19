class SparseMatrix:
    """Simple sparse matrix implementation"""
    
    def __init__(self, matrix_file_path=None, num_rows=0, num_cols=0):
        # Initialize with empty dictionary to store non-zero elements
        self.elements = {}
        
        # Create matrix from file
        if matrix_file_path:
            try:
                with open(matrix_file_path, 'r') as file:
                    # Read and process non-empty lines
                    lines = []
                    for line in file:
                        if line.strip():
                            lines.append(line.strip())
                    
                    # Get dimensions from first two lines
                    rows_line = lines[0]
                    cols_line = lines[1]
                    
                    # Parse rows
                    if not rows_line.startswith('rows='):
                        raise ValueError("Input file has wrong format")
                    self.num_rows = int(rows_line.split('=')[1])
                    
                    # Parse columns
                    if not cols_line.startswith('cols='):
                        raise ValueError("Input file has wrong format")
                    self.num_cols = int(cols_line.split('=')[1])
                    
                    # Read matrix elements
                    for i in range(2, len(lines)):
                        line = lines[i]
                        
                        # Check format (row, col, value)
                        if not (line.startswith('(') and line.endswith(')')):
                            raise ValueError("Input file has wrong format")
                            
                        # Remove parentheses and split by comma
                        content = line[1:-1]
                        parts = [part.strip() for part in content.split(',')]
                        
                        if len(parts) != 3:
                            raise ValueError("Input file has wrong format")
                            
                        # Convert to integers
                        try:
                            row = int(parts[0])
                            col = int(parts[1])
                            value = int(parts[2])
                        except ValueError:
                            raise ValueError("Input file has wrong format")
                            
                        # Store non-zero elements
                        if value != 0:
                            self.elements[(row, col)] = value
            except Exception as e:
                # Catch any other exceptions and raise with clear message
                raise ValueError(f"Input file has wrong format: {str(e)}")
        else:
            self.num_rows = num_rows
            self.num_cols = num_cols
    def get_element(self, row, col):
        """Get element at specified position"""
        if row < 0 or row >= self.num_rows or col < 0 or col >= self.num_cols:
            raise IndexError("Matrix indices out of bounds")
            
        # Return 0 if element not found
        return self.elements.get((row, col), 0)
    
    def set_element(self, row, col, value):
        """Set element at specified position"""
        if row < 0 or row >= self.num_rows or col < 0 or col >= self.num_cols:
            raise IndexError("Matrix indices out of bounds")
            
        if value == 0:
            # Remove zero elements to save memory
            if (row, col) in self.elements:
                del self.elements[(row, col)]
        else:
            self.elements[(row, col)] = value
    
    def add(self, other):
        """Add two matrices"""
        # Check dimensions
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError("Matrix dimensions must match for addition")
            
        # Create result matrix
        result = SparseMatrix(num_rows=self.num_rows, num_cols=self.num_cols)
        
        # Copy all elements from first matrix
        for (row, col), value in self.elements.items():
            result.elements[(row, col)] = value
            
        # Add elements from second matrix
        for (row, col), value in other.elements.items():
            if (row, col) in result.elements:
                result.elements[(row, col)] += value
                # Remove if sum is zero
                if result.elements[(row, col)] == 0:
                    del result.elements[(row, col)]
            else:
                result.elements[(row, col)] = value
                
        return result
    
    def subtract(self, other):
        """Subtract second matrix from first"""
        # Check dimensions
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError("Matrix dimensions must match for subtraction")
            
        # Create result matrix
        result = SparseMatrix(num_rows=self.num_rows, num_cols=self.num_cols)
        
        # Copy all elements from first matrix
        for (row, col), value in self.elements.items():
            result.elements[(row, col)] = value
            
        # Subtract elements from second matrix
        for (row, col), value in other.elements.items():
            if (row, col) in result.elements:
                result.elements[(row, col)] -= value
                # Remove if difference is zero
                if result.elements[(row, col)] == 0:
                    del result.elements[(row, col)]
            else:
                result.elements[(row, col)] = -value
                
        return result
    
    def multiply(self, other):
        """Multiply two matrices"""
        # Check dimensions for matrix multiplication
        if self.num_cols != other.num_rows:
            raise ValueError("Number of columns in first matrix must equal number of rows in second matrix")
            
        # Create result matrix
        result = SparseMatrix(num_rows=self.num_rows, num_cols=other.num_cols)
        
        # Perform multiplication only for non-zero elements
        for (row1, col1), val1 in self.elements.items():
            for (row2, col2), val2 in other.elements.items():
                if col1 == row2:
                    # Calculate product and add to result
                    product = val1 * val2
                    pos = (row1, col2)
                    
                    if pos in result.elements:
                        result.elements[pos] += product
                    else:
                        result.elements[pos] = product
                        
                    # Remove if result is zero
                    if result.elements[pos] == 0:
                        del result.elements[pos]
        
        return result
    
    def save_to_file(self, filename):
        """Save matrix to file"""
        with open(filename, 'w') as file:
            # Write dimensions
            file.write(f"rows={self.num_rows}\n")
            file.write(f"cols={self.num_cols}\n")
            
            # Write non-zero elements
            for (row, col), value in sorted(self.elements.items()):
                file.write(f"({row}, {col}, {value})\n")
    def main():
    """Main function to handle matrix operations"""
    try:
        # Get operation type
        print("Matrix Operations:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        choice = input("Enter your choice (1-3): ")
        
        operations = {
            "1": "add",
            "2": "subtract", 
            "3": "multiply"
        }
        
        if choice not in operations:
            print("Invalid choice. Please enter 1, 2 or 3.")
            return
            
        operation = operations[choice]
        
        # Get file paths
        matrix1_file = input("Enter first matrix file path: ")
        matrix2_file = input("Enter second matrix file path: ")
        output_file = input("Enter output file path: ")
        
        # Load matrices
        try:
            matrix1 = SparseMatrix(matrix1_file)
            matrix2 = SparseMatrix(matrix2_file)
            
            # Perform selected operation
            if operation == "add":
                result = matrix1.add(matrix2)
            elif operation == "subtract":
                result = matrix1.subtract(matrix2)
            else:  # multiply
                result = matrix1.multiply(matrix2)
                
            # Save result
            result.save_to_file(output_file)
            print(f"Operation completed successfully. Result saved to {output_file}")
            
        except FileNotFoundError as e:
            print(f"Error: File not found")
        except ValueError as e:
            print(f"Error: {e}")
            
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
