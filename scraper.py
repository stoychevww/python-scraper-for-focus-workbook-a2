import requests
from bs4 import BeautifulSoup
import json
import os
import time
import re
from tqdm import tqdm

class WorkbookScraper:
    def __init__(self, base_url="https://studifor.com"):
        self.base_url = base_url
        self.book_url = f"{self.base_url}/books/focus-2-workbook"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.all_data = {}
        
    def get_soup(self, url):
        """Get BeautifulSoup object from URL"""
        response = self.session.get(url)
        response.raise_for_status()  # Raise exception for bad status codes
        return BeautifulSoup(response.text, 'html.parser')
    
    def get_all_sections(self):
        """Get all sections from the main page"""
        soup = self.get_soup(self.book_url)
        sections = {}
        
        # Find all section cards
        section_cards = soup.select('.card')
        
        for card in section_cards:
            # Get section title
            title_elem = card.select_one('.accordion-header p')
            if not title_elem:
                continue
                
            section_title = title_elem.text.strip()
            
            # Get all exercises in this section
            exercises = {}
            exercise_links = card.select('.card-body a')
            
            for link in exercise_links:
                exercise_title = link.text.strip()
                exercise_url = link['href']
                exercises[exercise_title] = exercise_url
                
            sections[section_title] = {
                "exercises": exercises
            }
            
        return sections
    
    def get_exercise_content(self, exercise_url):
        """Get content from an exercise page"""
        full_url = f"{self.base_url}{exercise_url}"
        soup = self.get_soup(full_url)
        
        # Get exercise content
        content = {}
        
        # Get question
        question_container = soup.select_one('#question .card-body')
        if question_container:
            content['question'] = question_container.get_text(separator="\n", strip=True)
        
        # Get answer
        answer_container = soup.select_one('#solution .card-body')
        if answer_container:
            content['answer'] = answer_container.get_text(separator="\n", strip=True)
            
        return content
    
    def scrape_all(self, delay=1, max_exercises=None):
        """Scrape all sections and exercises"""
        print("Getting all sections...")
        sections = self.get_all_sections()
        
        print(f"Found {len(sections)} sections")
        
        total_exercises = sum(len(section['exercises']) for section in sections.values())
        if max_exercises:
            print(f"Will scrape up to {max_exercises} of {total_exercises} exercises")
        else:
            print(f"Found {total_exercises} exercises in total")
        
        # Create progress bar
        progress_bar = tqdm(total=min(total_exercises, max_exercises or total_exercises), desc="Scraping exercises")
        
        # Counter for exercises
        exercise_count = 0
        
        # Go through each section and get each exercise
        for section_title, section_data in sections.items():
            self.all_data[section_title] = {"exercises": {}}
            
            # Go through each exercise in the section
            for exercise_title, exercise_url in section_data['exercises'].items():
                # Get exercise content
                try:
                    print(f"  Scraping: {section_title} - {exercise_title}")
                    content = self.get_exercise_content(exercise_url)
                    
                    # Check if we got meaningful content
                    if 'question' not in content or not content['question']:
                        print(f"    Warning: No question found for {exercise_title} in {section_title}")
                    if 'answer' not in content or not content['answer']:
                        print(f"    Warning: No answer found for {exercise_title} in {section_title}")
                        
                    self.all_data[section_title]["exercises"][exercise_title] = content
                    
                    # Add a delay to avoid overloading the server
                    time.sleep(delay)
                except Exception as e:
                    print(f"    Error scraping {exercise_url}: {e}")
                    self.all_data[section_title]["exercises"][exercise_title] = {"error": str(e)}
                
                progress_bar.update(1)
                
                # Check if we've reached max_exercises
                exercise_count += 1
                if max_exercises and exercise_count >= max_exercises:
                    progress_bar.close()
                    print(f"Reached maximum number of exercises ({max_exercises})")
                    return
        
        progress_bar.close()
        print("Scraping completed!")
        
    def save_to_json(self, filename="focus_2_workbook.json"):
        """Save all data to a JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.all_data, f, ensure_ascii=False, indent=2)
        print(f"Data saved to {filename}")
        
    def save_to_markdown(self, filename="focus_2_workbook.md"):
        """Save all data to a Markdown file in a clean format for Word"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# FOCUS 2 WORKBOOK - ANSWERS\n\n")
            
            for section_title, section_data in self.all_data.items():
                f.write(f"## {section_title}\n\n")
                
                for exercise_title, exercise_content in section_data['exercises'].items():
                    f.write(f"### {exercise_title}\n\n")
                    
                    if 'answer' in exercise_content and exercise_content['answer']:
                        # Clean up the answer text - remove extra characters
                        answer_text = exercise_content['answer']
                        # Remove numbering like "1." if present at start of lines
                        answer_lines = []
                        for line in answer_text.split('\n'):
                            # Remove list markers and clean up
                            cleaned_line = re.sub(r'^\d+\.\s*', '', line).strip()
                            # Remove bullet points
                            cleaned_line = re.sub(r'^[•\-*]\s*', '', cleaned_line).strip()
                            if cleaned_line:
                                answer_lines.append(cleaned_line)
                        
                        # Write each answer on its own line
                        for line in answer_lines:
                            f.write(f"{line}\n")
                    
                    f.write("\n")  # Add space between exercises
                    
        print(f"Data saved to {filename} in a clean format for copying to Word")
        
    def save_to_text_file(self, filename="focus_2_workbook.txt"):
        """Save all data to a simple text file format for direct copying to Word"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("FOCUS 2 WORKBOOK - ANSWERS\n\n")
            
            for section_title, section_data in self.all_data.items():
                f.write(f"{section_title}\n")
                f.write("="*len(section_title) + "\n\n")
                
                for exercise_title, exercise_content in section_data['exercises'].items():
                    f.write(f"{exercise_title}\n")
                    f.write("-"*len(exercise_title) + "\n\n")
                    
                    if 'answer' in exercise_content and exercise_content['answer']:
                        # Clean up the answer text - remove extra characters
                        answer_text = exercise_content['answer']
                        
                        # Clean up the text
                        answer_lines = []
                        for line in answer_text.split('\n'):
                            # Keep the numbering but clean up extra formatting
                            cleaned_line = line.strip()
                            if cleaned_line:
                                answer_lines.append(cleaned_line)
                        
                        # Write each answer on its own line
                        for line in answer_lines:
                            f.write(f"{line}\n")
                    
                    f.write("\n\n")  # Add space between exercises
                    
        print(f"Data saved to {filename} in a simple text format for copying to Word")

def main():
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Initialize scraper
    scraper = WorkbookScraper()
    
    # Scrape all data (with option to limit for testing)
    test_mode = False
    if test_mode:
        # Only scrape 5 exercises for testing
        scraper.scrape_all(delay=1.5, max_exercises=5)
    else:
        # Scrape all exercises
        scraper.scrape_all(delay=1.5)
    
    # Save data to files
    scraper.save_to_json("data/focus_2_workbook.json")
    scraper.save_to_markdown("data/focus_2_workbook.md")
    scraper.save_to_text_file("data/focus_2_workbook.txt")
    
    print("\nAll done! You can find your files in the 'data' folder.")
    print("For Word, use the 'focus_2_workbook.txt' file for the cleanest format.")

if __name__ == "__main__":
    main()