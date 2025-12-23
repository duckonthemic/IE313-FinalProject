"""
Fixed Parser for CareerViet - Extracts from 'Thông tin khác' section
Output: 11 columns exactly as specified
"""
import os
import re
from pathlib import Path
from tqdm import tqdm
import pandas as pd
from bs4 import BeautifulSoup

# Exact 11 columns as specified (no 'source' column)
OUTPUT_COLUMNS = [
    'job_title', 'job_type', 'position_level', 'city', 'experience',
    'skills', 'job_fields', 'salary', 'salary_min', 'salary_max', 'unit'
]

def parse_salary(salary_str):
    """Parse Vietnamese salary string into min, max, unit"""
    if not salary_str:
        return None, None, None
    
    salary_str = str(salary_str).strip()
    salary_lower = salary_str.lower()
    
    # Check for negotiable
    if any(x in salary_lower for x in ['thỏa thuận', 'cạnh tranh', 'thoả thuận', 'thương lượng']):
        return None, None, 'VND'
    
    # Check for USD
    if 'usd' in salary_lower or '$' in salary_str:
        unit = 'USD'
        numbers = re.findall(r'[\d.,]+', salary_str)
        nums = []
        for n in numbers:
            try:
                nums.append(float(n.replace(',', '').replace('.', '')))
            except:
                pass
        if len(nums) >= 2:
            return min(nums), max(nums), unit
        elif len(nums) == 1:
            return nums[0], nums[0], unit
        return None, None, unit
    
    # VND - triệu format
    unit = 'VND'
    
    # Pattern: X Tr - Y Tr (both have Tr/Triệu suffix)
    match = re.search(r'(\d+(?:[.,]\d+)?)\s*(?:Tr|Triệu)?\s*[-–]\s*(\d+(?:[.,]\d+)?)\s*(?:Tr|Triệu)?', salary_str, re.I)
    if match:
        try:
            min_val = float(match.group(1).replace(',', '.'))
            max_val = float(match.group(2).replace(',', '.'))
            # Convert to VND (millions) if values are small
            if min_val < 1000:
                min_val *= 1_000_000
            if max_val < 1000:
                max_val *= 1_000_000
            return min_val, max_val, unit
        except:
            pass
    
    # Single value with Tr/Triệu
    match = re.search(r'(\d+(?:[.,]\d+)?)\s*(?:Tr|Triệu)', salary_str, re.I)
    if match:
        try:
            val = float(match.group(1).replace(',', '.'))
            if val < 1000:
                val *= 1_000_000
            return val, val, unit
        except:
            pass
    
    return None, None, unit


def parse_careerviet(html_content):
    """Parse CareerViet HTML - extract from Thông tin khác section"""
    soup = BeautifulSoup(html_content, 'lxml')
    data = {}
    
    # Remove script/style/nav/footer
    for tag in soup(['script', 'style', 'footer', 'nav', 'header']):
        tag.decompose()
    
    # Get full text for pattern matching
    full_text = soup.get_text()
    
    # === JOB TITLE ===
    h1 = soup.find('h1')
    if h1:
        data['job_title'] = ' '.join(h1.get_text(strip=True).split())[:200]
    
    # === SALARY === (from "Thông tin khác" section)
    # Look for "Lương: X Tr - Y Tr VND" pattern
    sal_match = re.search(r'Lương[:\s]*\n*\s*([\d.,]+\s*(?:Tr|Triệu)?\s*[-–]\s*[\d.,]+\s*(?:Tr|Triệu)?(?:\s*VND)?)', full_text, re.I)
    if sal_match:
        data['salary'] = sal_match.group(1).strip()
    else:
        # Try simpler pattern
        sal_match = re.search(r'Lương[:\s]*\n*\s*(Thỏa thuận|Cạnh tranh|[\d.,]+[^\n]*)', full_text, re.I)
        if sal_match:
            sal_text = sal_match.group(1).strip()
            # Clean up - stop at first non-salary text
            sal_text = re.split(r'(?:VND|USD)', sal_text)[0]
            if 'VND' in sal_match.group(0) or 'Tr' in sal_match.group(0):
                sal_text += ' VND'
            data['salary'] = sal_text[:50]
    
    # === POSITION LEVEL === (Cấp bậc)
    level_match = re.search(r'Cấp bậc[:\s]*\n*\s*([^\n]+)', full_text, re.I)
    if level_match:
        level = level_match.group(1).strip()
        # Clean - take first meaningful part
        level = level.split('\n')[0].strip()
        if level and len(level) < 50:
            data['position_level'] = level
    
    # === JOB TYPE === (Hình thức)
    type_match = re.search(r'Hình thức[:\s]*\n*\s*([^\n]+)', full_text, re.I)
    if type_match:
        jtype = type_match.group(1).strip()
        jtype = jtype.split('\n')[0].strip()
        if jtype and len(jtype) < 50:
            data['job_type'] = jtype
    
    # === EXPERIENCE === (Kinh nghiệm)
    exp_match = re.search(r'Kinh nghiệm[:\s]*\n*\s*(\d+\s*[-–]\s*\d+\s*năm|\d+\s*năm|Không yêu cầu|Chưa có kinh nghiệm|Dưới \d+ năm|Trên \d+ năm)', full_text, re.I)
    if exp_match:
        data['experience'] = exp_match.group(1).strip()
    
    # === CITY === (from detail-box map area)
    city_el = soup.find(class_='map')
    if city_el:
        city_link = city_el.find('a')
        if city_link:
            data['city'] = city_link.get_text(strip=True)
    
    if 'city' not in data:
        # Fallback: look for "Địa điểm" in detail-box
        detail_boxes = soup.find_all(class_='detail-box')
        for box in detail_boxes:
            text = box.get_text()
            if 'Địa điểm' in text:
                # Extract city name after "Địa điểm"
                city_match = re.search(r'Địa điểm\s*\n+\s*([A-Za-zÀ-ỹ\s]+)', text)
                if city_match:
                    data['city'] = city_match.group(1).strip()[:30]
                break
    
    # === SKILLS === (from job-tags)
    skills_el = soup.find(class_=re.compile('job-tags', re.I))
    if skills_el:
        items = skills_el.find_all(['li', 'a', 'span'])
        skills = [i.get_text(strip=True) for i in items if i.get_text(strip=True)]
        # Filter out empty and job titles
        skills = [s for s in skills if s and len(s) < 50 and not s.startswith('[')]
        if skills:
            data['skills'] = ', '.join(skills[:10])
    
    # === JOB FIELDS === (from detail-box)
    for box in soup.find_all(class_='detail-box'):
        text = box.get_text()
        if 'Ngành nghề' in text:
            # Find all links in this box after "Ngành nghề"
            links = box.find_all('a')
            fields = [l.get_text(strip=True) for l in links if l.get_text(strip=True)]
            if fields:
                data['job_fields'] = ', '.join(fields[:5])
            break
    
    # === PARSE SALARY COMPONENTS ===
    sal_min, sal_max, unit = parse_salary(data.get('salary', ''))
    data['salary_min'] = sal_min
    data['salary_max'] = sal_max
    data['unit'] = unit if unit else 'VND'
    
    return data


def main():
    html_folder = './data/html_content/careerviet'
    output_file = './datasets/raw_jobs/careerviet_final.csv'
    
    print("="*60)
    print("CAREERVIET PARSER - FIXED VERSION")  
    print("="*60)
    
    html_files = [f for f in os.listdir(html_folder) if f.endswith('.html')]
    print(f"Found {len(html_files)} HTML files")
    
    results = []
    errors = 0
    
    for filename in tqdm(html_files, desc="Parsing"):
        filepath = os.path.join(html_folder, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                html = f.read()
            
            # Skip small files (error pages)
            if len(html) < 10000:
                errors += 1
                continue
            
            data = parse_careerviet(html)
            
            # Only add if has job_title
            if data.get('job_title'):
                results.append(data)
            else:
                errors += 1
                
        except Exception as e:
            errors += 1
            continue
    
    print(f"\nParsed: {len(results)} jobs")
    print(f"Errors/Skipped: {errors} files")
    
    # Create DataFrame
    df = pd.DataFrame(results)
    
    # Ensure all columns exist
    for col in OUTPUT_COLUMNS:
        if col not in df.columns:
            df[col] = None
    
    # Select only the 11 specified columns in order
    df = df[OUTPUT_COLUMNS]
    
    # Save
    Path('./datasets/raw_jobs').mkdir(parents=True, exist_ok=True)
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"Saved to {output_file}")
    
    # Quality report
    print("\n" + "="*60)
    print("DATA QUALITY - 11 COLUMNS")
    print("="*60)
    for col in OUTPUT_COLUMNS:
        filled = df[col].notna().sum()
        non_empty = df[col].apply(lambda x: bool(str(x).strip()) if pd.notna(x) else False).sum()
        pct = non_empty / len(df) * 100 if len(df) > 0 else 0
        print(f"  {col}: {non_empty}/{len(df)} ({pct:.0f}%)")
    
    # Sample
    print("\n" + "="*60)
    print("SAMPLE DATA")
    print("="*60)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    print(df[['job_title', 'salary', 'salary_min', 'salary_max', 'city', 'position_level']].head(5).to_string())


if __name__ == "__main__":
    main()
