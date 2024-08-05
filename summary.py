import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load the pre-trained T5 model and tokenizer
model_name = 't5-base'
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)


# Function to summarize a job description and extract requirements using the T5 model
def summarize_job_description(job_description):
    input_text = "summarize: " + job_description

    # Tokenize the input text
    input_ids = tokenizer.encode(input_text, return_tensors='pt', max_length=512, truncation=True)

    # Generate the summary using the T5 model
    summary_ids = model.generate(input_ids, num_beams=4, max_length=400, early_stopping=True)

    # Decode the generated summary
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    # Extract requirements using different keywords
    requirements = extract_requirements(job_description)

    return summary, requirements


# Function to extract requirements from a job description
def extract_requirements(job_description):
    requirement_keywords = ["requirements:", "what you bring:", "your tasks:", "what does it take?",
                            "your tasks with us:", 'requirements for applicant:', 'our requirements for you:',
                            'we expect:', 'your tasks include:', 'your tasks:', 'your requirements:',
                            'desirable are:', 'job requirement:', 'your profile:', 'bring:',
                            'bring…', 'your task:', 'your qualifications:', 'responsibility:', 'your profile',
                            'your skill:', "tasks:", 'skill:', "skills:", 'task:', 'my profile:',
                            'you:']

    for keyword in requirement_keywords:
        requirements_section = job_description.lower().split(keyword)
        if len(requirements_section) > 1:
            requirements_text = requirements_section[1]
            requirements = [line.strip() for line in requirements_text.split('\n') if line.strip()]
            return requirements

    return []


# Read the UTF-8 text file and split the job descriptions
with open('job.txt', 'r', encoding='utf-8') as file:
    file_content = file.read()
    job_descriptions = file_content.split('-----')

# Prepare the file for writing
output_file = 'output.txt'
with open(output_file, 'w', encoding='utf-8') as outfile:
    # Process each job description
    for i, job_description in enumerate(job_descriptions, start=1):  # Start numbering from 1
        if job_description.strip():
            summary, requirements = summarize_job_description(job_description)

            # Print and write summary
            summary_title = f"Summary for Job {i}:"
            print(summary_title)
            print(summary)
            print("--------------------")
            outfile.write(summary_title + "\n")
            outfile.write(summary + "\n")
            outfile.write("--------------------\n")

            # Print and write requirements
            requirements_title = f"Requirements for Job {i}:"
            print(requirements_title)
            outfile.write(requirements_title + "\n")  # Write requirements title
            for requirement in requirements:
                print("- " + requirement)
                outfile.write("- " + requirement + "\n")
            print("--------------------")
            outfile.write("--------------------\n")

print(f"Summaries and requirements saved to {output_file}.")
