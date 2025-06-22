import streamlit as st
import requests

st.set_page_config(
    page_title="SaaS Market Intelligence Tool",
    layout="centered",
    initial_sidebar_state="expanded",
)
st.title("🧠 SaaS Market Intelligence Tool")
st.sidebar.header("🛠️ Settings")

api_key = st.sidebar.text_input("Your OpenAI API Key", type="password")
mode = st.sidebar.radio(
    "Choose analysis mode", ["Offer Clarity Analyzer", "Competitor Page Breakdown"]
)
url = st.text_input(
    "Enter a SaaS web page URL below & OpenAi API key in the sidebar",
    placeholder="https://example.com",
)

SCRAPE_API_URL = "https://saas-intel-backend.onrender.com/scrape"
ANALYZE_API_URL = "https://saas-intel-backend.onrender.com/analyze"

if st.button("Run Analysis"):
    if not url or not api_key:
        st.error("Please enter both the URL and your OpenAI API key.")
    else:
        with st.spinner("Scraping homepage..."):
            try:
                scrape_response = requests.post(SCRAPE_API_URL, json={"url": url})
                scrape_json = scrape_response.json()

                if scrape_response.status_code != 200 or "text" not in scrape_json:
                    st.error(
                        f"Error scraping site: {scrape_json.get('error', 'Unknown error')}"
                    )
                    st.stop()

                scraped_text = scrape_json["text"]

                with st.spinner("Running GPT analysis..."):
                    payload = {
                        "text": scraped_text,
                        "mode": "clarity" if "Clarity" in mode else "competitor",
                        "api_key": api_key,
                    }
                    analyze_response = requests.post(ANALYZE_API_URL, json=payload)
                    analyze_json = analyze_response.json()

                    if analyze_response.status_code == 200:
                        result = analyze_json.get("result", "").strip()
                        if result:
                            st.success("✅ Analysis Complete")
                            st.markdown(
                                "### 🧠 GPT-4 Analysis Output", unsafe_allow_html=True
                            )
                            st.markdown(result, unsafe_allow_html=True)
                        else:
                            st.warning("⚠️ GPT returned an empty result.")
                    else:
                        st.error(
                            f"❌ Error: {analyze_response.status_code} - {analyze_json.get('error', 'Unknown error')}"
                        )

            except Exception as e:
                st.error(f"❌ Exception occurred: {str(e)}")

st.markdown(
    "<p style='font-size: 1rem; color: #ccc;'>"
    "For a full walkthrough of this project, visit: "
    "<a href='https://codebynight.dev' target='_blank' style='color: #ccc; text-decoration: underline;'>"
    "codebynight.dev</a></p>",
    unsafe_allow_html=True,
)
st.caption("Built with ❤️ for Marketers using Streamlit + FastAPI + GPT-4o-mini")
