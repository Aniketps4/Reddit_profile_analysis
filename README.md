## Setup

### Prerequisites
- **Python 3.8 or higher**: Ensure Python is installed. Verify with:python --version
-  **Required Libraries**:
- `praw`: For Reddit API interaction.
- `python-docx`: For generating Word documents.
Install them using pip:pip install praw python-docx
- **Reddit API Credentials**: Obtain a Reddit API client ID, client secret, and user agent from [Reddit App Preferences](https://www.reddit.com/prefs/apps). Replace the placeholder credentials in `scrape_reddit.py` with your own:
- `client_id`
- `client_secret`
- `user_agent`

### Directory Structure
- `scrape_reddit.py`: Script to scrape Reddit data and save it as JSON.
- `generate_persona_word.py`: Script to process JSON data and generate a Word document.
- `Hungry-Move-6603_data.json`: Scraped data for user `Hungry-Move-6603`.
- `kojied_data.json`: Scraped data for user `kojied`.
- `Hungry-Move-6603_persona.docx`: Generated persona document for `Hungry-Move-6603`.
- `kojied_persona.docx`: Generated persona document for `kojied`.
- `ReadMe.md`: This file.

## How to Execute the Code

### Step 1: Scrape Reddit Data
1. **Navigate to the Project Directory**:
2. **Run the Scraping Script**:
- For `Hungry-Move-6603`:"C:/Users/anike/PostgreSQL/17/pgAdmin 4/python/python.exe" scrape_reddit.py https://www.reddit.com/user/Hungry-Move-6603/
-  For `kojied`:"C:/Users/anike/PostgreSQL/17/pgAdmin 4/python/python.exe" generate_persona_word.py kojied_data.json
3. **Verify Output**:
- Check for `Hungry-Move-6603_data.json` and `kojied_data.json` in the directory. The terminal will display scraped posts and comments for debugging.

### Step 2: Generate Persona Word Document
1. **Run the Generation Script**:
- For `Hungry-Move-6603`:"C:/Users/anike/PostgreSQL/17/pgAdmin 4/python/python.exe" generate_persona_word.py Hungry-Move-6603_data.json
-  For `kojied`:"C:/Users/anike/PostgreSQL/17/pgAdmin 4/python/python.exe" generate_persona_word.py kojied_data.json
 
2. **Verify Output**:
- Check for `Hungry-Move-6603_persona.docx` and `kojied_persona.docx`. Open the files to review the generated personas.

### Troubleshooting
- **Missing Argument Error**: Ensure the URL is provided when running `scrape_reddit.py`.
- **Permission Issues**: Run Git Bash as Administrator if access is denied.
- **Dependency Errors**: Verify all libraries are installed and compatible.

## Approach Used to Complete the Task

### Overview
The task was to scrape Reddit data for users `Hungry-Move-6603` and `kojied` and generate a persona document without hardcoding the output. The solution was divided into two scripts to separate data collection and processing, ensuring modularity and scalability.

### Step-by-Step Approach
1. **Data Scraping**:
- Used the `praw` library to interact with the Reddit API.
- Scraped up to 10 recent posts and 20 recent comments for each user.
- Saved the data as JSON files (`username_data.json`) to preserve the raw scraped content for dynamic processing.
- Included error handling and UTF-8 encoding to manage Unicode characters.

2. **Persona Generation**:
- Developed `generate_persona_word.py` to read the JSON files and build a persona dynamically.
- Inferred basic info (e.g., location, occupation) from posts containing keywords like "lucknow" or "business".
- Calculated motivations (e.g., wellness, dietary needs) by counting keyword occurrences across all text.
- Determined personality traits (e.g., feeling, intuition) based on emotional cues (e.g., "😂") and future-oriented language (e.g., "shift").
- Identified behaviors, frustrations, and goals from comments using keyword matching (e.g., "cook" for habits, "cop" for frustrations).
- Simulated an LLM with `analyze_text_for_themes` to detect dominant themes (e.g., health, location) and generate a custom quote, enhancing the persona’s narrative.

3. **Word Document Output**:
- Utilized `python-docx` to create a structured Word document with sections for each persona attribute.
- Ensured citations were included for all inferred data, linking back to the original Reddit URLs.

### Key Features
- **Dynamic Processing**: Avoided hardcoding by processing live scraped data, making the solution adaptable to new users.
- **LLM Simulation**: The theme-based quote generation mimics an LLM’s summarization, though a real LLM (e.g., via xAI’s API) could be integrated for advanced insights.
- **Modularity**: Separating scraping and generation allows independent execution and testing.

### Limitations and Future Improvements
- **Citation Accuracy**: The script prioritizes the first matching URL, which may not always be the most relevant source. Future work could rank citations by context.
- **LLM Integration**: The current simulation is basic. Integrating a real LLM (e.g., Grok via xAI’s API) could improve quote quality and persona depth.
- **Error Handling**: Enhanced error handling for API rate limits or missing data could improve robustness.

