import datetime
from google import genai
from tools import NewsToolkit

class NewsAgent:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        self.tools = NewsToolkit()

    def generate_broadcast(self, subject):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        sources = self.tools.search_topics(subject)
        if not sources:
            return "No recent news found for this topic.", []
        context = ""
        for src in sources:
            content = self.tools.fetch_article_content(src['url'])
            context += f"\n[SOURCE: {src['title']}]: {content[:1500]}\n"

        prompt = f"""
        Current Date/Time: {current_time}
        Topic: {subject}
        
        Using the LATEST NEWS SOURCE data provided below, write a professional 30-second news script. 
        Focus on facts from the last hour. If the data is older, mention that.
        
        DATA:
        {context}
        """
    
        response = self.client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt
        )
        return response.text, sources