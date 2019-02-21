import xlrd

class ProcessExcel:

    def __init__(self, filepath):

        self.filepath = filepath

    def get_data(self):
        
        wb = xlrd.open_workbook(self.filepath)
        sheet = wb.sheet_by_index(0)
        for i in range(1, sheet.nrows):
            temp_dict = {}
            for j in range(0, sheet.ncols):
                temp_dict[sheet.cell_value(0, j).lower()] = sheet.cell_value(i, j)
            yield temp_dict
