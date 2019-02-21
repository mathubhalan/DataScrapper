

class Report:
    
    def __init__(self, file):
        
        self.file = file
        self.report_content = ""
        
    def generate_report_content(self, title, table_header, table_data):
        
        content = ""
        title = f"<h3>{title}</h3>\n"
        if table_data:
            for col_index in range(len(table_header)):
                content += f"\t\t\t<th>{table_header[col_index]}</th>\n"
            content = f"\t\t<tr>\n{content}\t\t</tr>\n"
            for row_index in range(len(table_data)):
                row = ""
                for col_index in range(len(table_header)):                    
                    row += f"\t\t\t<td>{table_data[row_index][col_index]}</td>\n"
                row = f"\t\t<tr>\n{row}\t\t</tr>\n"
                content += row
            self.report_content += f"""{title}\t<table border="1">\n{content}\t</table>\n<br>\n"""
        else:
            self.report_content += f"""{title}<p>No Data Found</p>\n<br>\n"""
        return self.report_content
        
    def create_html_report(self):
        
        with open(self.file, 'w') as html_file:
            html_file.write(self.report_content)
    