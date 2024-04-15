#Import required libraries
import os
import pandas as pd
import google.generativeai as genai
import chardet
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Gemini API key from environment variables
gemini_API_Key = os.getenv("gemini_API_Key")

# Configure the GenerativeAI API with the Gemini API key
genai.configure(api_key=gemini_API_Key)

# Create a GenerativeModel object with the Gemini model version
model = genai.GenerativeModel('gemini-1.0-pro')

# Get the file path from environment variables
filePath = os.getenv("csv_path")

# Read the CSV file using pandas
df = pd.read_csv(filePath)

# Detect the encoding of the file
with open(filePath, 'rb') as file:
    result = chardet.detect(file.read())

encoding = result['encoding']

# Read the CSV file again with the detected encoding
df = pd.read_csv(filePath, encoding=encoding)

response_texts = []

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    try:
        # Create a prompt using the data from the row
        prompt = f"The following data consists of information regarding the {row['table_page_title']} mainly focusing on {row['table_section_title']}. The data is {row['table_array']}. With the information provided, answer the following question: {row['question']}. If it is a question that requires mathematical operations, calculate them and give the result\n"
        
        # Generate content using the prompt with the GenerativeModel
        response = model.generate_content(prompt)
        
        # Append the generated response to the response_texts list
        response_texts.append(response.text)
        
    except:
        # If an exception occurs, append a default message to the response_texts list
        response_texts.append("The data is not sufficient to provide the answer")

# Add the response_texts as a new column in the DataFrame
df['response'] = response_texts

# Define the output file path
output_file = '/testDataSolution.csv'

# Save the DataFrame as a CSV file without the index column
df.to_csv(output_file, index=False)