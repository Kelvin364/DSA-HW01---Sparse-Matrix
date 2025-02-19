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