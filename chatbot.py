import yaml
from IPython.display import display, clear_output
import ipywidgets as widgets
from ipywidgets import VBox, HBox, Button, HTML, Layout

class DecisionTreeChatbot:
    def __init__(self):
        self.decision_tree = None
        self.current_node = None
        self.history = []
        self.start_node = 'node1'
        
        # Create widgets
        self.output = widgets.Output()
        self.create_widgets()
        
        # Load sample data by default
        self.load_sample_data()
        
    def create_widgets(self):
        """Create the UI widgets"""
        # Control buttons
        self.back_button = Button(
            description="← Back",
            disabled=True,
            button_style='',
            layout=Layout(width='100px')
        )
        self.back_button.on_click(self.go_back)
        
        self.restart_button = Button(
            description="🔄 Restart",
            button_style='info',
            layout=Layout(width='100px')
        )
        self.restart_button.on_click(self.restart)
        
        # File upload
        self.upload_button = widgets.FileUpload(
            accept='.yaml,.yml,.txt',
            multiple=False,
            description="Upload YAML",
            button_style='success'
        )
        self.upload_button.observe(self.handle_upload, names='value')
        
        # Load sample button
        self.sample_button = Button(
            description="Load Sample",
            button_style='warning',
            layout=Layout(width='120px')
        )
        self.sample_button.on_click(lambda x: self.load_sample_data())
        
        # Control panel
        self.controls = HBox([
            self.back_button, 
            self.restart_button, 
            self.upload_button,
            self.sample_button
        ])
        
        # Main container
        self.container = VBox([
            HTML("<h2>Decision Tree Chatbot</h2>"),
            self.controls,
            self.output
        ])
    
    def parse_yaml_simple(self, yaml_text):
        """Simple YAML parser for the specific format"""
        lines = yaml_text.strip().split('\n')
        result = {}
        current_key = None
        current_obj = None
        in_options = False
        
        for line in lines:
            original_line = line
            line = line.strip()
            if not line:
                continue
                
            # Check if this is a new node (no indentation)
            if line.endswith(':') and not original_line.startswith(' '):
                current_key = line[:-1]
                current_obj = {}
                result[current_key] = current_obj
                in_options = False
            elif line.startswith('question:'):
                current_obj['question'] = line[9:].strip().strip('\'"')
                in_options = False
            elif line.startswith('verdict:'):
                current_obj['verdict'] = line[8:].strip().strip('\'"')
                in_options = False
            elif line == 'options:':
                current_obj['options'] = {}
                in_options = True
            elif in_options and ':' in line and original_line.startswith(' '):
                key, value = line.split(':', 1)
                current_obj['options'][key.strip()] = value.strip()
        
        return result
    
    def load_sample_data(self):
        """Load sample decision tree data"""
        sample_yaml = """node1:
    question: "Is this request for new software?"
    options:
        yes: node2
        no: node3

node2:
    question: "Is the software cost over $1000?"
    options:
        yes: node4
        no: node5

node3:
    question: "Is this a hardware request?"
    options:
        yes: node6
        no: node7

node4:
    verdict: "Requires CFO approval and security review"

node5:
    verdict: "Can be approved by IT manager"

node6:
    question: "Is the hardware cost over $500?"
    options:
        yes: node8
        no: node9

node7:
    verdict: "Please clarify the type of request"

node8:
    verdict: "Requires manager approval and procurement review"

node9:
    verdict: "Can be approved by direct supervisor" """
        
        try:
            self.decision_tree = self.parse_yaml_simple(sample_yaml)
            self.current_node = self.start_node
            self.history = []
            self.update_display()
        except Exception as e:
            self.show_error(f"Error loading sample data: {str(e)}")
    
    def handle_upload(self, change):
        """Handle file upload"""
        if change['new']:
            uploaded_file = list(change['new'].values())[0]
            content = uploaded_file['content'].decode('utf-8')
            
            try:
                # Try standard YAML first, then fall back to simple parser
                try:
                    self.decision_tree = yaml.safe_load(content)
                except:
                    self.decision_tree = self.parse_yaml_simple(content)
                
                # Find the starting node
                if self.decision_tree:
                    self.start_node = list(self.decision_tree.keys())[0]
                    self.current_node = self.start_node
                    self.history = []
                    self.update_display()
                else:
                    self.show_error("No valid data found in file")
                    
            except Exception as e:
                self.show_error(f"Error parsing file: {str(e)}")
    
    def show_error(self, message):
        """Display error message"""
        with self.output:
            clear_output(wait=True)
            print(f"❌ {message}")
    
    def update_display(self):
        """Update the main display"""
        if not self.decision_tree or not self.current_node:
            return
            
        node_data = self.decision_tree.get(self.current_node)
        if not node_data:
            self.show_error(f"Node '{self.current_node}' not found")
            return
        
        # Update back button state
        self.back_button.disabled = len(self.history) == 0
        
        with self.output:
            clear_output(wait=True)
            
            if 'question' in node_data:
                # Display question and options
                print(f"❓ {node_data['question']}")
                print()
                
                if 'options' in node_data:
                    option_buttons = []
                    for option, next_node in node_data['options'].items():
                        btn = Button(
                            description=option,
                            layout=Layout(width='200px', margin='5px'),
                            button_style='primary'
                        )
                        btn.next_node = next_node
                        btn.option_text = option
                        btn.on_click(self.handle_option_click)
                        option_buttons.append(btn)
                    
                    # Display buttons in a nice layout
                    if len(option_buttons) <= 3:
                        display(HBox(option_buttons))
                    else:
                        # Split into rows if more than 3 options
                        for i in range(0, len(option_buttons), 3):
                            display(HBox(option_buttons[i:i+3]))
                else:
                    print("No options available")
                    
            elif 'verdict' in node_data:
                # Display final verdict
                print("✅ Decision:")
                print()
                display(HTML(f"""
                <div style="
                    background-color: #d4edda; 
                    border: 1px solid #c3e6cb; 
                    padding: 15px; 
                    border-radius: 5px;
                    color: #155724;
                    font-weight: bold;
                ">
                    {node_data['verdict']}
                </div>
                """))
            else:
                self.show_error("Invalid node data")
            
            # Show decision path if available
            if self.history:
                print("\n" + "="*50)
                print("📍 Decision Path:")
                path = " → ".join([step['choice'] for step in self.history])
                print(f"   {path}")
    
    def handle_option_click(self, button):
        """Handle option button click"""
        # Add to history
        self.history.append({
            'node': self.current_node,
            'choice': button.option_text
        })
        
        # Move to next node
        self.current_node = button.next_node
        self.update_display()
    
    def go_back(self, button):
        """Go back to previous question"""
        if self.history:
            last_step = self.history.pop()
            self.current_node = last_step['node']
            self.update_display()
    
    def restart(self, button):
        """Restart from the beginning"""
        self.current_node = self.start_node
        self.history = []
        self.update_display()
    
    def display(self):
        """Display the chatbot"""
        display(self.container)

# Usage example:
def create_decision_tree_chatbot():
    """Create and display the decision tree chatbot"""
    chatbot = DecisionTreeChatbot()
    chatbot.display()
    return chatbot

# To use in your notebook:
# chatbot = create_decision_tree_chatbot()