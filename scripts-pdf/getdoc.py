import os
import requests
from PyPDF2 import PdfMerger

# URL of the website containing the JSON response
base_url = "https://www.bop.gov/PublicInfo/execute/policysearch/index.jsp?todo=query&output=json&name=&series=&type=&sortBy=&sortDescending="

# Create a directory to store downloaded PDFs
if not os.path.exists("downloaded_pdfs"):
    os.makedirs("downloaded_pdfs")

# Fetch the JSON response
response = requests.get(base_url)
json_data = response.json()

# List to store downloaded PDF filenames
pdf_filenames = []


# Function to download PDFs
def download_pdf(url):
    response = requests.get(url)
    if response.status_code == 200:
        pdf_filename = url.split("/")[-1]
        pdf_path = os.path.join("downloaded_pdfs", pdf_filename)
        with open(pdf_path, "wb") as pdf_file:
            pdf_file.write(response.content)
        pdf_filenames.append(pdf_path)
        print(f"Downloaded: {pdf_filename}")
    else:
        print(f"Failed to download: {url}")


# Download PDFs based on the JSON response
for policy in json_data.get("Policies", []):
    pdf_url = "https://www.bop.gov" + policy.get("url")
    download_pdf(pdf_url)

# Combine downloaded PDFs into a single PDF
pdf_merger = PdfMerger()

for pdf_filename in pdf_filenames:
    pdf_merger.append(pdf_filename)

combined_pdf_path = "combined_pdfs.pdf"
pdf_merger.write(combined_pdf_path)
pdf_merger.close()

print(f"All PDFs combined into: {combined_pdf_path}")
