import streamlit as st
import requests

# Apollo.io Enrich API endpoint
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

    # Input for email
    email = st.text_input("Enter an email address to enrich")

    if st.button("Enrich"):
        if email:
            with st.spinner("Enriching..."):
                result = enrich_apollo(email)
                
            if result and result.get('person'):
                person = result['person']
                st.subheader("Enrichment Results")
                st.write(f"Name: {person.get('name', 'N/A')}")
                st.write(f"First Name: {person.get('first_name', 'N/A')}")
                st.write(f"Last Name: {person.get('last_name', 'N/A')}")
                st.write(f"Title: {person.get('title', 'N/A')}")
                st.write(f"Company: {person.get('organization', {}).get('name', 'N/A')}")
                st.write(f"LinkedIn URL: {person.get('linkedin_url', 'N/A')}")
                st.write(f"Location: {person.get('city', 'N/A')}, {person.get('state', 'N/A')}, {person.get('country', 'N/A')}")
                st.write(f"Industry: {person.get('industry', 'N/A')}")
                st.write(f"Twitter URL: {person.get('twitter_url', 'N/A')}")
                
                if person.get('phone_numbers'):
                    st.write("Phone Numbers:")
                    for phone in person['phone_numbers']:
                        st.write(f"- {phone}")
            elif result:
                st.warning("No enrichment data found for this email address.")
            else:
                st.error("Error occurred while fetching data from Apollo.io API.")
        else:
            st.warning("Please enter an email address.")

if __name__ == "__main__":
    main()
