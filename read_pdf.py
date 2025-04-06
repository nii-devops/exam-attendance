
from pprint import pprint


# import camelot
# import pandas as pd

# # Path to your PDF file
# pdf_path = "app/static/uploads/KSB_TIMETABLE_FINAL.pdf"

# # Extract tables from all pages starting from page 2 to the end
# # You can change flavor to "lattice" if your tables have clear borders, otherwise "stream" is often useful.
# tables = camelot.read_pdf(pdf_path, pages="2-end", flavor="stream")

# # Check if any tables were found
# if not tables:
#     print("No tables found on pages 2 to end.")
#     exit()

# # Concatenate all tables into one DataFrame
# combined_df = pd.concat([table.df for table in tables], ignore_index=True)

# # Optional: If your extracted tables don't include headers, you can manually set column names.
# # For example:
# #combined_df.columns = ["Day/Date", "Course Code", "Course Name", "No. of Students", "Time", "Venue", "Examiner(s)"]
# # If there are 8 columns, define 8 header names:
# combined_df.columns = ["Day/Date", "Course Code", "Course Name", "No. of Students", "Time", "Venue", "Examiner(s)", "Extra Column"]


# # Insert a heading row (as a new sheet heading or at the top of the data)
# heading = "KSB END OF 1ST SEMESTER EXAMS 2024/2025 Timetable"
# # One approach is to write the heading as a merged cell on the Excel sheet.
# output_file = "combined_timetable.xlsx"
# with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
#     # Write the DataFrame to a sheet
#     combined_df.to_excel(writer, index=False, sheet_name="Timetable", startrow=2)
    
#     # Get the workbook and sheet objects
#     workbook  = writer.book
#     worksheet = writer.sheets["Timetable"]
    
#     # Merge cells for the heading (first row) across all columns
#     num_cols = len(combined_df.columns)
#     worksheet.merge_cells(start_row=1, start_column=1, end_row=1, end_column=num_cols)
#     cell = worksheet.cell(row=1, column=1)
#     cell.value = heading
#     cell.style = 'Headline 1'
    
# print(f"Excel file created successfully: {output_file}")



session_data = [
  {'name': 'Day 1 - Session 1 (Saturday)', 'start_time': '8:30:00', 'end_time': '10:30:00', 'day': 'Day 1'},
{'name': 'Day 1 - Session 2 (Saturday)', 'start_time': '12:00:00', 'end_time': '14:00:00', 'day': 'Day 1'},
{'name': 'Day 1 - Session 3 (Saturday)', 'start_time': '15:30:00', 'end_time': '17:30:00', 'day': 'Day 1'},
{'name': 'Day 2 - Session 1 (Sunday)', 'start_time': '8:30:00', 'end_time': '10:30:00', 'day': 'Day 2'},
{'name': 'Day 2 - Session 2 (Sunday)', 'start_time': '12:00:00', 'end_time': '14:00:00', 'day': 'Day 2'},
{'name': 'Day 2 - Session 3 (Sunday)', 'start_time': '15:30:00', 'end_time': '17:30:00', 'day': 'Day 2'},
{'name': 'Day 3 - Session 1 (Monday)', 'start_time': '8:30:00', 'end_time': '10:30:00', 'day': 'Day 3'},
{'name': 'Day 3 - Session 2 (Monday)', 'start_time': '12:00:00', 'end_time': '14:00:00', 'day': 'Day 3'},
{'name': 'Day 3 - Session 3 (Monday)', 'start_time': '15:30:00', 'end_time': '17:30:00', 'day': 'Day 3'},
{'name': 'Day 4 - Session 1 (Tuesday)', 'start_time': '8:30:00', 'end_time': '10:30:00', 'day': 'Day 4'},
{'name': 'Day 4 - Session 2 (Tuesday)', 'start_time': '12:00:00', 'end_time': '14:00:00', 'day': 'Day 4'},
{'name': 'Day 4 - Session 3 (Tuesday)', 'start_time': '15:30:00', 'end_time': '17:30:00', 'day': 'Day 4'},
{'name': 'Day 5 - Session 1 (Wednesday)', 'start_time': '8:30:00', 'end_time': '10:30:00', 'day': 'Day 5'},
{'name': 'Day 5 - Session 2 (Wednesday)', 'start_time': '12:00:00', 'end_time': '14:00:00', 'day': 'Day 5'},
{'name': 'Day 5 - Session 3 (Wednesday)', 'start_time': '15:30:00', 'end_time': '17:30:00', 'day': 'Day 5'},
{'name': 'Day 6 - Session 1 (Thursday)', 'start_time': '8:30:00', 'end_time': '10:30:00', 'day': 'Day 6'},
{'name': 'Day 6 - Session 2 (Thursday)', 'start_time': '12:00:00', 'end_time': '14:00:00', 'day': 'Day 6'},
{'name': 'Day 6 - Session 3 (Thursday)', 'start_time': '15:30:00', 'end_time': '17:30:00', 'day': 'Day 6'},
{'name': 'Day 7 - Session 1 (Friday)', 'start_time': '8:30:00', 'end_time': '10:30:00', 'day': 'Day 7'},
{'name': 'Day 7 - Session 2 (Friday)', 'start_time': '12:00:00', 'end_time': '14:00:00', 'day': 'Day 7'},
{'name': 'Day 7 - Session 3 (Friday)', 'start_time': '15:30:00', 'end_time': '17:30:00', 'day': 'Day 7'},
{'name': 'Day 8 - Session 1 (Saturday)', 'start_time': '8:30:00', 'end_time': '10:30:00', 'day': 'Day 8'},
{'name': 'Day 8 - Session 2 (Saturday)', 'start_time': '12:00:00', 'end_time': '14:00:00', 'day': 'Day 8'},
{'name': 'Day 8 - Session 3 (Saturday)', 'start_time': '15:30:00', 'end_time': '17:30:00', 'day': 'Day 8'},
{'name': 'Day 9 - Session 1 (Sunday)', 'start_time': '8:30:00', 'end_time': '10:30:00', 'day': 'Day 9'},
{'name': 'Day 9 - Session 2 (Sunday)', 'start_time': '12:00:00', 'end_time': '14:00:00', 'day': 'Day 9'},
{'name': 'Day 9 - Session 3 (Sunday)', 'start_time': '15:30:00', 'end_time': '17:30:00', 'day': 'Day 9'},
{'name': 'Day 10 - Session 1 (Monday)', 'start_time': '8:30:00', 'end_time': '10:30:00', 'day': 'Day 10'},
{'name': 'Day 10 - Session 2 (Monday)', 'start_time': '12:00:00', 'end_time': '14:00:00', 'day': 'Day 10'},
{'name': 'Day 10 - Session 3 (Monday)', 'start_time': '15:30:00', 'end_time': '17:30:00', 'day': 'Day 10'},
{'name': 'Day 11 - Session 1 (Tuesday)', 'start_time': '8:30:00', 'end_time': '10:30:00', 'day': 'Day 11'},
{'name': 'Day 11 - Session 2 (Tuesday)', 'start_time': '12:00:00', 'end_time': '14:00:00', 'day': 'Day 11'},
{'name': 'Day 11 - Session 3 (Tuesday)', 'start_time': '15:30:00', 'end_time': '17:30:00', 'day': 'Day 11'},
{'name': 'Day 12 - Session 1 (Wednesday)', 'start_time': '8:30:00', 'end_time': '10:30:00', 'day': 'Day 12'},
{'name': 'Day 12 - Session 2 (Wednesday)', 'start_time': '12:00:00', 'end_time': '14:00:00', 'day': 'Day 12'},
{'name': 'Day 12 - Session 3 (Wednesday)', 'start_time': '15:30:00', 'end_time': '17:30:00', 'day': 'Day 12'},
{'name': 'Day 13 - Session 1 (Thursday)', 'start_time': '8:30:00', 'end_time': '10:30:00', 'day': 'Day 13'},
{'name': 'Day 13 - Session 2 (Thursday)', 'start_time': '12:00:00', 'end_time': '14:00:00', 'day': 'Day 13'},
{'name': 'Day 13 - Session 3 (Thursday)', 'start_time': '15:30:00', 'end_time': '17:30:00', 'day': 'Day 13'},
{'name': 'Day 14 - Session 1 (Friday)', 'start_time': '8:30:00', 'end_time': '10:30:00', 'day': 'Day 14'},
{'name': 'Day 14 - Session 2 (Friday)', 'start_time': '12:00:00', 'end_time': '14:00:00', 'day': 'Day 14'},
{'name': 'Day 14 - Session 3 (Friday)', 'start_time': '15:30:00', 'end_time': '17:30:00', 'day': 'Day 14'},
{'name': 'Day 15 - Session 1 (Saturday)', 'start_time': '8:30:00', 'end_time': '10:30:00', 'day': 'Day 15'},
{'name': 'Day 15 - Session 2 (Saturday)', 'start_time': '12:00:00', 'end_time': '14:00:00', 'day': 'Day 15'},
{'name': 'Day 15 - Session 3 (Saturday)', 'start_time': '15:30:00', 'end_time': '17:30:00', 'day': 'Day 15'},
{'name': 'Day 16 - Session 1 (Sunday)', 'start_time': '8:30:00', 'end_time': '10:30:00', 'day': 'Day 16'},
{'name': 'Day 16 - Session 2 (Sunday)', 'start_time': '12:00:00', 'end_time': '14:00:00', 'day': 'Day 16'},
{'name': 'Day 16 - Session 3 (Sunday)', 'start_time': '15:30:00', 'end_time': '17:30:00', 'day': 'Day 16'},
{'name': 'Day 17 - Session 1 (Monday)', 'start_time': '8:30:00', 'end_time': '10:30:00', 'day': 'Day 17'},
{'name': 'Day 17 - Session 2 (Monday)', 'start_time': '12:00:00', 'end_time': '14:00:00', 'day': 'Day 17'},
{'name': 'Day 17 - Session 3 (Monday)', 'start_time': '15:30:00', 'end_time': '17:30:00', 'day': 'Day 17'},
{'name': 'Day 18 - Session 1 (Tuesday)', 'start_time': '8:30:00', 'end_time': '10:30:00', 'day': 'Day 18'},
{'name': 'Day 18 - Session 2 (Tuesday)', 'start_time': '12:00:00', 'end_time': '14:00:00', 'day': 'Day 18'},
{'name': 'Day 18 - Session 3 (Tuesday)', 'start_time': '15:30:00', 'end_time': '17:30:00', 'day': 'Day 18'},
{'name': 'Day 19 - Session 1 (Wednesday)', 'start_time': '8:30:00', 'end_time': '10:30:00', 'day': 'Day 19'},
{'name': 'Day 19 - Session 2 (Wednesday)', 'start_time': '12:00:00', 'end_time': '14:00:00', 'day': 'Day 19'},
{'name': 'Day 19 - Session 3 (Wednesday)', 'start_time': '15:30:00', 'end_time': '17:30:00', 'day': 'Day 19'},
{'name': 'Day 20 - Session 1 (Thursday)', 'start_time': '8:30:00', 'end_time': '10:30:00', 'day': 'Day 20'},
{'name': 'Day 20 - Session 2 (Thursday)', 'start_time': '12:00:00', 'end_time': '14:00:00', 'day': 'Day 20'},
{'name': 'Day 20 - Session 3 (Thursday)', 'start_time': '15:30:00', 'end_time': '17:30:00', 'day': 'Day 20'},
{'name': 'Day 21 - Session 1 (Friday)', 'start_time': '8:30:00', 'end_time': '10:30:00', 'day': 'Day 21'},
{'name': 'Day 21 - Session 2 (Friday)', 'start_time': '12:00:00', 'end_time': '14:00:00', 'day': 'Day 21'},
{'name': 'Day 21 - Session 3 (Friday)', 'start_time': '15:30:00', 'end_time': '17:30:00', 'day': 'Day 21'},
]

from datetime import datetime, timedelta

# Start date as a datetime object
current_date = datetime.strptime("05-04-2025", "%d-%m-%Y")
prev_day = None

for item in session_data:
    # If this is the first item or the day has changed, update current_date
    if prev_day is None or item["day"] != prev_day:
        # For the first item, or when the day number changes, set the new date.
        # (For the first item, current_date remains "05-04-2025")
        if prev_day is not None:
            current_date += timedelta(days=1)
        prev_day = item["day"]
    # Add the formatted date string to the dictionary
    item["date"] = current_date.strftime("%d-%m-%Y")

# To display the complete updated data:
# for item in session_data:
pprint(session_data)


#date = datetime.strptime(date, '%d-%m-%Y').date()
#print(date)

ay = '2024/2025 Academic year'
#print(ay.upper())

