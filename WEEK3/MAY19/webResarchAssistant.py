import asyncio
import os
import textwrap
from dotenv import load_dotenv

# Selenium imports for web browsing
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# BeautifulSoup for HTML parsing
from bs4 import BeautifulSoup

# LangChain imports
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate

# Load environment variables from .env file
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# --- 1. Initialize LLM ---
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)

# --- 2. Build the Tools ---

async def _fetch_page_source_with_selenium(url: str) -> str:
    """
    Blocking Selenium call wrapped to run in executor.
    Returns the full page source HTML as a string.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/91.0.4472.124 Safari/537.36"
    )

    driver = None
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(30)
        driver.get(url)

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        return driver.page_source

    finally:
        if driver:
            driver.quit()

@tool
async def web_browser(url: str) -> str:
    """
    Async wrapper tool for fetching and extracting main text content from a URL.
    Runs blocking Selenium code in a thread executor to avoid blocking event loop.
    """
    try:
        page_source = await asyncio.to_thread(_fetch_page_source_with_selenium, url)
    except TimeoutException:
        print(f"Timeout while loading {url}")
        return f"Error: Page load timed out for {url}"
    except WebDriverException as e:
        print(f"WebDriver error for {url}: {e}")
        return f"Error: WebDriver encountered an issue for {url}. {e}"
    except Exception as e:
        print(f"Unexpected error for {url}: {e}")
        return f"Error: An unexpected error occurred while fetching {url}. {e}"

    # Parse page source for main textual content
    soup = BeautifulSoup(page_source, "html.parser")

    main_content_tags = ["article", "main", "div", "p"]
    text_content = ""
    for tag_name in main_content_tags:
        tag = soup.find(tag_name)
        if tag:
            # If tag is article or main, get all <p> text inside it for better content
            if tag_name in ("article", "main"):
                paragraphs = tag.find_all("p")
                if paragraphs:
                    text_content = "\n".join(p.get_text(strip=True) for p in paragraphs)
                else:
                    text_content = tag.get_text(separator="\n", strip=True)
            else:
                text_content = tag.get_text(separator="\n", strip=True)

            if text_content:
                break

    if not text_content and soup.body:
        text_content = soup.body.get_text(separator="\n", strip=True)

    # Clean up excessive whitespace and newlines
    lines = [line.strip() for line in text_content.splitlines() if line.strip()]
    text_content = "\n".join(lines)
    text_content = text_content.replace("  ", " ").replace("\n\n", "\n").strip()

    print(f"Web content fetched from {url}, length: {len(text_content)} characters.")
    return text_content[:40000]  # limit length for LLM

@tool
async def text_summarizer(text_content: str) -> str:
    """
    Uses LLM to generate a concise summary of the provided text content.
    """
    if not text_content or len(text_content.strip()) < 50:
        return "Not enough content to summarize effectively."

    prompt_template = PromptTemplate(
        input_variables=["text"],
        template=textwrap.dedent("""
            You are an expert summarizer. Your goal is to provide a concise, high-quality, and informative summary of the given text.
            Focus on the main points, key facts, and essential information.
            The summary should be no more than 300 words.

            Text to summarize:
            ---
            {text}
            ---

            Concise Summary:
        """),
    )

    chain = prompt_template | llm

    try:
        response = await chain.ainvoke({"text": text_content})
        summary = response.content
        print(f"Text summarized. Summary length: {len(summary)} characters.")
        return summary
    except Exception as e:
        print(f"Error during summarization: {e}")
        return f"Error: Failed to summarize text. {e}"

# --- 3. Define Agents ---

researcher_prompt_template_str = textwrap.dedent("""
    You are a diligent Researcher agent. Your sole purpose is to fetch raw web content.
    You have access to the following tool:
    {tools}

    To achieve your goal, you *must* follow this format:

    Question: The URL for which to fetch content.
    Thought: You should always think about what action to take. Your only action is to use the `web_browser` tool.
    Action: the action to take, should be one of [{tool_names}]
    Action Input: The URL to browse.
    Observation: The raw content fetched by the tool.
    Thought: I have fetched the content. My final answer is the raw content.
    Final Answer: The raw content.

    Begin!

    Question: Fetch content from {input}
    Thought:{agent_scratchpad}
""")

researcher_prompt = PromptTemplate.from_template(researcher_prompt_template_str)

researcher_agent = create_react_agent(llm, [web_browser], researcher_prompt)
researcher_executor = AgentExecutor(agent=researcher_agent, tools=[web_browser], verbose=False)

summarizer_prompt_template_str = textwrap.dedent("""
    You are an expert Summarizer agent. Your sole purpose is to provide a concise, high-quality, and informative summary of the given text.
    You have access to the following tool:
    {tools}

    To achieve your goal, you *must* follow this format:

    Question: The text content that needs to be summarized.
    Thought: You should always think about what action to take. Your only action is to use the `text_summarizer` tool.
    Action: the action to take, should be one of [{tool_names}]
    Action Input: The text to summarize.
    Observation: The concise summary generated by the tool.
    Thought: I have summarized the content. My final answer is the concise summary.
    Final Answer: The concise summary.

    Begin!

    Question: Summarize the following content: {input}
    Thought:{agent_scratchpad}
""")

summarizer_prompt = PromptTemplate.from_template(summarizer_prompt_template_str)

summarizer_agent = create_react_agent(llm, [text_summarizer], summarizer_prompt)
summarizer_executor = AgentExecutor(agent=summarizer_agent, tools=[text_summarizer], verbose=False)

# --- 4. Orchestration ---

class WebResearchAssistant:
    def __init__(self):
        self.researcher_executor = researcher_executor
        self.summarizer_executor = summarizer_executor

    async def run_research_and_summarize(self, url: str) -> str:
        print(f"\n--- Web Research Assistant Initiated for URL: {url} ---")

        try:
            print("\n--- Researcher Agent: Fetching web content... ---")
            research_result = await self.researcher_executor.ainvoke({"input": url})
            fetched_content = research_result['output']

            if "Error:" in fetched_content:
                print(f"Researcher Agent reported an error: {fetched_content}")
                return f"Failed to fetch content: {fetched_content}"

            if not fetched_content or len(fetched_content.strip()) < 50:
                print("Researcher Agent fetched insufficient content.")
                return "Failed to fetch substantial content for summarization. Content might be empty or too short."

            print(f"--- Researcher Agent: Content fetched (length: {len(fetched_content)} characters). ---")

            print("\n--- Summarizer Agent: Generating summary... ---")
            summarized_result = await self.summarizer_executor.ainvoke({"input": fetched_content})
            final_summary = summarized_result['output']

            if "Error:" in final_summary:
                print(f"Summarizer Agent reported an error: {final_summary}")
                return f"Failed to summarize content: {final_summary}"

            print("\n--- Process Complete! ---")
            return final_summary

        except Exception as e:
            print(f"An unhandled error occurred during orchestration: {e}")
            return f"An unhandled error occurred during the process: {e}"

# --- Main execution ---

async def main():
    assistant = WebResearchAssistant()

    urls_to_process = [
        "https://www.nasa.gov/news-release/nasa-and-us-spacewalkers-prepare-for-iss-power-upgrade-spacewalk/",
        "https://en.wikipedia.org/wiki/Large_language_model",
        "https://www.bbc.com/news/world-us-canada-69022634",
        "https://www.nytimes.com/2024/05/17/technology/ai-models-text-data-shortage.html"
    ]

    for url in urls_to_process:
        print(f"\n{'='*20} Processing URL: {url} {'='*20}")
        summary = await assistant.run_research_and_summarize(url)
        print(f"\nFinal Summary for {url}:\n{summary}")
        print(f"\n{'='*80}\n")

if __name__ == "__main__":
    if not os.getenv("GOOGLE_API_KEY"):
        print("Error: GOOGLE_API_KEY environment variable not found.")
        print("Please set it in your .env file or system environment variables.")
    else:
        asyncio.run(main())
