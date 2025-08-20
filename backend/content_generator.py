# This module is responsible for generating the tweet content.
import random

CATEGORIES = [
    "my_journey",
    "apps_built",
    "tech_tips",
    "tech_news",
    "tech_stories",
    "ethical_hacking",
    "cracked_apps",
    "general_tech",
]

CONTENT = {
    "my_journey": [
        "Spent the morning learning about {topic}. My brain is full, but it's so rewarding! #webdev #100DaysOfCode",
        "Just pushed a new feature to my side project. It's a small one, but it feels great to make progress. #buildinpublic",
        "Reflecting on how far I've come as a developer. It's a marathon, not a sprint. #codingjourney",
        "The best part of being a developer is the constant learning. The worst part is the constant learning. 😉 #developerlife"
    ],
    "apps_built": [
        "Check out this little app I built to {purpose}. It's amazing what you can do with a few lines of {language}! #PortfolioProject #{language}",
        "Thinking about my next side project. Maybe something with {tech_stack}? Any ideas? #webdeveloper #sideproject",
        "One of my favorite projects I've built is a {app_description}. It taught me so much about {learning}. #coding #appdev"
    ],
    "tech_tips": [
        "CSS Tip: Use `clamp()` for fluid typography that respects a min and max size. `font-size: clamp(1rem, 2.5vw, 1.5rem);` #css #webdesign",
        "JavaScript Tip: Destructuring can make your code so much cleaner. `const {{ user, token }} = response.data;` #javascript #es6",
        "React Tip: Use `React.memo` to prevent re-renders of functional components that receive the same props. #reactjs #performance",
        "Git Tip: `git stash` is your best friend when you need to quickly switch contexts without committing your current work. #git #developer"
    ],
    "tech_news": [
        # This will be replaced with an API call later
        "Tech news placeholder: A new JS framework was released today. #technews"
    ],
    "tech_stories": [
        "Remember the 'I LOVE YOU' virus from 2000? It spread via email and caused billions in damages. A wild time for the internet. #techhistory #security",
        "The story of the first computer bug is fascinating. A moth was literally found trapped in a relay of the Harvard Mark II computer. #computinghistory",
        "Ever heard of the PayPal Mafia? A group of former PayPal employees who went on to found companies like Tesla, LinkedIn, and YouTube. #techstories #entrepreneurship"
    ],
    "ethical_hacking": [
        "Ethical Hacking Explained: It's the practice of testing a system's security for vulnerabilities that a malicious hacker could exploit. It's all about defense! #cybersecurity #ethicalhacking",
        "A common tool for ethical hackers is Nmap, used for network discovery and security auditing. It's powerful stuff. #infosec",
        "Phishing is still one of the most common attack vectors. Always double-check the sender's email and links before clicking! #securityawareness"
    ],
    "cracked_apps": [
        "Cracked Apps Explained: They are modified versions of paid software that bypass license verification. But they often come with a hidden cost: malware. #malware #softwaresafety",
        "The risk of using cracked software is huge. You're essentially giving a stranger permission to run any code they want on your machine. Not worth it! #cybersecurity"
    ],
    "general_tech": [
        "What's a piece of tech you're most excited about right now? For me, it's {exciting_tech}. #technology #innovation",
        "The rise of AI is going to change everything. What are your predictions for the next 5 years? #AI #futureoftech",
        "Quantum computing is still in its early days, but the potential is mind-boggling. #quantumcomputing #tech"
    ]
}

def _fill_placeholders(text):
    """
    Fills in placeholders in a given string with random values.
    """
    placeholders = {
        "{topic}": ["React Hooks", "CSS Grid", "Python's asyncio", "WebSockets"],
        "{purpose}": ["track my reading list", "organize my notes", "generate color palettes"],
        "{language}": ["Python", "JavaScript", "Go", "Rust"],
        "{tech_stack}": ["the T3 stack", "a serverless setup", "something with WebAssembly"],
        "{app_description}": ["a simple pomodoro timer", "a markdown note-taking app", "a weather dashboard"],
        "{learning}": ["state management", "API integration", "user authentication"],
        "{exciting_tech}": ["WebAssembly", "edge computing", "generative AI"],
    }
    for key, values in placeholders.items():
        if key in text:
            text = text.replace(key, random.choice(values))
    return text

def generate_content(category):
    """
    Generates content for a given category by picking from a predefined list.
    """
    if category not in CONTENT or not CONTENT[category]:
        # Fallback for empty or non-existent categories
        return "This is a placeholder tweet. #tech"

    content_template = random.choice(CONTENT[category])
    return _fill_placeholders(content_template)

def get_random_category():
    """
    Returns a random category from the list.
    """
    return random.choice(CATEGORIES)
