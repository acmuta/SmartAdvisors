#!/usr/bin/env python3
"""
UTA Catalog Course Scraper - Version 3.0
========================================
Features:
1. Python-style list output: ['MAE 1140', 'MATH 1426']
2. "Or" Filter: Only keeps the first course mentioned in an "or" group.
3. Pathing: Saves to server/data/ folder relative to script location.
"""

import sys
import os
import re
import csv
import urllib.request
import html

def fetch_page(url):
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) SmartAdvisors/1.0'
    })
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read().decode('utf-8', errors='replace')

def clean_all_html(text):
    text = html.unescape(text)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = text.replace('\xa0', ' ').replace('\t', ' ')
    return re.sub(r'\s+', ' ', text).strip()

def extract_primary_codes(requirement_text):
    """
    Splits by commas/ands and takes only the first course found in each segment.
    Example: 'MAE 1140 (or ENGR 1250), MATH 1426' -> ['MAE 1140', 'MATH 1426']
    """
    if not requirement_text:
        return []
    
    # Split by common separators like comma, semicolon, or the word 'and'
    segments = re.split(r',|;| and ', requirement_text, flags=re.IGNORECASE)
    
    primary_codes = []
    for seg in segments:
        # Find the first occurrence of a DEPT NNNN pattern in this segment
        match = re.search(r'([A-Z]{2,4})\s*(\d{4})', seg)
        if match:
            primary_codes.append(f"{match.group(1)} {match.group(2)}")
            
    return primary_codes

def scrape_catalog(dept_code):
    dept_lower = dept_code.lower()
    url = f'https://catalog.uta.edu/coursedescriptions/{dept_lower}/'
    print(f"Fetching: {url}")

    try:
        full_html = fetch_page(url)
    except Exception as e:
        print(f"Error fetching: {e}")
        sys.exit(1)
    
    clean_page = clean_all_html(full_html)

    # Captures: 1:Dept, 2:Num, 3:Name, 4:Hours, 5:Description
    course_pattern = r'([A-Z]{2,4})\s*(\d{4})\.\s*(.*?)\.\s*(\d+)\s*Hours?\.\s*(.*?)(?=[A-Z]{2,4}\s*\d{4}\.|$)'
    matches = re.findall(course_pattern, clean_page)
    
    courses = []
    for dept, num, name, hours, desc in matches:
        code = f"{dept} {num}"
        
        # Isolate Prereq and Coreq text blocks
        prereq_match = re.search(r'Prerequisites?[:\s]+(.*?)(?:\.|$|Corequisite)', desc, re.IGNORECASE)
        coreq_match = re.search(r'Corequisites?[:\s]+(.*?)(?:\.|$)', desc, re.IGNORECASE)
        
        courses.append({
            'code': code,
            'name': name.strip(),
            'prereqs': extract_primary_codes(prereq_match.group(1)) if prereq_match else [],
            'coreqs': extract_primary_codes(coreq_match.group(1)) if coreq_match else []
        })
    
    return courses

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scrape_uta_catalog.py <DEPT>")
        sys.exit(1)

    dept_code = sys.argv[1].upper()

    # Determine Folder Paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    server_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
    data_dir = os.path.join(server_root, 'csv_files')

    if not os.path.isdir(data_dir):
        os.makedirs(data_dir)

    output_path = os.path.join(data_dir, f'{dept_code} Degree Plan CSV.csv')

    # Scrape
    all_found = scrape_catalog(dept_code)
    
    # Prefix filtering (AE/MAE overlap)
    relevant_prefixes = ['AE', 'MAE'] if dept_code in ['AE', 'MAE'] else [dept_code]
    filtered = [c for c in all_found if any(c['code'].startswith(p) for p in relevant_prefixes)]

    if not filtered:
        print(f"No results for {dept_code}.")
        return

    # Write CSV
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Formal Name', 'Course Name', 'Prerequisites', 'Corequisites', 'Requirement'])
        
        for c in filtered:
            # We use str() to ensure it looks like a Python list: ['DEPT NNNN']
            # If the list is empty, we return '[None]' as a string
            p_list = str(c['prereqs']) if c['prereqs'] else '[None]'
            c_list = str(c['coreqs']) if c['coreqs'] else '[None]'
            
            writer.writerow([c['code'], c['name'], p_list, c_list, 'required'])

    print(f"\nSuccess! Wrote {len(filtered)} courses to: {output_path}")

if __name__ == '__main__':
    main()