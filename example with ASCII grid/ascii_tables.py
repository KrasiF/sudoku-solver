import copy

class ASCIITable:

    WIDTH_LIMIT_DEFAULT = 8
    WIDTH_MINIMUM_DEFAULT = 1

    def __init__(self, rows_amount, cols_amount, cell_width_limit = WIDTH_LIMIT_DEFAULT, cell_width_minimum = WIDTH_MINIMUM_DEFAULT):
        self._rows_amount = rows_amount
        self._cols_amount = cols_amount
        self._width_limiter = cell_width_limit
        self._width_minimum = cell_width_minimum
        self._content = [["" for i in range(cols_amount)] for i in range(rows_amount)]

    @staticmethod
    def from_2d_list(list_2d, cell_width_limit = WIDTH_LIMIT_DEFAULT, cell_width_minimum = WIDTH_MINIMUM_DEFAULT):
        rows_amount = len(list_2d)
        cols_amount = ASCIITable._find_col_amount(list_2d)
        table_to_return = ASCIITable(rows_amount,cols_amount,cell_width_limit,cell_width_minimum)
        for row_index in range(rows_amount):
            for col_index in range(len(list_2d[row_index])):
                item = list_2d[row_index][col_index]
                table_to_return.set(col_index,row_index,item)
        return table_to_return

    @staticmethod
    def _find_col_amount(list_2d):
        max_cols_per_row = 0
        for item in list_2d:
            return max(max_cols_per_row,len(item))
        return max_cols_per_row

    def set(self,x,y,data):
        self._content[y][x] = str(data)
    
    def insert_column(self, x):
        self._cols_amount+=1
        for row in self._content:
            row.insert(x,"")

    def insert_row(self, y):
        self._rows_amount+=1
        self._content.insert(y,["" for i in range(self._cols_amount)])

    def get_ascii_table(self): 
        def draw_horizontal_border(len):
            return "{:->{width}}".format("",width=len)+"\n"

        def draw_row_with_borders(row_index,row_height_index):
            nonlocal prepared_content
            nonlocal col_max_lens
            row_output_string = ""
            for col_index in range(len(prepared_content[row_index])):
                prepared_cell = prepared_content[row_index][col_index]
                width=col_max_lens[col_index]
                if row_height_index + 1 <= len(prepared_cell):
                    row_output_string += "|" + "{:<{format_width}}".format(prepared_cell[row_height_index],format_width=width)
                else:
                    row_output_string += "|" + "{:<{format_width}}".format("",format_width=width)
            row_output_string += "|\n"
            return row_output_string

        output_string = ""
        prepared_content = self._prepare_text()        
        col_max_lens = self._get_col_max_widths(prepared_content)
        row_max_heights = self._get_row_max_heights(prepared_content)

        for row_index in range(self._rows_amount):
            output_string += draw_horizontal_border(sum(col_max_lens)+self._cols_amount+1)

            for row_height_index in range(row_max_heights[row_index]):                
                output_string += draw_row_with_borders(row_index,row_height_index)

        output_string += draw_horizontal_border(sum(col_max_lens)+self._cols_amount+1)

        return output_string

    def _get_col_max_widths(self,prepared_content):
        col_max_lens = [0 for i in range(self._cols_amount)]
        for row in prepared_content:
            for col_index in range(len(row)):
                col_max_lens[col_index] = max(col_max_lens[col_index], len(row[col_index][0]))    
                if col_max_lens[col_index] < self._width_minimum:
                    col_max_lens[col_index] = self._width_minimum
        return col_max_lens

    def _get_row_max_heights(self,prepared_content):
        max_heights = [1 for i in range(self._rows_amount)]
        for row_index in range(len(prepared_content)):
            max_height_curr_row = 1
            for col in prepared_content[row_index]:
                max_height_curr_row = max(max_height_curr_row,len(col))
            max_heights[row_index] = max_height_curr_row
        return max_heights
    
    def _prepare_text(self):  

        def listify_all_items(_to_prepare_content):
            to_prepare_content = copy.deepcopy(_to_prepare_content)
            for row_index in range(len(to_prepare_content)):
                for col_index in range(len(to_prepare_content[row_index])):
                    to_prepare_content[row_index][col_index] = [to_prepare_content[row_index][col_index]]
            return to_prepare_content

        def split_all_items_by_max_len(_to_prepare_content, width_limit):
            to_prepare_content = copy.deepcopy(_to_prepare_content)
            for i in range(len(to_prepare_content)):
                for j in range(len(to_prepare_content[i])):
                    added_lines = 0
                    while(len(to_prepare_content[i][j][added_lines]) > width_limit):
                        string_to_cut = to_prepare_content[i][j][added_lines]
                        to_prepare_content[i][j][added_lines] = string_to_cut[0:width_limit]
                        to_prepare_content[i][j].append(string_to_cut[width_limit:])
                        added_lines += 1
            return to_prepare_content

        to_prepare_content = listify_all_items(self._content)
        
        to_prepare_content = split_all_items_by_max_len(to_prepare_content, self._width_limiter)        
        
        return to_prepare_content