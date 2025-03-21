# Focus 2 Workbook Scraper

A Python web scraper designed to extract all lessons and answers from the Focus 2 Workbook from Studifor.com.

## 📚 Description

This scraper automates the process of collecting educational content from the Focus 2 Workbook, organizing all sections, exercises, questions, and answers into structured formats for easy reference.

The tool is especially useful for students who want to have a local, searchable copy of the workbook content for study purposes.

## ✨ Features

- **Complete Content Extraction**: Scrapes all sections, exercises, questions, and answers
- **Multiple Output Formats**:
  - JSON for data processing and analysis
  - Markdown for readable documentation
  - Clean text format for easy copy/paste into Word documents
- **Progress Tracking**: Visual feedback during the scraping process
- **Error Handling**: Continues operation even if individual exercises fail
- **Rate Limiting**: Respects website resources with configurable delays

## 🔧 Requirements

- Python 3.6+
- Required packages:
  - requests
  - beautifulsoup4
  - tqdm

## 📥 Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/focus2-workbook-scraper.git
   cd focus2-workbook-scraper
   ```

2. Install the required packages:
   ```bash
   pip install requests beautifulsoup4 tqdm
   ```

## 🚀 Usage

Run the scraper with:

```bash
python scraper.py
```

The script will:

1. Create a `data` directory (if it doesn't exist)
2. Fetch all sections and exercises from the website
3. Extract content from each exercise page
4. Save the data in three formats:
   - `data/focus_2_workbook.json`: Structured JSON data
   - `data/focus_2_workbook.md`: Markdown documentation
   - `data/focus_2_workbook.txt`: Clean text format for Word

### Test Mode

For testing purposes, you can enable test mode by setting `test_mode = True` in the `main()` function. This will limit the scraper to only process 5 exercises, allowing you to verify functionality before running a full scrape.

## 📋 Output Structure

### JSON Structure

```json
{
  "Section Title": {
    "exercises": {
      "Exercise 1": {
        "question": "Question text...",
        "answer": "Answer text..."
      },
      "Exercise 2": {
        ...
      }
    }
  },
  "Another Section": {
    ...
  }
}
```

### Text File Format

```
FOCUS 2 WORKBOOK - ANSWERS

Section Title
============

Exercise 1
----------
Answer content line 1
Answer content line 2
...

Exercise 2
----------
...
```

## ⚠️ Disclaimer

This tool is intended for personal educational use only. Please respect the website's terms of service and copyright policies. Use the scraper responsibly with reasonable delays between requests to avoid overloading the server.

## 🛠️ Customization

You can customize the scraper behavior by modifying:

- `delay` parameter in `scrape_all()` to adjust the time between requests
- Output formats in the `save_to_*` methods
- User agent in the `__init__` method if needed

## 📝 License

[MIT License](LICENSE)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome. Feel free to check the [issues page](https://github.com/stoychevww/python-scraper-for-focus-workbook-a2/issues) if you want to contribute.
