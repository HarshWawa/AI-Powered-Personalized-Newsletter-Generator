import streamlit as st
import feedparser
import spacy.cli


from newspaper import Article
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import os
from dotenv import load_dotenv

load_dotenv()
apikey = os.getenv("groqPass")


# Load spaCy model
spacy.cli.download("en_core_web_md")
nlp = spacy.load("en_core_web_md")

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=apikey,
)

# Function: NLP-based relevance filter
def is_relevant_article(article_text, interest_phrases, threshold=0.55):
    doc1 = nlp(article_text.lower())
    for phrase in interest_phrases:
        doc2 = nlp(phrase.lower())
        if doc1.similarity(doc2) > threshold:
            return True
    return False

# Function: Extract full article text
def extract_full_article_text(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except:
        return "⚠️ Failed to extract article content."

# Function: Summarize article using Groq
def summarize_article_groq(content):
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "Summarize the following article in 3-4 concise sentences:\n\n." + content + "\n\n Only PROVIDE THE SUMMARY NOTHING ELSE.") 
    ])
    chain = prompt_template | llm | StrOutputParser()
    try:
        return chain.invoke({})
    except:
        return "⚠️ Summary could not be generated."

# Function: Generate highlights from summaries
def generate_highlights_groq(summaries):
    joined = "\n\n".join([f"Title: {s['title']}\nSummary: {s['summary']}" for s in summaries])
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "Given the following list of summarized articles, write a short highlight section summarizing the key trends or stories:\n"+joined)
    ])
    chain = prompt_template | llm | StrOutputParser()
    try:
        return chain.invoke({})
    except:
        return "⚠️ Highlights unavailable."

# Function: Generate newsletter markdown
def generate_md_with_highlights(persona_name, summaries, highlight_text):
    md = f"# 📰 {persona_name}'s Personalized Newsletter\n\n"
    md += "## 🔥 Highlights\n"
    md += highlight_text + "\n\n---\n"

    for article in summaries:
        md += f"## [{article['title']}]({article['link']})\n"
        md += f"*Source:* {article['source']}\n\n"
        md += f"{article['summary']}\n\n"
        md += "---\n"

    return md

# Persona profiles
persona_profiles = {

    "Alex Parker (Tech Enthusiast, USA)": {
        "interests": ["AI", "cybersecurity", "blockchain", "startups","programming"],
        "feeds": [
            "https://techcrunch.com/feed/",

        ]
    },
    "Priya Sharma (Finance & Business Guru, India)": {
        "interests": ["global markets", "startups", "fintech", "cryptocurrency", "economics"],
        "feeds": [
            # "https://www.ft.com/emerging-markets?format=rss",
            "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114",

        ]
    },
    "Marco Rossi (Sports Journalist, Italy)": {
        "interests": ["football", "F1", "NBA", "Olympic sports", "esports"],
        "feeds": [
            "https://feeds.bbci.co.uk/sport/rss.xml",

        ]
    },
    "Lisa Thompson (Entertainment Buff, UK)": {
        "interests": ["movies", "celebrity news", "TV shows", "music", "books"],
        "feeds": [
            "https://www.billboard.com/feed/",

        ]
    },
    "David Martinez (Science & Space Nerd, Spain)": {
        "interests": ["space exploration", "AI", "biotech", "physics", "renewable energy"],
        "feeds": [
            "https://www.nasa.gov/feed/",
        ]
    }
}


# Streamlit UI
st.set_page_config(page_title="AI Newsletter Generator", layout="centered")
st.title("📰 AI-Powered Personalized Newsletter Generator")

selected_persona = st.selectbox("👤 Choose a User Persona", list(persona_profiles.keys()))
profile = persona_profiles[selected_persona]
st.markdown(f"**Interests:** {', '.join(profile['interests'])}")

if st.button("📡 Fetch & Filter Articles"):
    with st.spinner("🔎 Fetching and filtering articles..."):
        articles = []
        for url in profile["feeds"]:
            feed = feedparser.parse(url)
            for entry in feed.entries[:15]:
                title = entry.title
                summary = entry.get("summary", "")
                full_text = f"{title} {summary}"
                if is_relevant_article(full_text, profile["interests"]):
                    articles.append({
                        "title": title,
                        "link": entry.link,
                        "summary": summary,
                        "source": url
                    })

    if articles:
        st.success(f"✅ Found {len(articles)} relevant articles.")

        # ✅ Show articles in UI
        for article in articles:
            st.markdown(f"### [{article['title']}]({article['link']})")
            st.markdown(f"*Source:* {article['source']}")
            st.markdown(f"{article['summary'][:300]}...")
            st.markdown("---")

        # 🧠 Summarize articles and generate .md
        summarized_articles = []
        with st.spinner("🧠 Extracting & summarizing articles..."):
            for article in articles:
                content = extract_full_article_text(article["link"])
                summary = summarize_article_groq(content)
                summarized_articles.append({
                    "title": article["title"],
                    "link": article["link"],
                    "summary": summary,
                    "source": article["source"]
                })

        with st.spinner("✨ Generating highlights..."):
            print()
            highlights = generate_highlights_groq(summarized_articles)
            

        newsletter_md = generate_md_with_highlights(selected_persona, summarized_articles, highlights)

        # ✅ Download button
        st.download_button(
            label="📥 Download Markdown Newsletter",
            data=newsletter_md,
            file_name="newsletter.md",
            mime="text/markdown"
        )

    else:
        st.warning("⚠️ No relevant articles found.")

