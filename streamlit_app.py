import streamlit as st
import requests

APOLLO_ENRICH_API_URL = "https://api.apollo.io/v1/people/match"

def enrich_apollo(email):
    headers = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache"
    }
    
    payload = {
        "api_key": st.secrets.apollo_api,
        "email": email
    }
    
    response = requests.post(APOLLO_ENRICH_API_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

def main():
    st.title("Apollo.io Email Enrichment App")

    email = st.text_input("Enter a business email address to enrich")

    if st.button("Enrich"):
        if email:
            with st.spinner("Enriching..."):
                result = enrich_apollo(email)
                
            if result and result.get('person'):
                person = result['person']
                organization = person.get('organization', {})
                
                st.header("Enrichment Results")
                
                # Person Information
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
                
                # Company Information
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

            elif result:
                st.warning("No enrichment data found for this email address.")
            else:
                st.error("Error occurred while fetching data from Apollo.io API.")
        else:
            st.warning("Please enter an email address.")

if __name__ == "__main__":
    main()
