from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import time
import openai

app = Flask(__name__)
CORS(app)

# Set up OpenAI client with Groq's base URL
client = openai.OpenAI(
    api_key="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",
    base_url="https://api.groq.com/openai/v1"  # Groq OpenAI-compatible base URL
)

# Information related to Lion Pro Dev
LION_PRO_DEV_INFO = """
Lion Pro Dev is a leading software development company specializing in:
1. Custom Software Development
2. Web Design & Development
3. Mobile Application Development
4. Cloud Solutions
5. Digital Marketing

We provide high-quality, tailor-made solutions to help businesses grow, utilizing cutting-edge technologies.
Contact us at:
- Email: contact@lionprodev.com

Our team of experts is here to help you build your dream project!

Core Services:
1. Web Development: Custom websites, eCommerce platforms, and responsive web design tailored to your business needs.
   - Service offerings: Full stack HTML, CSS, JavaScript, WordPress, PHP, react, flask, next and more.

2. Mobile App Development: Design and development of intuitive, high-performance mobile apps for iOS and Android platforms.
   - Service offerings: Native iOS/Android apps, Hybrid apps, App maintenance.

3. AI & ML Solutions: Leveraging Artificial Intelligence and Machine Learning to automate processes and improve decision-making.
   - Service offerings: Predictive analytics, data-driven decision-making tools, AI-powered chatbots.

4. Generative AI: Innovative AI tools and technologies that assist in content creation, design, and automation.
   - Service offerings: Generative design, content generation, automation workflows.

5. Graphic Design: Creative and unique graphic designs for branding, marketing materials, and digital assets.
   - Service offerings: Logo design, brochures, social media visuals, digital marketing campaigns.

6. Marketing Services: Full-stack digital marketing strategies to help you reach and engage your target audience effectively.
   - Service offerings: SEO, content marketing, social media strategy, email marketing.

7. Shopify Development: Expert Shopify store setup, customization, and optimization for better eCommerce success.
   - Service offerings: Custom Shopify themes, Shopify SEO, Shopify integrations.

Industries We Serve:
- eCommerce
- Healthcare
- Finance
- Education
- Retail
- Real Estate
- Hospitality

Why Choose Us:
- Experience: With years of experience, we bring expert knowledge to every project.
- Customer-Centric: We work closely with you to understand your needs and deliver the best possible solutions.
- Cutting-Edge Technology: We use the latest technologies and tools to keep your business ahead of the competition.
- Global Reach: We serve businesses around the world, delivering results that make an impact.

To schedule the meeting or book slots contact us via our email or website.
Contact Information:
- Email: contact@lionprodev.com
- Website: https://lionprodev.com/
"""

@app.route('/api/prompt', methods=['POST'])
def handle_prompt():
    data = request.get_json()
    prompt = data.get("prompt", "").strip()

    if not prompt:
        return jsonify({"error": "Prompt is required."}), 400

    try:
        # The model will respond in English
        chat_completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a helpful assistant specializing in " + LION_PRO_DEV_INFO
                },
                {"role": "user", "content": prompt}
            ],
            stream=True
        )

        def stream_response():
            for chunk in chat_completion:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    time.sleep(0.01)  # optional to slow down the stream

        return Response(stream_response(), content_type="text/plain")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3050, debug=True)
