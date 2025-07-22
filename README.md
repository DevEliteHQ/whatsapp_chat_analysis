# WhatsApp Chat Analysis

A Streamlit web application that provides detailed analysis and visualization of WhatsApp chat data. This tool helps you understand chat patterns, user engagement, and communication trends in your WhatsApp conversations.

## Features

- Upload and analyze WhatsApp chat export files
- View comprehensive chat statistics including:
  - Total number of messages
  - Total word count
  - Media files shared
  - Links shared
- User-specific analysis
- Interactive visualizations
- Support for both individual and group chats

## Requirements

- Python 3.x
- Required packages:
  ```
  streamlit
  pandas
  numpy
  matplotlib
  seaborn
  wordcloud
  urlextract
  emoji
  ```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/whatsapp_chat_analysis.git
   cd whatsapp_chat_analysis
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Export your WhatsApp chat:
   - Open WhatsApp
   - Go to the chat you want to analyze
   - Click on the three dots (⋮) > More > Export chat
   - Choose 'Without Media'
   - Save the exported .txt file

2. Run the application:
   ```bash
   streamlit run app.py
   ```

3. Use the application:
   - Upload your chat file using the sidebar
   - Select a user for specific analysis (or "Overall" for complete chat analysis)
   - Click "Show Analysis" to view the results

## Project Structure

- `app.py`: Main Streamlit application file
- `preprocessor.py`: Contains functions for data preprocessing
- `helper.py`: Helper functions for analysis and visualization
- `requirements.txt`: List of Python dependencies
- `stop_hinglish.txt`: Custom stopwords for text analysis
- `analysis/`: Contains Jupyter notebooks for development and testing
