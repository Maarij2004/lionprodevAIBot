from flask import Flask, request, jsonify, Response, send_from_directory
from flask_cors import CORS
import time
import openai
import os

app = Flask(__name__)
CORS(app)

client = openai.OpenAI(
    api_key="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",
    base_url="https://api.groq.com/openai/v1"
)

LION_PRO_DEV_INFO = """
EST in 2012, Lion Pro Dev is the brainchild of Lion MGT LLC, established with the vision of transforming the digital experience for businesses. From our humble beginnings, we set out on a journey to redefine standards. Located at 5195 Hampsted VCW #232, New Albany, OH 43054, not just a company, it's a partner invested in seeing your brand not only survive but thrive in the digital wilderness.

From the onset, Lion Pro Dev aimed not just to provide services but to become strategic partners in the success stories of our clients. It operates as a Doing Business As (DBA) entity under Lion MGT LLC. This structure ensures a solid foundation, financial stability, and a commitment to upholding the highest standards of business practices.
Lion Pro Dev is a leading software development company specializing in:
1. Custom Software Development
2. Web Design & Development
3. Mobile Application Development
4. Cloud Solutions
5. Digital Marketing

We provide high-quality, tailor-made solutions to help businesses grow, utilizing cutting-edge technologies.
Contact us at:
- Email: office@lionprodev.com

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

5. Graphic Design & UI/UX: Creative and unique graphic designs for branding, marketing materials, and digital assets.
   - Service offerings: Logo design, brochures, social media visuals, digital marketing campaigns.

6. Marketing Services: Full-stack digital marketing strategies to help you reach and engage your target audience effectively.
   - Service offerings: SEO, content marketing, social media strategy, email marketing.

7. Shopify Development: Expert Shopify store setup, customization, and optimization for better eCommerce success.
   - Service offerings: Custom Shopify themes, Shopify SEO, Shopify integrations.

8. UI/UX Design: Crafting seamless, user-centered designs that ensure delightful experiences for web and mobile apps.
   - Service offerings: User Interface (UI) design, User Experience (UX) design, wireframing, prototyping, and user testing.

Industries We Serve:
- eCommerce
- Healthcare
- Finance
- Education
- Retail
- Real Estate
- Hospitality and much more

Why Choose Us:
- Experience: With years of experience, we bring expert knowledge to every project.
- Customer-Centric: We work closely with you to understand your needs and deliver the best possible solutions.
- Cutting-Edge Technology: We use the latest technologies and tools to keep your business ahead of the competition.
- Global Reach: We serve businesses around the world, delivering results that make an impact.

To schedule the meeting or book slots contact us via our email or website.
Contact Information:

- Email: office@lionprodev.com
- Website: https://lionprodev.com/



Philip Cutting, a passionate Web, Mobile Apps Developer, AI Engineer, and the visionary (CTO & Co-founder) of Lion Pro Dev, has been steering the New Albany, Ohio-based software company towards innovation and excellence since 2012. Specializing in developing web and mobile applications, his career is dedicated to transforming visionary ideas into tangible, digital solutions that drive success.

With a comprehensive suite of services, the focus is on crafting bespoke solutions that not only meet but exceed clients' digital aspirations. The approach is always tailored and results-driven, aiming to craft engaging mobile apps and effective web solutions that enhance conversion and engagement.
"""

@app.route('/api/prompt', methods=['POST'])
def handle_prompt():
    data = request.get_json()
    prompt = data.get("prompt", "").strip()

    if not prompt:
        return jsonify({"error": "Prompt is required."}), 400

    try:
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
                    time.sleep(0.01) 

        return Response(stream_response(), content_type="text/plain")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def serve_react():
    try:
        return send_from_directory('../frontend/build', 'index.html')
    except:
        return jsonify({"message": "Lion Pro Dev API is running!", "status": "success"})

@app.route('/<path:path>')
def serve_static_files(path):
    try:
        return send_from_directory('../frontend/build', path)
    except:
        return send_from_directory('../frontend/build', 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3050))
    app.run(host='0.0.0.0', port=port, debug=False)