import streamlit as st
import requests

# Apollo.io API endpoint
APOLLO_API_URL = "https://api.apollo.io/v1/people/search"

def search_apollo(email):
    headers = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache"
    }
    
    payload = {
        "api_key": st.secrets.apollo_api,
        "email": email
    }
    
    response = requests.post(APOLLO_API_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

def main():
    st.title("Apollo.io Email Search App")

    # Input for email
    email = st.text_input("Enter an email address to search")

    if st.button("Search"):
        if email:
            with st.spinner("Searching..."):
                result = search_apollo(email)
                
            if result:
                if result['people']:
                    person = result['people'][0]
                    st.subheader("Search Results")
                    st.write(f"Name: {person.get('name', 'N/A')}")
                    st.write(f"Title: {person.get('title', 'N/A')}")
                    st.write(f"Company: {person.get('organization', {}).get('name', 'N/A')}")
                    st.write(f"LinkedIn URL: {person.get('linkedin_url', 'N/A')}")
                    st.write(f"Location: {person.get('city', 'N/A')}, {person.get('state', 'N/A')}, {person.get('country', 'N/A')}")
                else:
                    st.warning("No results found for this email address.")
            else:
                st.error("Error occurred while fetching data from Apollo.io API.")
        else:
            st.warning("Please enter an email address.")

if __name__ == "__main__":
    main()
