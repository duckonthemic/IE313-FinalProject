# City/Province Reference Table

## 📍 Overview

Bảng tham chiếu này map các **pattern location đa dạng** từ raw data về một **tập giá trị city/province chuẩn**. Thay vì hard-code trong function `normalize_city()`, chúng ta sử dụng bảng này để dễ dàng maintain và mở rộng.

## 📊 File Location

```
data/reference/city_province_mapping.csv
```

## 🔧 Structure

| Column | Type | Description |
|--------|------|-------------|
| `pattern` | string | Pattern để match (lowercase, no diacritics) |
| `city_standard` | string | City name chuẩn (Title Case, with diacritics if needed) |
| `province_standard` | string | Province name chuẩn (có thể giống city hoặc khác) |
| `notes` | string | Ghi chú về pattern (optional) |

## 📋 Current Coverage

### Ha Noi (15 patterns)
- **Core**: `ha noi`, `hanoi`
- **Districts**: `dong da`, `cau giay`, `ba dinh`, `hoan kiem`, `thanh xuan`, `hai ba trung`, `nam tu liem`, `bac tu liem`, `tay ho`, `long bien`, `dong anh`, `gia lam`, `hoang mai`

### Ho Chi Minh (31 patterns)
- **Core**: `ho chi minh`, `hcm`, `saigon`, `sai gon`, `tp hcm`, `tphcm`
- **Districts 1-12**: `quan 1-12`, `district 1-12`
- **Named Districts**: `tan binh`, `binh thanh`, `phu nhuan`, `go vap`, `thu duc`, `thu duc city`, `binh tan`, `tan phu`

### Da Nang (6 patterns)
- **Core**: `da nang`, `danang`
- **Districts**: `hai chau`, `son tra`, `ngu hanh son`, `lien chieu`, `cam le`

### Hai Phong (4 patterns)
- **Core**: `hai phong`, `haiphong`
- **Districts**: `hong bang`, `le chan`, `ngo quyen`

### Can Tho (4 patterns)
- **Core**: `can tho`, `cantho`
- **Districts**: `ninh kieu`, `binh thuy`

### Binh Duong (5 patterns)
- **Core**: `binh duong`, `binhduong`
- **Cities**: `thu dau mot`, `di an`, `thuan an`

### Dong Nai (4 patterns)
- **Core**: `dong nai`, `dongnai`
- **Cities**: `bien hoa`, `long khanh`

### Nha Trang / Khanh Hoa (3 patterns)
- **Core**: `nha trang`, `khanh hoa`
- **Cities**: `cam ranh`

### Vung Tau / Ba Ria - Vung Tau (2 patterns)
- **Core**: `vung tau`, `ba ria`

### Remote (5 patterns)
- **Keywords**: `remote`, `work from home`, `wfh`, `online`, `work remotely`

## 🔄 Usage in Pipeline

### Current Implementation (Hard-coded)
```python
def normalize_city(location_raw):
    if pd.isna(location_raw) or location_raw == '':
        return 'Unknown'
    
    location_lower = location_raw.lower()
    
    if 'hà nội' in location_lower or 'ha noi' in location_lower:
        return 'Ha Noi'
    elif 'hồ chí minh' in location_lower or 'hcm' in location_lower:
        return 'Ho Chi Minh'
    # ... more if-else
    else:
        return 'Other'
```

### Proposed Implementation (Table-driven)
```python
import pandas as pd
from unidecode import unidecode

# Load reference table
city_ref = pd.read_csv('data/reference/city_province_mapping.csv')

def normalize_city_v2(location_raw, ref_table=city_ref):
    """
    Normalize city using reference table lookup
    
    Args:
        location_raw: Raw location string from source
        ref_table: City reference table DataFrame
    
    Returns:
        Standardized city name or 'Other'/'Unknown'
    """
    # Handle NULL/empty
    if pd.isna(location_raw) or location_raw == '':
        return 'Unknown'
    
    # Pre-process: lowercase + remove diacritics
    location_normalized = unidecode(location_raw.lower().strip())
    
    # Remove special characters (keep letters and spaces)
    location_normalized = re.sub(r'[^a-z0-9\s]', ' ', location_normalized)
    location_normalized = re.sub(r'\s+', ' ', location_normalized).strip()
    
    # Pattern matching (exact match first, then substring)
    for _, row in ref_table.iterrows():
        pattern = row['pattern']
        
        # Exact match (higher priority)
        if location_normalized == pattern:
            return row['city_standard']
    
    # Substring match (lower priority)
    for _, row in ref_table.iterrows():
        pattern = row['pattern']
        
        if pattern in location_normalized:
            return row['city_standard']
    
    # Fallback
    return 'Other'

# Apply to DataFrame
df['city'] = df['location_raw'].apply(normalize_city_v2)
```

## 📈 Coverage Statistics

Based on raw data analysis (Kaggle + GitHub = 4,513 jobs):

| City | Count | Percentage | Patterns Used |
|------|-------|-----------|---------------|
| **Ho Chi Minh** | 2,060 | 51.7% | hcm, saigon, quan 1-12, tan binh, etc. |
| **Ha Noi** | 1,431 | 35.9% | hanoi, dong da, cau giay, ba dinh, etc. |
| **Da Nang** | 115 | 2.9% | da nang, hai chau |
| **Other** | 364 | 9.1% | Various |
| **Remote** | 6 | 0.2% | remote, wfh |
| **Hai Phong** | 3 | 0.1% | hai phong |
| **Can Tho** | 3 | 0.1% | can tho |
| **Unknown** | 3 | 0.1% | NULL/empty |

**Total**: 3,985 unique jobs after deduplication

## 🔧 How to Extend

### Adding New City
1. **Identify patterns** from raw data:
   ```bash
   # Find unique locations
   grep -i "quy nhon" data/raw/*/jobs.csv
   ```

2. **Add to CSV**:
   ```csv
   quy nhon,Quy Nhon,Binh Dinh,Coastal city in Binh Dinh
   binh dinh,Quy Nhon,Binh Dinh,Province capital
   ```

3. **Re-run normalization** (no code changes needed!)

### Adding New District
1. **Check parent city**:
   - Example: "Tan Phu" → Ho Chi Minh

2. **Add pattern**:
   ```csv
   tan phu,Ho Chi Minh,Ho Chi Minh,District in HCMC
   ```

### Handling Ambiguous Patterns
- **Problem**: "Binh Thanh" could be district in HCM or other province
- **Solution**: 
  - Use **exact match** for ambiguous patterns
  - Use **context** (check if "HCM" or "District" appears nearby)
  - **Priority**: Exact match > Substring match

## ⚠️ Known Issues

### 1. International Locations
**Problem**: `"Singapore, Other, Ha Noi"` maps to `Ha Noi` (incorrect)

**Current Behavior**:
- Pattern `ha noi` found → returns `Ha Noi`

**Solution** (future):
```python
# Add country detection first
if 'singapore' in location_normalized:
    return 'Singapore'  # Add to table with country='Singapore'
```

### 2. Complex Addresses
**Problem**: `"521 Kim Mã, Ba Dinh, Ha Noi"`

**Current Behavior**:
- Matches `ba dinh` → returns `Ha Noi` ✅ (correct)
- Matches `ha noi` → returns `Ha Noi` ✅ (correct)

**Works because**: Both patterns map to same city

### 3. Province vs City
**Problem**: `province` column currently duplicates `city`

**Current Behavior**:
```python
df['province'] = df['city']  # Same value
```

**Future Enhancement**:
```python
# Use province_standard from reference table
df['province'] = df['location_raw'].apply(normalize_province)
```

**Example**:
- Location: `"Nha Trang"`
- City: `Nha Trang`
- Province: `Khanh Hoa` (from reference table)

## 🧪 Testing

### Test Cases
```python
import pandas as pd

# Load function
from normalize import normalize_city_v2

# Test cases
test_cases = [
    ("Hồ Chí Minh", "Ho Chi Minh"),
    ("HCM", "Ho Chi Minh"),
    ("Quan 1, TP.HCM", "Ho Chi Minh"),
    ("Ha Noi", "Ha Noi"),
    ("Dong Da, Hanoi", "Ha Noi"),
    ("Da Nang", "Da Nang"),
    ("Remote work", "Remote"),
    ("Some unknown city", "Other"),
    ("", "Unknown"),
    (None, "Unknown"),
]

# Run tests
for raw, expected in test_cases:
    result = normalize_city_v2(raw)
    status = "✅" if result == expected else "❌"
    print(f"{status} {raw!r} → {result} (expected: {expected})")
```

### Expected Output
```
✅ 'Hồ Chí Minh' → Ho Chi Minh (expected: Ho Chi Minh)
✅ 'HCM' → Ho Chi Minh (expected: Ho Chi Minh)
✅ 'Quan 1, TP.HCM' → Ho Chi Minh (expected: Ho Chi Minh)
✅ 'Ha Noi' → Ha Noi (expected: Ha Noi)
✅ 'Dong Da, Hanoi' → Ha Noi (expected: Ha Noi)
✅ 'Da Nang' → Da Nang (expected: Da Nang)
✅ 'Remote work' → Remote (expected: Remote)
✅ 'Some unknown city' → Other (expected: Other)
✅ '' → Unknown (expected: Unknown)
✅ None → Unknown (expected: Unknown)
```

## 📊 Validation Metrics

After applying normalization:

| Metric | Value | Status |
|--------|-------|--------|
| **Total jobs** | 3,985 | ✅ |
| **With city** | 3,985 (100%) | ✅ |
| **Ha Noi** | 1,431 (35.9%) | ✅ |
| **Ho Chi Minh** | 2,060 (51.7%) | ✅ |
| **Da Nang** | 115 (2.9%) | ✅ |
| **Other cities** | 364 (9.1%) | ✅ |
| **Remote** | 6 (0.2%) | ✅ |
| **Unknown** | 9 (0.2%) | ✅ |

**Normalization Rate**: 99.8% (3,976 / 3,985 mapped to standard cities)

## 🔗 Related Documentation

- **Master Schema**: See `docs/schema.md` (City Normalization Strategy section)
- **Column Mapping**: See `docs/column_mapping.md` (normalize_city function)
- **Pipeline**: See `docs/pipeline_overview.md` (Block C: Normalization)
- **Implementation**: See `vietnam_it_jobs_merge_analysis.ipynb` (Cell 5-6)

## 🔮 Future Enhancements

1. **Fuzzy Matching**:
   - Use `fuzzywuzzy` for typo tolerance
   - `"Ha Noi"` vs `"Hanoi"` → score 90% → match

2. **Multi-language Support**:
   - Vietnamese: `Hà Nội`
   - English: `Hanoi`
   - Map both to `Ha Noi`

3. **Geocoding**:
   - Add latitude/longitude columns
   - Enable geographic visualizations

4. **District-level Analysis**:
   - Separate `district` column
   - City: `Ho Chi Minh`, District: `Quan 1`

5. **Province Hierarchy**:
   - City: `Nha Trang`
   - Province: `Khanh Hoa`
   - Region: `South Central Coast`

---

**Last Updated**: November 14, 2025  
**Version**: 1.0.0  
**Status**: ✅ Production-ready reference table
