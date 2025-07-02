import os
from google.colab import userdata
#  ************************************************************
# I'm doing this in google colab and keeping API keys as secrets.
# You might want to modify this bit
#  ************************************************************

openai_api_key = userdata.get('openai_api_key')
os.environ['OPENAI_API_KEY'] = openai_api_key

deepseek_api_key = userdata.get('deepseek_api_key')
os.environ['DEEPSEEK_API_KEY'] = deepseek_api_key

anthropic_api_key = userdata.get('anthropic_api_key')
os.environ['ANTHROPIC_API_KEY'] = anthropic_api_key



import os
import json
import numpy as np
from anthropic import Anthropic
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
from IPython.display import HTML, display, clear_output
import ipywidgets as widgets
from pathlib import Path

# Initialize clients
# Option 1: Use environment variables (recommended)
anthropic_client = Anthropic()  # defaults to os.environ.get("ANTHROPIC_API_KEY")
openai_client = OpenAI()  # defaults to os.environ.get("OPENAI_API_KEY")

# Option 2: Hardcode (less secure)
# anthropic_client = Anthropic(api_key="your-anthropic-api-key-here")
# openai_client = OpenAI(api_key="your-openai-api-key-here")

# Global variables for the chat
conversation_history = []
embeddings_data = []

# Load knowledge base
def load_knowledge_base(folder_path="knowledge_base"):
    """Load all text files from the knowledge base folder"""
    knowledge_docs = []
    folder = Path(folder_path)
    
    if not folder.exists():
        print(f"Creating {folder_path} directory...")
        folder.mkdir()
        print(f"Please add your text files to the {folder_path} directory and run this cell again.")
        return []
    
    for file_path in folder.glob("*.txt"):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            knowledge_docs.append({
                'filename': file_path.name,
                'content': content,
                'chunks': chunk_text(content)
            })
    
    print(f"Loaded {len(knowledge_docs)} documents")
    return knowledge_docs

def chunk_text(text, chunk_size=500, overlap=100):
    """Split text into overlapping chunks"""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks

def get_embedding(text):
    """Get embedding using OpenAI's embeddings API"""
    try:
        # Create embedding using OpenAI's API
        response = openai_client.embeddings.create(
            model="text-embedding-3-small",  # You can also use "text-embedding-3-large" for better quality
            input=text[:8000]  # Limit text length for efficiency
        )
        return np.array(response.data[0].embedding)
    except Exception as e:
        print(f"Error getting embedding: {e}")
        # Fallback to random vector if API fails
        return np.random.rand(1536)  # text-embedding-3-small has 1536 dimensions

def create_embeddings(knowledge_docs):
    """Create embeddings for all document chunks"""
    print("Creating embeddings... This may take a moment.")
    embeddings_data = []
    
    total_chunks = sum(len(doc['chunks']) for doc in knowledge_docs)
    processed = 0
    
    for doc in knowledge_docs:
        for chunk in doc['chunks']:
            processed += 1
            print(f"Processing chunk {processed}/{total_chunks} from {doc['filename']}", end='\r')
            embedding = get_embedding(chunk)
            embeddings_data.append({
                'filename': doc['filename'],
                'chunk': chunk,
                'embedding': embedding
            })
    
    print(f"\nCreated {len(embeddings_data)} chunk embeddings")
    return embeddings_data

def find_relevant_chunks(query, embeddings_data, top_k=3):
    """Find most relevant chunks for a query"""
    if not embeddings_data:
        return []
        
    query_embedding = get_embedding(query)
    
    similarities = []
    for item in embeddings_data:
        sim = cosine_similarity([query_embedding], [item['embedding']])[0][0]
        similarities.append((sim, item))
    
    # Sort by similarity and get top k
    similarities.sort(key=lambda x: x[0], reverse=True)
    
    # Only return chunks with similarity above threshold
    threshold = 0.3  # Adjust this to control relevance
    relevant = [item[1] for item in similarities[:top_k] if item[0] > threshold]
    
    return relevant

def generate_assistant_response(conversation_history, relevant_chunks):
    """Generate AI assistant response based on conversation and relevant knowledge"""
    # Format relevant knowledge
    knowledge_context = "\n\n".join([
        f"From {chunk['filename']}:\n{chunk['chunk']}"
        for chunk in relevant_chunks
    ]) if relevant_chunks else "No relevant knowledge base articles found."
    
    # Format conversation history
    conversation_text = "\n".join([
        f"{msg['sender'].capitalize()}: {msg['message']}"
        for msg in conversation_history
    ])
    
    prompt = f"""You are an AI assistant helping a contact center agent. 
Based on the conversation below and the relevant knowledge articles, provide helpful information, 
summaries, and suggestions for the agent.

Relevant Knowledge:
{knowledge_context}

Current Conversation:
{conversation_text}

Provide a concise, helpful response with:
1. Key relevant information from the knowledge base
2. Suggested responses or actions for the agent
3. Any important procedures or guidelines that apply

Keep your response focused and actionable. Format your response with clear sections using markdown."""
    
    try:
        response = anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",  # Using latest available model
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        return f"Error generating response: {e}"

# Create the UI components
def create_chat_interface():
    """Create the interactive chat interface using ipywidgets"""
    
    # Create the output areas
    chat_output = widgets.Output()
    ai_output = widgets.Output()
    knowledge_output = widgets.Output()
    
    # Create input fields
    customer_input = widgets.Text(
        placeholder='Type customer message and press Enter...',
        description='Customer:',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='100%')
    )
    
    agent_input = widgets.Text(
        placeholder='Type agent message and press Enter...',
        description='Agent:',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='100%')
    )
    
    # Status label
    status_label = widgets.Label(value="Ready! Type in either field and press Enter.")
    
    def update_ai_assistant():
        """Update the AI assistant panel with new response"""
        # Get full conversation text
        conversation_text = "\n".join([
            f"{msg['sender'].capitalize()}: {msg['message']}"
            for msg in conversation_history
        ])
        
        # Find relevant chunks
        relevant_chunks = find_relevant_chunks(conversation_text, embeddings_data)
        
        # Update AI assistant panel (middle)
        with ai_output:
            clear_output(wait=True)
            print("🔄 AI Assistant is analyzing the conversation...")
            
            # Generate response
            ai_response = generate_assistant_response(conversation_history, relevant_chunks)
            
            # Display the response
            clear_output(wait=True)
            display(HTML(f"""
                <div style="font-family: sans-serif; line-height: 1.6;">
                    <div style="white-space: pre-wrap;">{ai_response}</div>
                </div>
            """))
        
        # Update knowledge base panel (right)
        with knowledge_output:
            clear_output(wait=True)
            if relevant_chunks:
                display(HTML("<h4 style='margin-top: 0; color: #1976D2;'>📄 Retrieved Knowledge Base Snippets:</h4>"))
                for i, chunk in enumerate(relevant_chunks, 1):
                    display(HTML(f"""
                        <div style="margin-bottom: 15px; padding: 12px; background-color: #f0f4f8; 
                                    border-left: 4px solid #1976D2; border-radius: 4px;">
                            <div style="font-weight: bold; color: #1976D2; margin-bottom: 8px;">
                                Source: {chunk['filename']} (Snippet {i})
                            </div>
                            <div style="font-family: monospace; font-size: 13px; white-space: pre-wrap; 
                                        color: #333; background-color: white; padding: 10px; 
                                        border-radius: 4px; border: 1px solid #ddd;">
{chunk['chunk']}
                            </div>
                        </div>
                    """))
            else:
                display(HTML("""
                    <div style="text-align: center; color: #666; padding: 20px;">
                        <p>No relevant knowledge base snippets found for this conversation.</p>
                    </div>
                """))
    
    def add_message(sender, message):
        """Add a message to the conversation"""
        if message.strip():
            # Add to history
            conversation_history.append({
                'sender': sender,
                'message': message.strip()
            })
            
            # Display in chat
            with chat_output:
                display(HTML(f"""
                    <div style="margin: 8px 0; padding: 10px 14px; border-radius: 12px; 
                         background-color: {'#e3f2fd' if sender == 'customer' else '#e8f5e9'};">
                        <strong>{sender.upper()}:</strong> {message}
                    </div>
                """))
            
            # Update AI assistant
            update_ai_assistant()
    
    def on_customer_submit(change):
        """Handle customer input submission"""
        if change['new'] and customer_input.value.strip():
            add_message('customer', customer_input.value)
            customer_input.value = ''
    
    def on_agent_submit(change):
        """Handle agent input submission"""
        if change['new'] and agent_input.value.strip():
            add_message('agent', agent_input.value)
            agent_input.value = ''
    
    # Connect event handlers
    customer_input.on_submit(lambda x: on_customer_submit({'new': True}))
    agent_input.on_submit(lambda x: on_agent_submit({'new': True}))
    
    # Create the layout with three panels
    left_panel = widgets.VBox([
        widgets.HTML("<h3>💬 Customer Service Chat</h3>"),
        widgets.Box([chat_output], layout=widgets.Layout(
            height='400px', 
            overflow_y='auto',
            border='1px solid #ddd',
            padding='10px',
            border_radius='8px'
        )),
        customer_input,
        agent_input,
        status_label
    ], layout=widgets.Layout(width='30%', padding='10px'))
    
    middle_panel = widgets.VBox([
        widgets.HTML("<h3>🤖 AI Assistant Response</h3>"),
        widgets.Box([ai_output], layout=widgets.Layout(
            height='500px',
            overflow_y='auto',
            border='1px solid #ddd',
            padding='15px',
            border_radius='8px',
            background_color='#f8f9fa'
        ))
    ], layout=widgets.Layout(width='35%', padding='10px'))
    
    right_panel = widgets.VBox([
        widgets.HTML("<h3>📚 Knowledge Base Sources</h3>"),
        widgets.Box([knowledge_output], layout=widgets.Layout(
            height='500px',
            overflow_y='auto',
            border='1px solid #ddd',
            padding='15px',
            border_radius='8px',
            background_color='#f5f7fa'
        ))
    ], layout=widgets.Layout(width='35%', padding='10px'))
    
    # Initial messages
    with ai_output:
        display(HTML("""
            <div style="text-align: center; color: #666; padding: 20px;">
                <p>AI-generated assistance will appear here...</p>
            </div>
        """))
    
    with knowledge_output:
        display(HTML("""
            <div style="text-align: center; color: #666; padding: 20px;">
                <p>Knowledge base snippets will appear here when found...</p>
            </div>
        """))
    
    # Create main container with three panels
    main_container = widgets.HBox([left_panel, middle_panel, right_panel], 
                                  layout=widgets.Layout(width='100%'))
    
    return main_container

# Load and process knowledge base
print("Loading knowledge base...")
knowledge_docs = load_knowledge_base()
embeddings_data = create_embeddings(knowledge_docs) if knowledge_docs else []

# Create and display the interface
print("\n" + "="*60)
if not knowledge_docs:
    print("⚠️  WARNING: No documents found in knowledge_base folder!")
    print("\nTo use this system:")
    print("1. Create a 'knowledge_base' folder in the same directory as this notebook")
    print("2. Add your .txt files with SOPs/procedures to that folder")
    print("3. Re-run this cell to load the documents")
else:
    print(f"✅ System ready! ")
    print(f"📚 Loaded {len(knowledge_docs)} documents")
    print(f"🔍 Created {len(embeddings_data)} searchable chunks")
    print(f"\n💡 Using:")
    print(f"   - OpenAI embeddings (text-embedding-3-small)")
    print(f"   - Claude for response generation")
    print(f"\n📋 Three-panel layout:")
    print(f"   - Left: Customer service chat")
    print(f"   - Middle: AI-generated assistance")
    print(f"   - Right: Retrieved knowledge base snippets")
    print(f"\n🚀 Start typing in the Customer or Agent input boxes to begin!")
print("="*60)
print("\n")

# Display the interface
interface = create_chat_interface()
display(interface)

# Add a note about adjusting the similarity threshold
print("\n💡 Tip: The system shows the top 3 most relevant knowledge base snippets with similarity > 0.3")
print("   You can adjust the 'top_k' parameter in find_relevant_chunks() to show more/fewer snippets")
print("   You can adjust the 'threshold' parameter to control relevance filtering")