"""
Demo data for offline/demo mode
Provides sample search results without making real API calls
"""

DEMO_SEARCH_RESULTS = {
    "artificial intelligence in healthcare": [
        {
            'title': 'AI in Healthcare: Transforming Patient Care',
            'url': 'https://example.com/ai-healthcare-1',
            'snippet': 'Artificial intelligence is revolutionizing healthcare through improved diagnostics, personalized treatment plans, and predictive analytics. AI algorithms can analyze medical images with accuracy comparable to human radiologists, helping detect diseases like cancer at earlier stages.'
        },
        {
            'title': 'Machine Learning Applications in Medicine',
            'url': 'https://example.com/ai-healthcare-2',
            'snippet': 'Machine learning models are being used to predict patient outcomes, optimize hospital operations, and assist in drug discovery. These technologies are helping healthcare providers make more informed decisions and improve patient care quality.'
        },
        {
            'title': 'The Future of AI-Powered Healthcare',
            'url': 'https://example.com/ai-healthcare-3',
            'snippet': 'From virtual health assistants to robotic surgery, AI is expanding the possibilities in healthcare. Recent developments include AI systems that can detect diseases earlier and more accurately than traditional methods, leading to better patient outcomes.'
        },
        {
            'title': 'AI Ethics in Medical Practice',
            'url': 'https://example.com/ai-healthcare-4',
            'snippet': 'As AI becomes more prevalent in healthcare, ethical considerations around patient privacy, algorithmic bias, and accountability are crucial. Medical professionals and policymakers are working to establish guidelines for responsible AI use.'
        },
        {
            'title': 'Real-World AI Healthcare Success Stories',
            'url': 'https://example.com/ai-healthcare-5',
            'snippet': 'Healthcare institutions worldwide are reporting significant improvements in patient outcomes using AI. Case studies show reduced diagnosis times, improved treatment accuracy, and better resource allocation in hospitals.'
        }
    ],
    
    "artificial intelligence": [
        {
            'title': 'Understanding Artificial Intelligence',
            'url': 'https://example.com/ai-overview',
            'snippet': 'Artificial Intelligence (AI) refers to computer systems that can perform tasks typically requiring human intelligence. This includes learning, reasoning, problem-solving, and understanding language.'
        },
        {
            'title': 'AI Technology Trends 2024',
            'url': 'https://example.com/ai-trends',
            'snippet': 'The AI landscape is rapidly evolving with breakthroughs in large language models, computer vision, and autonomous systems. Companies are investing billions in AI research and development.'
        },
        {
            'title': 'Applications of AI Across Industries',
            'url': 'https://example.com/ai-applications',
            'snippet': 'AI is being applied across healthcare, finance, transportation, education, and entertainment. From chatbots to self-driving cars, AI technologies are transforming how we live and work.'
        }
    ],
    
    "machine learning": [
        {
            'title': 'Machine Learning Fundamentals',
            'url': 'https://example.com/ml-basics',
            'snippet': 'Machine learning is a subset of AI that enables systems to learn and improve from experience without explicit programming. It uses algorithms to identify patterns in data.'
        },
        {
            'title': 'Types of Machine Learning',
            'url': 'https://example.com/ml-types',
            'snippet': 'The three main types of machine learning are supervised learning, unsupervised learning, and reinforcement learning. Each has different applications and use cases.'
        },
        {
            'title': 'Real-World ML Applications',
            'url': 'https://example.com/ml-applications',
            'snippet': 'Machine learning powers recommendation systems, fraud detection, image recognition, and natural language processing. Companies use ML to gain insights from large datasets.'
        }
    ],
    
    "climate change": [
        {
            'title': 'Climate Change: Current State',
            'url': 'https://example.com/climate-overview',
            'snippet': 'Global temperatures continue to rise, with 2024 on track to be one of the warmest years on record. Scientists warn of increasing extreme weather events and sea level rise.'
        },
        {
            'title': 'Climate Solutions and Mitigation',
            'url': 'https://example.com/climate-solutions',
            'snippet': 'Renewable energy, carbon capture, and sustainable practices offer pathways to reduce emissions. Countries are implementing policies to achieve net-zero targets.'
        },
        {
            'title': 'Impact on Global Ecosystems',
            'url': 'https://example.com/climate-impact',
            'snippet': 'Climate change affects biodiversity, agriculture, and human health. Ecosystems are struggling to adapt to rapid environmental changes.'
        }
    ],
    
    "quantum computing": [
        {
            'title': 'Introduction to Quantum Computing',
            'url': 'https://example.com/quantum-intro',
            'snippet': 'Quantum computers use quantum mechanical phenomena to solve complex problems faster than classical computers. They leverage qubits instead of traditional bits.'
        },
        {
            'title': 'Quantum Computing Applications',
            'url': 'https://example.com/quantum-apps',
            'snippet': 'Potential applications include cryptography, drug discovery, optimization problems, and materials science. Major tech companies are racing to build practical quantum computers.'
        },
        {
            'title': 'Challenges in Quantum Computing',
            'url': 'https://example.com/quantum-challenges',
            'snippet': 'Quantum systems are fragile and require extremely low temperatures. Error correction and scaling remain significant technical hurdles.'
        }
    ],
    
    "default": [
        {
            'title': 'Research Topic Overview',
            'url': 'https://example.com/overview',
            'snippet': 'This topic encompasses various aspects including recent developments, practical applications, and future implications. Research shows significant interest and ongoing innovation in this field.'
        },
        {
            'title': 'Latest Developments and Trends',
            'url': 'https://example.com/trends',
            'snippet': 'Current trends indicate growing adoption and increasing investment. Experts predict continued growth and evolution in the coming years with new applications emerging regularly.'
        },
        {
            'title': 'Practical Applications',
            'url': 'https://example.com/applications',
            'snippet': 'Real-world implementations demonstrate the value and potential of this technology. Organizations across industries are finding innovative ways to leverage these capabilities for competitive advantage.'
        },
        {
            'title': 'Challenges and Considerations',
            'url': 'https://example.com/challenges',
            'snippet': 'While promising, this field faces several challenges including technical limitations, ethical concerns, and regulatory questions that need to be addressed.'
        },
        {
            'title': 'Future Outlook',
            'url': 'https://example.com/future',
            'snippet': 'The future looks bright with continued innovation expected. Researchers and practitioners are optimistic about upcoming breakthroughs and wider adoption.'
        }
    ]
}

def get_demo_results(query: str, max_results: int = 5) -> list:
    """
    Get demo search results for a query
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return
        
    Returns:
        List of demo search results
    """
    # Normalize query
    query_lower = query.lower()
    
    # Check for exact or partial matches
    for key in DEMO_SEARCH_RESULTS:
        if key == "default":
            continue
        
        # Check if query contains the key or vice versa
        if key in query_lower or any(word in query_lower for word in key.split()):
            return DEMO_SEARCH_RESULTS[key][:max_results]
    
    # Return default results if no match found
    return DEMO_SEARCH_RESULTS["default"][:max_results]


# Add more topics easily
def add_demo_topic(topic: str, results: list):
    """
    Add a new demo topic
    
    Args:
        topic: Topic name
        results: List of result dictionaries
    """
    DEMO_SEARCH_RESULTS[topic.lower()] = results