import streamlit as st
import requests
import json

# API endpoints and keys
APOLLO_ENRICH_API_URL = "https://api.apollo.io/v1/people/match"
ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"

# Assuming you're storing API keys in Streamlit secrets
APOLLO_API_KEY = st.secrets["apollo_api"]
ANTHROPIC_API_KEY = st.secrets["anthropic_api"]

def enrich_apollo(email):
    headers = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache"
    }
    
    payload = {
        "api_key": APOLLO_API_KEY,
        "email": email
    }
    
    response = requests.post(APOLLO_ENRICH_API_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

def extend_keywords(industry):
    prompt = f"""Generate a comprehensive list of keywords for {industry} software development services. Include:
1. Core software development terms specific to the industry
2. Types of software applications commonly used in the industry
3. Industry-specific processes or systems that might need software solutions
4. Data management and analytics keywords relevant to the industry
5. Integration services for popular software used in the industry
6. Emerging technologies being adopted in the industry
7. Compliance and security-related software needs
8. Cloud and mobile solutions specific to the industry
9. Automation and AI applications in the industry
10. Software for improving efficiency or solving common industry problems

For each category, provide at least 10-20 specific, targeted keywords or phrases that potential clients in this industry might use when searching for software development services."""

    headers = {
        'Content-Type': 'application/json',
        'x-api-key': ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01'
    }
    
    payload = {
        "model": "claude-3-5-sonnet-20240620",
        "max_tokens": 3000,
        "messages": [{"role": "user", "content": prompt}]
    }
    
    response = requests.post(ANTHROPIC_API_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()['content'][0]['text']
    else:
        return None

def display_person_info(person):
    st.subheader("Person Information")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Name:** {person.get('name', 'N/A')}")
        st.write(f"**Title:** {person.get('title', 'N/A')}")
        st.write(f"**Seniority:** {person.get('seniority', 'N/A')}")
        st.write(f"**Departments:** {', '.join(person.get('departments', ['N/A']))}")
    with col2:
        st.write(f"**LinkedIn:** {person.get('linkedin_url', 'N/A')}")
        st.write(f"**Twitter:** {person.get('twitter_url', 'N/A')}")
        if person.get('phone_numbers'):
            st.write("**Phone Numbers:**")
            for phone in person['phone_numbers']:
                st.write(f"- {phone}")
        else:
            st.write("**Phone Numbers:** N/A")

def display_company_info(organization):
    st.subheader("Company Information")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Company Name:** {organization.get('name', 'N/A')}")
        st.write(f"**Website:** {organization.get('website_url', 'N/A')}")
        st.write(f"**HQ Location:** {organization.get('city', 'N/A')}, {organization.get('state', 'N/A')}, {organization.get('country', 'N/A')}")
        st.write(f"**Industry:** {organization.get('industry', 'N/A')}")
    with col2:
        st.write(f"**Employees:** {organization.get('estimated_num_employees', 'N/A')}")
        st.write(f"**Annual Revenue:** ${organization.get('estimated_annual_revenue', 'N/A')}")
        st.write(f"**Total Funding:** ${organization.get('total_funding', 'N/A')}")
        st.write(f"**Latest Funding:** {organization.get('latest_funding_round_type', 'N/A')}")
    
    st.write(f"**Keywords:** {', '.join(organization.get('keywords', ['N/A']))}")

def email_enricher():
    st.subheader("Email Enricher (Using Apollo API)")
    email = st.text_input("Enter a business email address to enrich")

    if st.button("Lookup Email"):
        if email:
            with st.spinner("Looking up email..."):
                result = enrich_apollo(email)
                
            if result and result.get('person'):
                st.success("Email lookup successful!")
                person = result['person']
                organization = person.get('organization', {})
                
                display_person_info(person)
                display_company_info(organization)
            elif result:
                st.warning("No enrichment data found for this email address.")
            else:
                st.error("Error occurred while fetching data from Apollo API.")
        else:
            st.warning("Please enter an email address.")

def keyword_extender():
    st.subheader("Keyword Extender (Using Anthropic API)")
    industry = st.text_input("Enter an industry for keyword extension")

    if st.button("Extend Keywords"):
        if industry:
            with st.spinner("Extending keywords..."):
                keywords = extend_keywords(industry)
                
            if keywords:
                st.success("Keywords extended successfully!")
                st.text_area("Extended Keywords", keywords, height=300)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Copy Keywords"):
                        st.write("Keywords copied to clipboard!")
                        st.session_state.clipboard = keywords
                with col2:
                    if st.download_button("Save as TXT", keywords, file_name="extended_keywords.txt"):
                        st.write("Keywords saved as TXT file!")
            else:
                st.error("Error occurred while extending keywords.")
        else:
            st.warning("Please enter an industry.")

def main():
    st.title("Multi-Service Enrichment App")

    tab1, tab2 = st.tabs(["Email Enricher", "Keyword Extender"])

    with tab1:
        email_enricher()

    with tab2:
        keyword_extender()

if __name__ == "__main__":
    main()
