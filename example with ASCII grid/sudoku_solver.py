import itertools
import copy

class SudokuSolver:

    ALL_NUMBERS = {1,2,3,4,5,6,7,8,9}

    def __init__(self, field):
        self._field = copy.deepcopy(field)
        self._row_sets = [set() for i in range(9)]
        self._col_sets = [set() for i in range(9)]
        self._square_sets = [[set() for j in range(3)] for i in range(3)]
        self._markers = [[set() for j in range(9)] for i in range(9)]
        self._empty_cells = self._count_empty_cells()

    
    def solve_sudoku(self):
        self._fill_initially_markers()     
        while(self._empty_cells>0):
            self._fill_sets()            
            self._fill_markers_from_sets()            
            self._fill_pointers()
            self._find_combinations()
            self._find_only_markers()
            self._populate_field()            
        return self._field
    
    def _fill_initially_markers(self):
        for row in range(9):
            for col in range(9):
                if self._field[row][col] != "":
                    continue
                self._markers[row][col] = {*SudokuSolver.ALL_NUMBERS}

    #fills the cells which have a single marker 
    def _populate_field(self):
        for row in range(9):
            for col in range(9):
                if self._field[row][col] != "":
                    continue
                if len(self._markers[row][col]) == 1:
                    self._field[row][col] = self._markers[row][col].pop()
                    self._empty_cells -= 1

    #finds the only cell, which can contain a certain number
    def _find_only_markers(self):
        self._find_only_markers_in_squares()
        self._find_only_markers_in_rows()
        self._find_only_markers_in_cols()
    
    def _find_only_markers_in_cols(self):
        for col in range(9):
            self._find_only_markers_in_col(col)

    def _find_only_markers_in_col(self,col):
        for row in range(9):
            if self._field[row][col] != "":
                continue
            self._check_cell_for_only_marker_in_col(row,col)
    
    def _check_cell_for_only_marker_in_col(self,cell_row,cell_col):
        cell_markers = {*self._markers[cell_row][cell_col]}

        for row in range(9):
            if row == cell_row or self._field[row][cell_col] != "":
                continue
            cell_markers = cell_markers.difference(self._markers[row][cell_col])

        if len(cell_markers) == 1:
            self._markers[cell_row][cell_col] = cell_markers

        for row in range(9):
            if row == cell_row or self._field[row][cell_col] != "":
                continue
            self._markers[row][cell_col] = self._markers[row][cell_col].difference(cell_markers)



    def _find_only_markers_in_rows(self):
        for row in range(9):
            self._find_only_markers_in_row(row)

    def _find_only_markers_in_row(self,row):
        for col in range(9):
            if self._field[row][col] != "":
                continue
            self._check_cell_for_only_marker_in_row(row,col)
    
    def _check_cell_for_only_marker_in_row(self,cell_row,cell_col):
        cell_markers = {*self._markers[cell_row][cell_col]}

        for col in range(9):
            if col == cell_col or self._field[cell_row][col] != "":
                continue
            cell_markers = cell_markers.difference(self._markers[cell_row][col])

        if len(cell_markers) == 1:
            self._markers[cell_row][cell_col] = cell_markers

        for col in range(9):
            if col == cell_col or self._field[cell_row][col] != "":
                continue
            self._markers[cell_row][col] = self._markers[cell_row][col].difference(cell_markers)

    def _find_only_markers_in_squares(self):
        for square_row in range(3):
            for square_col in range(3):
                self._find_only_markers_in_square(square_row,square_col)

    def _find_only_markers_in_square(self,square_row,square_col):
        for row_add in range(3):
            for col_add in range(3):
                if self._field[square_row*3+row_add][square_col*3+col_add] != "":
                    continue
                self._check_cell_for_only_marker_in_square(square_row,square_col,row_add,col_add)

    def _check_cell_for_only_marker_in_square(self,square_row,square_col,cell_row_add,cell_col_add):
        cell_markers = {*self._markers[square_row*3+cell_row_add][square_col*3+cell_col_add]}
        for row_add in range(3):
            for col_add in range(3):
                if (row_add == cell_row_add and col_add == cell_col_add) or self._field[square_row*3+row_add][square_col*3+col_add] != "":
                    continue
                cell_markers = cell_markers.difference(self._markers[square_row*3+row_add][square_col*3+col_add])

        if len(cell_markers) == 1:
            self._markers[square_row*3+cell_row_add][square_col*3+cell_col_add] = cell_markers
        for row_add in range(3):
            for col_add in range(3):
                if (row_add == cell_row_add and col_add == cell_col_add) or self._field[square_row*3+row_add][square_col*3+col_add] != "":
                    continue
                self._markers[square_row*3+row_add][square_col*3+col_add] = self._markers[square_row*3+row_add][square_col*3+col_add].difference(cell_markers)


    #finds combinations (pairs, triplets, etc.)
    def _find_combinations(self):
        self._find_combinations_in_squares()
        self._find_combinations_in_cols()
        self._find_combinations_in_rows()

    def _find_combinations_in_squares(self):
        for square_row in range(3):
            for square_col in range(3):
                for occurrences_amount in range(2,9,1):
                    self._find_combinations_by_occurrences_in_square(occurrences_amount,square_row,square_col)

    def _find_combinations_by_occurrences_in_square(self,occurrences,square_row,square_col):
        cells_open = self._get_cells_open_for_combinations_in_square(square_row,square_col)              
        possible_combinations = list(itertools.combinations(cells_open,occurrences))

        for combination in possible_combinations:
            combination_markers = set()
            for index in combination:
                row_add = index // 3
                col_add = index - row_add * 3
                combination_markers = combination_markers.union(self._markers[square_row*3+row_add][square_col*3+col_add])
                
            for index in cells_open:                
                if index in combination: 
                    continue
                row_add = index // 3
                col_add = index - row_add * 3
                combination_markers = combination_markers - self._markers[square_row * 3 + row_add][square_col * 3 + col_add]
            if len(combination_markers) == occurrences:

                for index in range(9):
                    row_add = index // 3
                    col_add = index - row_add * 3
                    if self._field[square_row*3+row_add][square_col*3+col_add] != "":
                        continue
                    if index in combination:
                        self._markers[square_row*3+row_add][square_col*3+col_add] = self._markers[square_row*3+row_add][square_col*3+col_add].intersection(combination_markers)
                    else:
                        self._markers[square_row*3+row_add][square_col*3+col_add] = self._markers[square_row*3+row_add][square_col*3+col_add].difference(combination_markers)

    def _get_cells_open_for_combinations_in_square(self,square_row,square_col):
        cells_dict = dict()
        for row_add in range(3):
            for col_add in range(3):
                cell_value = self._field[square_row*3+row_add][square_col*3+col_add]
                if cell_value != "":
                    continue
                cells_dict[row_add*3+col_add] = {*self._markers[square_row*3 + row_add][square_col*3 + col_add]}
        return cells_dict  

    def _find_combinations_in_cols(self):
        for col in range(9):
            for occurrences_amount in range(2,9,1):
                self._find_combinations_by_occurrences_in_col(occurrences_amount,col)

    def _find_combinations_by_occurrences_in_col(self,occurrences,col):
        cells_open = self._get_cells_open_for_combinations_in_col(col)
        possible_combinations = list(itertools.combinations(cells_open,occurrences))

        for combination in possible_combinations:
            combination_markers = set()
            for index in combination:
                combination_markers = combination_markers.union(self._markers[index][col])
                #do tuk
            for index in cells_open:
                if index in combination: 
                    continue
                combination_markers = combination_markers - self._markers[index][col]
            if len(combination_markers) == occurrences:

                for row in range(9):
                    if self._field[row][col] != "":
                        continue
                    if row in combination:
                        self._markers[row][col] = self._markers[row][col].intersection(combination_markers)
                    else:
                        self._markers[row][col] = self._markers[row][col].difference(combination_markers)

    def _get_cells_open_for_combinations_in_col(self,col):
        cells_dict = dict()
        for row in range(9):
            cell_value = self._field[row][col]
            if cell_value != "":
                continue
            cells_dict[row] = {*self._markers[row][col]}
        return cells_dict  

    def _find_combinations_in_rows(self):           
        for row in range(9):
            for occurrences_amount in range(2,9,1):
                self._find_combinations_by_occurrences_in_row(occurrences_amount,row)


    def _find_combinations_by_occurrences_in_row(self,occurrences,row):
        cells_open = self._get_cells_open_for_combinations_in_row(row)
        possible_combinations = list(itertools.combinations(cells_open,occurrences))

        for combination in possible_combinations:
            combination_markers = set()
            for index in combination:
                combination_markers = combination_markers.union(self._markers[row][index])
            for index in cells_open:
                if index in combination: 
                    continue
                combination_markers = combination_markers - self._markers[row][index]
            if len(combination_markers) == occurrences:
                for col in range(9):
                    if self._field[row][col] != "":
                        continue
                    if col in combination:
                        self._markers[row][col] = self._markers[row][col].intersection(combination_markers)
                    else:
                        self._markers[row][col] = self._markers[row][col].difference(combination_markers)

            
    def _get_cells_open_for_combinations_in_row(self,row):
        cells_dict = dict()
        for col in range(9):
            cell_value = self._field[row][col]
            if cell_value != "":
                continue
            cells_dict[col] = {*self._markers[row][col]}
        return cells_dict    

    #searches and fills pointing combinations
    def _fill_pointers(self):
        for y in range(3):
            for x in range(3):
                for n in range(3):
                    self._fill_horizontal_pointers(x,y,n)
                    self._fill_vertical_pointers(x,y,n)

    def _fill_horizontal_pointers(self,square_x,square_y,row_in_square):
        row_markers = set()
        
        for i in range(3):
            if self._field[square_y*3+row_in_square][square_x*3+i] != "":
                continue
            row_markers = row_markers.union(self._markers[square_y*3+row_in_square][square_x*3+i])
        
        for y in range(3):
            if y == row_in_square:
                continue
            for x in range(3):
                row_markers -= self._markers[square_y*3+y][square_x*3+x]
        
        if len(row_markers) == 0:
            return

        for other_square_x in range(3):
            if other_square_x == square_x:
                continue
            for x in range(3):
                self._markers[square_y*3+row_in_square][other_square_x*3+x] -= row_markers 

    def _fill_vertical_pointers(self,square_x,square_y,col_in_square):
        col_markers = set()
        
        for i in range(3):
            if self._field[square_y*3+i][square_x*3+col_in_square] != "":
                continue
            col_markers = col_markers.union(self._markers[square_y*3+i][square_x*3+col_in_square])
        
        for y in range(3):
            for x in range(3):
                if x == col_in_square:
                    continue
                col_markers -= self._markers[square_y*3+y][square_x*3+x]
        
        if len(col_markers) == 0:
            return

        for other_square_y in range(3):
            if other_square_y == square_y:
                continue
            for y in range(3):
                self._markers[other_square_y*3+y][square_x*3+col_in_square] -= col_markers 

    #excludes impossible markers from every cell
    def _fill_markers_from_sets(self):
        for i in range(9):
            for j in range(9):
                if self._field[i][j] != "":
                    continue
                self._markers[i][j] = self._markers[i][j].difference(set.union(self._row_sets[i],self._col_sets[j],self._square_sets[i//3][j//3]))

    #adds newly found numbers to the sets
    def _fill_sets(self):        
        for i in range(9):
            for j in range(9):
                if self._field[i][j] == "":
                    continue
                self._row_sets[i].add(self._field[i][j])
                self._col_sets[j].add(self._field[i][j])
                self._square_sets[i//3][j//3].add(self._field[i][j])

    def _count_empty_cells(self):
        empty_cells = 0
        for row in self._field:
            for col in row:
                if col == "":
                    empty_cells +=1 
        return empty_cells
