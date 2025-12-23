# Crawler Reference (from JobsTrending)

This folder contains crawler scripts adapted from [tinh2044/JobsTrending](https://github.com/tinh2044/JobsTrending).

## Structure

```
crawler-ref/
├── parse_html.py       # Main parsing script (Selenium + XPath)
├── selector/           # XPath selectors for each website
│   ├── topcv.json      # TopCV selectors
│   ├── careerviet.json # CareerViet selectors
│   ├── jobsgo.json     # JobsGo selectors
│   └── vieclam24h.json # ViecLam24h selectors
├── links/              # Seed URLs for crawling
│   ├── topcv.json      # 560+ TopCV URLs
│   ├── careerviet.json # CareerViet URLs
│   └── ...
└── vn_cities.json      # Vietnamese cities mapping
```

## Usage

### Prerequisites
```bash
pip install selenium tqdm pandas
# Download ChromeDriver and update path in parse_html.py
```

### Parse HTML Files
```bash
# Place downloaded HTML files in ./data/html_content/{website_name}/
python parse_html.py --name topcv
```

### Output
- Parsed data saved to `./datasets/raw_jobs/{website_name}_*.csv`
- Backup JSON files in `./data/backup/{website_name}/`

## Workflow

1. **Download HTML files** from job websites (using the NestJS crawler or manually)
2. **Run parse_html.py** to extract structured data
3. **Process CSV** with data_processing_pipeline.py

## Notes

- Original crawler uses NestJS + Puppeteer (complex setup)
- For simpler approach, use Selenium or requests to download HTML files
- Selectors may need adjustment as websites update their HTML structure
