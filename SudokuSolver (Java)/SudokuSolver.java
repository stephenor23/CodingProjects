public class SudokuSolver {
	
	// a 2D array of integers will be used to represent the Sudoku puzzle
	// a 0 represents an empty square
	private int[][] board;  
	
	// constructor populates the board array
	public SudokuSolver() {
		this.board = generateBoard();
	}
	
	// returns the board in its current state, as a 2D array of integers
	public int[][] getBoard(){
		return this.board;
	}
	
	// a recursive function which implements the backtracking algorithm to solve the puzzle
	public boolean solveBoard() {
		
		int[] emptyCoords = this.findEmptySpace(); // find an empty square
		int row, col;  // these will represent the coordinates of the empty square
		
		
		if (emptyCoords == null) {  // if all squares have been validly filled
			return true;  // the puzzle is solved
		}
		else {
			row = emptyCoords[0];  // the row number of the empty square
			col = emptyCoords[1];  // the column number ""
		}
		
		// increment from 1 up to and including 9, one of these values has to be correct
		// the exhaustion of this loop will lead to a false being returned, allowing the program
		// to "backtrack" and try another guess
		for (int i=1; i<10; i++) { 
			if (this.isValid(i, emptyCoords)) {
				board[row][col] = i;  	// this is a guess and will be corrected if necessary 
				if (this.solveBoard()) {  // call this same function on the board with the guess added
					return true;  		  // allowing the first call to return true and terminate
				}
				board[row][col] = 0;  // remove the guess, as it was incorrect
			}
		}
		return false;  // this notifies the preceding call that its guess was wrong
	}
	
	// returns the coordinates of the first empty space found
	public int[] findEmptySpace() {
		for (int i=0; i<board.length; i++) {  // loop through each row
			for (int j=0; j<board[0].length; j++) {  // loop through each cell in the row
				if (board[i][j] == 0) { // if the cell is empty
					return new int[] {i, j};  // return the coordinates of the empty cell
				}
			}
		}
		return null;  // there are no empty cells
	}
	
	// it's important to note that a "valid" guess here is a guess that doesn't contradict
	// the rules of the game (i.e. no same numbers in row, column, or 3x3 box) and is
	// not necessarily correct in the long run
	public boolean isValid(int newNumber, int[] coords) {
		
		// check if ROW is still valid with the given newNumber placed at the given coords
		for (int i=0; i<board.length; i++) {
			if (board[coords[0]][i] == newNumber && i != coords[1]) {
				return false;
			}
		}
		
		// check if COLUMN is still valid
		for (int i=0; i<board[0].length; i++) {
			if (board[i][coords[1]] == newNumber && i != coords[0]) {
				return false;
			}
		}
		
		// here we're using the coordinates given to find the parameters of the 3x3 box they're found in
		int box_x = coords[1]/3;
		int box_y = coords[0]/3;
		
		// check if the 3x3 BOX the coords are in will still be valid i.e. not have any recurring values
		for (int i=box_y*3; i<box_y*3+3; i++) {  // iterate through the 3x3 box
			for (int j=box_x*3; j<box_x*3+3; j++) {
				if (board[i][j] == newNumber && i != coords[0] && j != coords[1]) {
					return false;  // check if the values in the 3x3 box contradict our guess
				}
			}
		}
		
		return true;  // the guess is valid (but not necessarily correct)
		
	}
	
	// hardcoded sudoku puzzle
	public int[][] generateBoard(){
		
		int[][] board = new int[9][9];
		
		board[0] = new int[] {6, 0, 5,   0, 0, 0,   7, 0, 9};
		board[1] = new int[] {7, 3, 4,   5, 9, 8,   0, 0, 2};
		board[2] = new int[] {2, 0, 0,   7, 6, 4,   3, 0, 0};
		
		board[3] = new int[] {1, 0, 0,   0, 8, 3,   0, 0, 4};
		board[4] = new int[] {0, 4, 0,   0, 1, 0,   8, 6, 0};
		board[5] = new int[] {5, 0, 8,   4, 0, 0,   0, 0, 3};
		
		board[6] = new int[] {0, 0, 1,   0, 4, 0,   2, 0, 0};
		board[7] = new int[] {9, 0, 6,   8, 0, 1,   4, 3, 0};
		board[8] = new int[] {0, 0, 0,   2, 0, 0,   0, 0, 0};
		
		return board;
		
	}
	
	public String toString() {
		String s = "";
		for (int[] row : this.board) {
			for (int x : row) {
				s += x + " ";
			}
			s += "\n";
		}
		return s;
	}
	
	public static void main(String[] args) {
		// initialize
		SudokuSolver sudoku = new SudokuSolver();

		// display initial board
		System.out.println("Initial board: \n");
		System.out.println(sudoku);
		
		// solve
		sudoku.solveBoard();
		
		// display result
		System.out.println("\n\nCompleted board: \n");
		System.out.println(sudoku);
		
	}

}
