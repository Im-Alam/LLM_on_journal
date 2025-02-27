import os
import requests
import feedparser

# Define search parameters
categories = ["cs.CV", "cs.CL"]  # AI and Machine Learning categories
year = "2025"
max_results = 20  # Change as needed
output_folder = "ML_arxiv_papers_2025"

# Create output folder if not exists
os.makedirs(output_folder, exist_ok=True)

for category in categories:
    print(f"\n🔍 Fetching papers for category: {category}")
    
    # arXiv API URL
    api_url = f"http://export.arxiv.org/api/query?search_query=cat:{category}&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"

    # Fetch data from arXiv
    feed = feedparser.parse(api_url)

    for entry in feed.entries:
        published_year = entry.published[:4]  # Extract year (YYYY-MM-DD format)

        if published_year == year:
            title = entry.title.replace(" ", "_").replace("/", "_")[:50]  # Safe filename
            pdf_url = entry.link.replace("abs", "pdf") + ".pdf"
            pdf_path = os.path.join(output_folder, f"{title}.pdf")

            print(f"📥 Downloading: {entry.title}")

            # Download PDF
            response = requests.get(pdf_url)
            if response.status_code == 200:
                with open(pdf_path, "wb") as f:
                    f.write(response.content)
                print(f"✅ Saved: {pdf_path}")
            else:
                print(f"❌ Failed to download: {pdf_url}")

print("\n🎉 Download complete!")
