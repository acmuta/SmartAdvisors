# import pdfplumber
# import re
# import sys
# from typing import List

# def extract_all_courses(pdf_path: str) -> List[str]:
#     """
#     Parses a UTA Unofficial Civil Engineering Undergrad transcript PDF to find all course codes,
#     handling all known formats including different semesters for transfers.
#     """
    
#     # Pattern 1: Finds regular semester courses (graded and in-progress).
#     semester_course_pattern = re.compile(r'^([A-Z]{2,4}(?:-[A-Z]{2})?)\s(\d{4}).*?\d+\.\d{3}\s+\d+\.\d{3}')
    
#     # Pattern 2: Finds ALL transfer/test credits.
#     # It now specifically looks for the semester name (Summer, Spring, Fall) and is case-insensitive.
#     transfer_test_pattern = re.compile(
#         r'Transferred to Term \d{4} (?:Summer|Spring|Fall) as\s*\n\s*([A-Z]{3,4}\s\d{4})',
#         re.IGNORECASE
#     )

#     found_courses_set = set()
    
#     try:
#         with pdfplumber.open(pdf_path) as pdf:
#             print(f"Reading {len(pdf.pages)} pages from '{pdf_path}'...")
            
#             for page in pdf.pages:
#                 text = page.extract_text(x_tolerance=2, y_tolerance=3)
                
#                 if not text:
#                     continue
                
#                 # --- Search for all Transfer and Test Credit courses ---
#                 transfer_matches = transfer_test_pattern.findall(text)
#                 for course_code in transfer_matches:
#                     found_courses_set.add(course_code)
                
#                 # --- Search for regular and in-progress courses line by line ---
#                 lines = text.split('\n')
#                 for line in lines:
#                     match = semester_course_pattern.match(line.strip())
#                     if match:
#                         course_code = f"{match.group(1)} {match.group(2)}"
#                         found_courses_set.add(course_code)
                        
#     except FileNotFoundError:
#         print(f"Error: The file '{pdf_path}' was not found.")
#         return []
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return []

#     unique_courses = sorted(list(found_courses_set))
#     return unique_courses

# # --- Main execution block ---
# if __name__ == "__main__":
#     if len(sys.argv) > 1:
#         transcript_pdf_path = sys.argv[1]
#     else:
#         transcript_pdf_path = '/home/aki/Downloads/SSR_TSRPT_UN.pdf'
    
#     extracted_courses = extract_all_courses(transcript_pdf_path)
    
#     if extracted_courses:
#         print("\n--- Found Courses ---")
#         for course in extracted_courses:
#             print(course)
#         print(f"\nTotal unique courses found: {len(extracted_courses)}")
#     else:
#         print("\nNo course codes could be extracted.")

# # if someone has a D, F, P, F, Q,W, R, I Z
# # also if you are a freshman, there might not be any grades attached to the courses
# # also if the user has no classes, there should be an option called i'm new to UTA and we just send them to select the professor and courses attributes

import pdfplumber
import re
from typing import List

def extract_all_courses(pdf_path: str) -> List[str]:
    """
    Parses a UTA Unofficial Civil Engineering Undergrad transcript PDF to find all course codes.
    """
    semester_course_pattern = re.compile(r'^([A-Z]{2,4}(?:-[A-Z]{2})?)\s(\d{4}).*?\d+\.\d{3}\s+\d+\.\d{3}')
    transfer_test_pattern = re.compile(
        r'Transferred to Term \d{4} (?:Summer|Spring|Fall) as\s*\n\s*([A-Z]{3,4}\s\d{4})',
        re.IGNORECASE
    )

    found_courses_set = set()
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text(x_tolerance=2, y_tolerance=3)
                if not text:
                    continue
                
                for course_code in transfer_test_pattern.findall(text):
                    found_courses_set.add(course_code)
                
                for line in text.split('\n'):
                    match = semester_course_pattern.match(line.strip())
                    if match:
                        found_courses_set.add(f"{match.group(1)} {match.group(2)}")
                        
    except Exception as e:
        print(f"Error parsing PDF: {e}")
        return []

    unique_courses = sorted(list(found_courses_set))
    return unique_courses

# --- Main execution block ---
if __name__ == "__main__":
    if len(sys.argv) > 1:
        transcript_pdf_path = sys.argv[1]
    else:
        transcript_pdf_path = "/Users/johna/Downloads/SSR_TSRPT_UN (20) (1).pdf"
    
    extracted_courses = extract_all_courses(transcript_pdf_path)
    
    if extracted_courses:
        print("\n--- Found Courses ---")
        for course in extracted_courses:
            print(course)
        print(f"\nTotal unique courses found: {len(extracted_courses)}")
    else:
        print("\nNo course codes could be extracted.")

# if someone has a D, F, P, F, Q,W, R, I Z
# also if you are a freshman, there might not be any grades attached to the courses
# also if the user has no classes, there should be an option called i'm new to UTA and we just send them to select the professor and courses attributes
