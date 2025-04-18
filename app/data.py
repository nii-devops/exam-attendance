from pprint import pprint
import os
from dotenv import load_dotenv



load_dotenv()  # Load environment variables

managers = os.getenv("MANAGERS", "").split(",")


semester_data = {
    'semesters':['FIRST (1ST) SEMESTER', 'SECOND (2ND) SEMESTER', 'SUPPLEMENTARY SEMESTER'],
    'exam_types': ['MID-SEMESTER EXAMS', 'END OF SEMESTER EXAMS','SUPPLEMENTARY EXAMS']
    }
  



# VENUE DATA
rooms = [
    'PG BLOCK B', 
    'PG BLOCK C',
    'PG BLOCK C - FF01',
    'PG BLOCK C - Gallery/Basement',
    'PG BLOCK D',
    'PG BLOCK D - Basement',
    'PG BLOCK D - Upper',
    'PG BLOCK E',
    'PG BLOCK F',
    'PG BLOCK F - Basement',
    'PG BLOCK F - Gallery/Basement',
    'SAARAH-MENSAH - SMA',
    'SAARAH-MENSAH - SMA Gallery',
]


session_data = [{'date': '05-04-2025',
  'day': 'Day 1',
  'end_time': '10:30:00',
  'name': 'Day 1 - Session 1 (Saturday)',
  'start_time': '8:30:00'},
 {'date': '05-04-2025',
  'day': 'Day 1',
  'end_time': '14:00:00',
  'name': 'Day 1 - Session 2 (Saturday)',
  'start_time': '12:00:00'},
 {'date': '05-04-2025',
  'day': 'Day 1',
  'end_time': '17:30:00',
  'name': 'Day 1 - Session 3 (Saturday)',
  'start_time': '15:30:00'},
 {'date': '06-04-2025',
  'day': 'Day 2',
  'end_time': '10:30:00',
  'name': 'Day 2 - Session 1 (Sunday)',
  'start_time': '8:30:00'},
 {'date': '06-04-2025',
  'day': 'Day 2',
  'end_time': '14:00:00',
  'name': 'Day 2 - Session 2 (Sunday)',
  'start_time': '12:00:00'},
 {'date': '06-04-2025',
  'day': 'Day 2',
  'end_time': '17:30:00',
  'name': 'Day 2 - Session 3 (Sunday)',
  'start_time': '15:30:00'},
 {'date': '07-04-2025',
  'day': 'Day 3',
  'end_time': '10:30:00',
  'name': 'Day 3 - Session 1 (Monday)',
  'start_time': '8:30:00'},
 {'date': '07-04-2025',
  'day': 'Day 3',
  'end_time': '14:00:00',
  'name': 'Day 3 - Session 2 (Monday)',
  'start_time': '12:00:00'},
 {'date': '07-04-2025',
  'day': 'Day 3',
  'end_time': '17:30:00',
  'name': 'Day 3 - Session 3 (Monday)',
  'start_time': '15:30:00'},
 {'date': '08-04-2025',
  'day': 'Day 4',
  'end_time': '10:30:00',
  'name': 'Day 4 - Session 1 (Tuesday)',
  'start_time': '8:30:00'},
 {'date': '08-04-2025',
  'day': 'Day 4',
  'end_time': '14:00:00',
  'name': 'Day 4 - Session 2 (Tuesday)',
  'start_time': '12:00:00'},
 {'date': '08-04-2025',
  'day': 'Day 4',
  'end_time': '17:30:00',
  'name': 'Day 4 - Session 3 (Tuesday)',
  'start_time': '15:30:00'},
 {'date': '09-04-2025',
  'day': 'Day 5',
  'end_time': '10:30:00',
  'name': 'Day 5 - Session 1 (Wednesday)',
  'start_time': '8:30:00'},
 {'date': '09-04-2025',
  'day': 'Day 5',
  'end_time': '14:00:00',
  'name': 'Day 5 - Session 2 (Wednesday)',
  'start_time': '12:00:00'},
 {'date': '09-04-2025',
  'day': 'Day 5',
  'end_time': '17:30:00',
  'name': 'Day 5 - Session 3 (Wednesday)',
  'start_time': '15:30:00'},
 {'date': '10-04-2025',
  'day': 'Day 6',
  'end_time': '10:30:00',
  'name': 'Day 6 - Session 1 (Thursday)',
  'start_time': '8:30:00'},
 {'date': '10-04-2025',
  'day': 'Day 6',
  'end_time': '14:00:00',
  'name': 'Day 6 - Session 2 (Thursday)',
  'start_time': '12:00:00'},
 {'date': '10-04-2025',
  'day': 'Day 6',
  'end_time': '17:30:00',
  'name': 'Day 6 - Session 3 (Thursday)',
  'start_time': '15:30:00'},
 {'date': '11-04-2025',
  'day': 'Day 7',
  'end_time': '10:30:00',
  'name': 'Day 7 - Session 1 (Friday)',
  'start_time': '8:30:00'},
 {'date': '11-04-2025',
  'day': 'Day 7',
  'end_time': '14:00:00',
  'name': 'Day 7 - Session 2 (Friday)',
  'start_time': '12:00:00'},
 {'date': '11-04-2025',
  'day': 'Day 7',
  'end_time': '17:30:00',
  'name': 'Day 7 - Session 3 (Friday)',
  'start_time': '15:30:00'},
 {'date': '12-04-2025',
  'day': 'Day 8',
  'end_time': '10:30:00',
  'name': 'Day 8 - Session 1 (Saturday)',
  'start_time': '8:30:00'},
 {'date': '12-04-2025',
  'day': 'Day 8',
  'end_time': '14:00:00',
  'name': 'Day 8 - Session 2 (Saturday)',
  'start_time': '12:00:00'},
 {'date': '12-04-2025',
  'day': 'Day 8',
  'end_time': '17:30:00',
  'name': 'Day 8 - Session 3 (Saturday)',
  'start_time': '15:30:00'},
 {'date': '13-04-2025',
  'day': 'Day 9',
  'end_time': '10:30:00',
  'name': 'Day 9 - Session 1 (Sunday)',
  'start_time': '8:30:00'},
 {'date': '13-04-2025',
  'day': 'Day 9',
  'end_time': '14:00:00',
  'name': 'Day 9 - Session 2 (Sunday)',
  'start_time': '12:00:00'},
 {'date': '13-04-2025',
  'day': 'Day 9',
  'end_time': '17:30:00',
  'name': 'Day 9 - Session 3 (Sunday)',
  'start_time': '15:30:00'},
 {'date': '14-04-2025',
  'day': 'Day 10',
  'end_time': '10:30:00',
  'name': 'Day 10 - Session 1 (Monday)',
  'start_time': '8:30:00'},
 {'date': '14-04-2025',
  'day': 'Day 10',
  'end_time': '14:00:00',
  'name': 'Day 10 - Session 2 (Monday)',
  'start_time': '12:00:00'},
 {'date': '14-04-2025',
  'day': 'Day 10',
  'end_time': '17:30:00',
  'name': 'Day 10 - Session 3 (Monday)',
  'start_time': '15:30:00'},
 {'date': '15-04-2025',
  'day': 'Day 11',
  'end_time': '10:30:00',
  'name': 'Day 11 - Session 1 (Tuesday)',
  'start_time': '8:30:00'},
 {'date': '15-04-2025',
  'day': 'Day 11',
  'end_time': '14:00:00',
  'name': 'Day 11 - Session 2 (Tuesday)',
  'start_time': '12:00:00'},
 {'date': '15-04-2025',
  'day': 'Day 11',
  'end_time': '17:30:00',
  'name': 'Day 11 - Session 3 (Tuesday)',
  'start_time': '15:30:00'},
 {'date': '16-04-2025',
  'day': 'Day 12',
  'end_time': '10:30:00',
  'name': 'Day 12 - Session 1 (Wednesday)',
  'start_time': '8:30:00'},
 {'date': '16-04-2025',
  'day': 'Day 12',
  'end_time': '14:00:00',
  'name': 'Day 12 - Session 2 (Wednesday)',
  'start_time': '12:00:00'},
 {'date': '16-04-2025',
  'day': 'Day 12',
  'end_time': '17:30:00',
  'name': 'Day 12 - Session 3 (Wednesday)',
  'start_time': '15:30:00'},
 {'date': '17-04-2025',
  'day': 'Day 13',
  'end_time': '10:30:00',
  'name': 'Day 13 - Session 1 (Thursday)',
  'start_time': '8:30:00'},
 {'date': '17-04-2025',
  'day': 'Day 13',
  'end_time': '14:00:00',
  'name': 'Day 13 - Session 2 (Thursday)',
  'start_time': '12:00:00'},
 {'date': '17-04-2025',
  'day': 'Day 13',
  'end_time': '17:30:00',
  'name': 'Day 13 - Session 3 (Thursday)',
  'start_time': '15:30:00'},
 {'date': '18-04-2025',
  'day': 'Day 14',
  'end_time': '10:30:00',
  'name': 'Day 14 - Session 1 (Friday)',
  'start_time': '8:30:00'},
 {'date': '18-04-2025',
  'day': 'Day 14',
  'end_time': '14:00:00',
  'name': 'Day 14 - Session 2 (Friday)',
  'start_time': '12:00:00'},
 {'date': '18-04-2025',
  'day': 'Day 14',
  'end_time': '17:30:00',
  'name': 'Day 14 - Session 3 (Friday)',
  'start_time': '15:30:00'},
 {'date': '19-04-2025',
  'day': 'Day 15',
  'end_time': '10:30:00',
  'name': 'Day 15 - Session 1 (Saturday)',
  'start_time': '8:30:00'},
 {'date': '19-04-2025',
  'day': 'Day 15',
  'end_time': '14:00:00',
  'name': 'Day 15 - Session 2 (Saturday)',
  'start_time': '12:00:00'},
 {'date': '19-04-2025',
  'day': 'Day 15',
  'end_time': '17:30:00',
  'name': 'Day 15 - Session 3 (Saturday)',
  'start_time': '15:30:00'},
 {'date': '20-04-2025',
  'day': 'Day 16',
  'end_time': '10:30:00',
  'name': 'Day 16 - Session 1 (Sunday)',
  'start_time': '8:30:00'},
 {'date': '20-04-2025',
  'day': 'Day 16',
  'end_time': '14:00:00',
  'name': 'Day 16 - Session 2 (Sunday)',
  'start_time': '12:00:00'},
 {'date': '20-04-2025',
  'day': 'Day 16',
  'end_time': '17:30:00',
  'name': 'Day 16 - Session 3 (Sunday)',
  'start_time': '15:30:00'},
 {'date': '21-04-2025',
  'day': 'Day 17',
  'end_time': '10:30:00',
  'name': 'Day 17 - Session 1 (Monday)',
  'start_time': '8:30:00'},
 {'date': '21-04-2025',
  'day': 'Day 17',
  'end_time': '14:00:00',
  'name': 'Day 17 - Session 2 (Monday)',
  'start_time': '12:00:00'},
 {'date': '21-04-2025',
  'day': 'Day 17',
  'end_time': '17:30:00',
  'name': 'Day 17 - Session 3 (Monday)',
  'start_time': '15:30:00'},
 {'date': '22-04-2025',
  'day': 'Day 18',
  'end_time': '10:30:00',
  'name': 'Day 18 - Session 1 (Tuesday)',
  'start_time': '8:30:00'},
 {'date': '22-04-2025',
  'day': 'Day 18',
  'end_time': '14:00:00',
  'name': 'Day 18 - Session 2 (Tuesday)',
  'start_time': '12:00:00'},
 {'date': '22-04-2025',
  'day': 'Day 18',
  'end_time': '17:30:00',
  'name': 'Day 18 - Session 3 (Tuesday)',
  'start_time': '15:30:00'},
 {'date': '23-04-2025',
  'day': 'Day 19',
  'end_time': '10:30:00',
  'name': 'Day 19 - Session 1 (Wednesday)',
  'start_time': '8:30:00'},
 {'date': '23-04-2025',
  'day': 'Day 19',
  'end_time': '14:00:00',
  'name': 'Day 19 - Session 2 (Wednesday)',
  'start_time': '12:00:00'},
 {'date': '23-04-2025',
  'day': 'Day 19',
  'end_time': '17:30:00',
  'name': 'Day 19 - Session 3 (Wednesday)',
  'start_time': '15:30:00'},
 {'date': '24-04-2025',
  'day': 'Day 20',
  'end_time': '10:30:00',
  'name': 'Day 20 - Session 1 (Thursday)',
  'start_time': '8:30:00'},
 {'date': '24-04-2025',
  'day': 'Day 20',
  'end_time': '14:00:00',
  'name': 'Day 20 - Session 2 (Thursday)',
  'start_time': '12:00:00'},
 {'date': '24-04-2025',
  'day': 'Day 20',
  'end_time': '17:30:00',
  'name': 'Day 20 - Session 3 (Thursday)',
  'start_time': '15:30:00'},
 {'date': '25-04-2025',
  'day': 'Day 21',
  'end_time': '10:30:00',
  'name': 'Day 21 - Session 1 (Friday)',
  'start_time': '8:30:00'},
 {'date': '25-04-2025',
  'day': 'Day 21',
  'end_time': '14:00:00',
  'name': 'Day 21 - Session 2 (Friday)',
  'start_time': '12:00:00'},
 {'date': '25-04-2025',
  'day': 'Day 21',
  'end_time': '17:30:00',
  'name': 'Day 21 - Session 3 (Friday)',
  'start_time': '15:30:00'}]


staff_titles = ['Rev. Prof.', 'Prof.', 'Prof. (Mrs.)', 'Dr.', 'Dr. (Mrs.)', 'Mr.', 'Mrs.', 'Ms.', 'Miss', ]

titles  = (
    ('---', '---'),
    ('Rev Prof.', 'Rev. Prof.'),
    ('Prof.', 'Prof.'),
    ('Prof. (Mrs.)', 'Prof. (Mrs.)'),
    ('Dr.', 'Dr.'),
    ('Dr. (Mrs.)', 'Dr. (Mrs.)'),
    ('Mr.', 'Mr.'),
    ('Mrs.', 'Mrs.'),
    ('Ms.', 'Ms.'),
    ('Miss', 'Miss')
)


it_staff = ['ACQUAH Charity Mensima', 
                'AMANKWAH Gideon Baffour (Mr.)', 
                'ADU-ASSIFU Aaron Offei', 
                'AYAABA Ebenezer', 
                'AKOTO Hanson',
                'TONON Abdul-Shafiu Mahmud', 
                'ALI Abubakar Sadik', 
                'GHARTEY Rolland Evans', 
                'AMOAH Raymond Kofi', 
                'HINSON Ivy Maame Efua', 
                'ABDULAI Hamdiya Pognaa',
                'AMANKWAA Nathan Kojo Kutin', 
                'MENSAH Jonathan', 
                'AMPOFO Alberta Twumasi', 
                'OWUSU Randy', 
                'ARTHUR David Kelvin', 
                'ANTWIWAA Rosemond',
                'AFARI Sandra Ntoni', 
                'ACQUAH Charity Mensima', 
                'NTIM Anthony Twumasi',
                'SARKODIE Akwasi Boateng'
                ]


student_attendants = ['ACQUAH Charity Mensima', 
                'AMANKWAH Gideon Baffour (Mr.)', 
                'ADU-ASSIFU Aaron Offei', 
                'AYAABA Ebenezer', 
                'AKOTO Hanson',
                'TONON Abdul-Shafiu Mahmud', 
                'ALI Abubakar Sadik',
                'AMOAH Raymond Kofi', 
                'HINSON Ivy Maame Efua', 
                'ABDULAI Hamdiya Pognaa',
                'AMANKWAA Nathan Kojo Kutin', 
                'MENSAH Jonathan', 
                'AMPOFO Alberta Twumasi', 
                'OWUSU Randy', 
                'ARTHUR David Kelvin', 
                'ANTWIWAA Rosemond',
                'AFARI Sandra Ntoni', 
                'ACQUAH Charity Mensima', 
                'NTIM Anthony Twumasi',
                'SARKODIE Akwasi Boateng'
                ]



biometric_staff = [
    {'department': 'KNUST School of Business',
  'name': 'ACQUAH Charity Mensima',
  'staff_category': 'Senior Staff'},
 {'department': "Dean's Office, Faculty of Arts",
  'name': 'AMANKWAH Gideon Baffour (Mr.)',
  'staff_category': 'Senior Staff'},
 {'department': 'UITS',
  'name': 'ADU-ASSIFU Aaron Offei',
  'staff_category': 'Senior Staff'},
 {'department': 'UITS',
  'name': 'AYAABA Ebenezer',
  'staff_category': 'Senior Staff'},
 {'department': 'UITS',
  'name': 'AKOTO Hanson',
  'staff_category': 'Senior Staff'},
 {'department': 'UITS',
  'name': 'TONON Abdul-Shafiu Mahmud',
  'staff_category': 'Senior Staff'},
 {'department': 'UITS',
  'name': 'ALI Abubakar Sadik',
  'staff_category': 'Senior Staff'},
 {'department': 'UITS',
  'name': 'GHARTEY Rolland Evans',
  'staff_category': 'Senior Staff'},
 {'department': 'KNUST School of Business',
  'name': 'AMOAH Raymond Kofi',
  'staff_category': 'Senior Staff'},
 {'department': 'KNUST School of Business',
  'name': 'HINSON Ivy Maame Efua',
  'staff_category': 'Senior Staff'},
 {'department': 'KNUST School of Business',
  'name': 'ABDULAI Hamdiya Pognaa',
  'staff_category': 'Senior Staff'},
 {'department': 'KNUST School of Business',
  'name': 'AMANKWAA Nathan Kojo Kutin',
  'staff_category': 'Senior Staff'},
 {'department': 'KNUST School of Business',
  'name': 'MENSAH Jonathan',
  'staff_category': 'Senior Staff'},
 {'department': 'KNUST School of Business',
  'name': 'AMPOFO Alberta Twumasi',
  'staff_category': 'Senior Staff'},
 {'department': 'KNUST School of Business',
  'name': 'OWUSU Randy',
  'staff_category': 'Senior Staff'},
 {'department': 'KNUST School of Business',
  'name': 'ARTHUR David Kelvin',
  'staff_category': 'Senior Staff'},
 {'department': 'KNUST School of Business',
  'name': 'ANTWIWAA Rosemond',
  'staff_category': 'Senior Staff'},
 {'department': 'KNUST School of Business',
  'name': 'AFARI Sandra Ntoni',
  'staff_category': 'Senior Staff'},
 {'department': 'KNUST School of Business',
  'name': 'ACQUAH Charity Mensima',
  'staff_category': 'Senior Staff'},
 {'department': 'UITS',
  'name': 'SARKODIE Akwasi Boateng',
  'staff_category': 'Senior Staff'}
]



staff_categories = ['Senior Member (Administrative)', 
                    'Senior Member (Academic)', 
                    'Senior Staff', 
                    'PhD Student']



ksb_programmes = [
    {'name': 'ACCOUNTING AND FINANCE - 100', 'year': 1},
    {'name': 'ACCOUNTING AND FINANCE - 200', 'year': 2},
    {'name': 'ACCOUNTING AND FINANCE - 300', 'year': 3},
    {'name': 'ACCOUNTING AND FINANCE - 400', 'year': 4},
    {'name': 'HOSPITALITY AND TOURISM MANAGEMENT - 100', 'year': 1},
    {'name': 'HOSPITALITY AND TOURISM MANAGEMENT - 200', 'year': 2},
    {'name': 'HOSPITALITY AND TOURISM MANAGEMENT - 300', 'year': 3},
    {'name': 'HOSPITALITY AND TOURISM MANAGEMENT - 400', 'year': 4},
    {'name': 'HUMAN RESOURCE MANAGEMENT - 100', 'year': 1},
    {'name': 'HUMAN RESOURCE MANAGEMENT - 200', 'year': 2},
    {'name': 'HUMAN RESOURCE MANAGEMENT - 300', 'year': 3},
    {'name': 'HUMAN RESOURCE MANAGEMENT - 400', 'year': 4},
    {'name': 'LOGISTICS | BUSINESS IT - 100', 'year': 1},
    {'name': 'LOGISTICS | BUSINESS IT - 200', 'year': 2},
    {'name': 'LOGISTICS | BUSINESS IT - 300', 'year': 3},
    {'name': 'LOGISTICS | BUSINESS IT - 400', 'year': 4},
    {'name': 'MARKETING AND INTERNATIONAL BUSINESS MGT - 100', 'year': 1},
    {'name': 'MARKETING AND INTERNATIONAL BUSINESS MGT - 200', 'year': 2},
    {'name': 'MARKETING AND INTERNATIONAL BUSINESS MGT - 300', 'year': 3},
    {'name': 'MARKETING AND INTERNATIONAL BUSINESS MGT - 400', 'year': 4},
    {'name': 'ACCOUNTING AND FINANCE - 100 (PARALLEL)', 'year': 1},
    {'name': 'ACCOUNTING AND FINANCE - 200 (PARALLEL)', 'year': 2},
    {'name': 'ACCOUNTING AND FINANCE - 300 (PARALLEL)', 'year': 3},
    {'name': 'ACCOUNTING AND FINANCE - 400 (PARALLEL)', 'year': 4},
    {'name': 'HOSPITALITY AND TOURISM MANAGEMENT - 100 (PARALLEL)', 'year': 1},
    {'name': 'HOSPITALITY AND TOURISM MANAGEMENT - 200 (PARALLEL)', 'year': 2},
    {'name': 'HOSPITALITY AND TOURISM MANAGEMENT - 300 (PARALLEL)', 'year': 3},
    {'name': 'HOSPITALITY AND TOURISM MANAGEMENT - 400 (PARALLEL)', 'year': 4},
    {'name': 'HUMAN RESOURCE MANAGEMENT - 100 (PARALLEL)', 'year': 1},
    {'name': 'HUMAN RESOURCE MANAGEMENT - 200 (PARALLEL)', 'year': 2},
    {'name': 'HUMAN RESOURCE MANAGEMENT - 300 (PARALLEL)', 'year': 3},
    {'name': 'HUMAN RESOURCE MANAGEMENT - 400 (PARALLEL)', 'year': 4},
    {'name': 'LOGISTICS | BUSINESS IT - 100 (PARALLEL)', 'year': 1},
    {'name': 'LOGISTICS | BUSINESS IT - 200 (PARALLEL)', 'year': 2},
    {'name': 'LOGISTICS | BUSINESS IT - 300 (PARALLEL)', 'year': 3},
    {'name': 'LOGISTICS | BUSINESS IT - 400 (PARALLEL)', 'year': 4},
    {'name': 'MARKETING AND INTERNATIONAL BUSINESS MGT - 100 (PARALLEL)', 'year': 1},
    {'name': 'MARKETING AND INTERNATIONAL BUSINESS MGT - 200 (PARALLEL)', 'year': 2},
    {'name': 'MARKETING AND INTERNATIONAL BUSINESS MGT - 300 (PARALLEL)', 'year': 3},
    {'name': 'MARKETING AND INTERNATIONAL BUSINESS MGT - 400 (PARALLEL)', 'year': 4},
    {'name': 'MBA | MPHIL - 100 (FT|PT|WEEKEND)', 'year': 1},
    {'name': 'MBA | MPHIL - 200 (FT|PT|WEEKEND)', 'year': 2},
    {'name': 'MSC BUSINESS ADMINSTRATION - 100', 'year': 1},
]





