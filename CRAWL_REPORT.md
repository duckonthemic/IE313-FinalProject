# Vietnam Job Crawler - Technical Report

## 1. Overview

Multi-source job crawler for collecting job postings from Vietnamese recruitment websites.

## 2. Data Sources

| # | Source | URL | Jobs Collected | Status |
|---|--------|-----|----------------|--------|
| 1 | CareerViet | careerviet.vn | ~34,000 | ✅ Active |
| 2 | TopCV | topcv.vn | ~25,600 | ✅ Active |
| 3 | ViecLam24h | vieclam24h.vn | ~17,000 | ✅ Active |
| 4 | JobsGo | jobsgo.vn | ~8,500 | ✅ Active |

**Total: 85,470 job postings**

## 3. Output Schema

```
job_title       - Job title (string)
job_type        - Employment type: full-time, part-time, etc.
position_level  - Position level: nhân viên, quản lý, etc.
city            - Location/city
experience      - Required experience
skills          - Required skills (comma-separated)
job_fields      - Industry/field
salary          - Salary text
salary_min      - Minimum salary (million VND)
salary_max      - Maximum salary (million VND)
unit            - Currency unit (vnd)
```

## 4. Data Quality

| Column | Coverage | Notes |
|--------|----------|-------|
| job_title | 100% | ✅ |
| job_type | 100% | ✅ |
| position_level | 100% | ✅ |
| city | 100% | ✅ |
| experience | 100% | ✅ |
| skills | 87% | Some missing |
| job_fields | 91% | ✅ |
| salary | 100% | ✅ |
| salary_min | 100% | ✅ |
| salary_max | 100% | ✅ |
| unit | 100% | ✅ |

## 5. Technical Stack

- **Language:** Python 3.9+
- **Web Scraping:** Selenium, BeautifulSoup4, lxml
- **Data Processing:** pandas, numpy
- **Configuration:** JSON selector files

## 6. File Structure

```
crawler.py                      # Main crawler script
crawler-ref/
├── selector/
│   ├── careerviet.json        # CareerViet selectors
│   ├── topcv.json             # TopCV selectors
│   ├── vieclam24h.json        # ViecLam24h selectors
│   └── jobsgo.json            # JobsGo selectors
├── fast_crawl.py              # URL collector
└── fast_parser.py             # HTML parser
data/
├── raw/careerviet_raw.csv     # Combined output (85,470 jobs)
└── clean/jobs_clean.csv       # Cleaned data
```

## 7. Usage

```bash
# Quick demo (200 jobs per source)
python crawler.py --mode demo

# Full crawl (all available jobs)
python crawler.py --mode full
```

## 8. Anti-Detection Measures

- Random delays between requests (1-3 seconds)
- Rotating User-Agent headers
- Headless browser with stealth options
- Rate limiting and retry logic

## 9. Crawl Statistics

- **Period:** December 2024
- **Total jobs:** 85,470
- **Unique titles:** 23,576
- **Top cities:** Hà Nội (26,224), HCM (25,958)
- **Median salary:** 13 million VND

---
*Last updated: December 2024*
