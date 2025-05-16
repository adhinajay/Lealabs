import autogen

# LLM configuration for Gemini Flash
config_list = [
    {
        'model': 'gemini-2.0-flash',
        'api_key': '#######',
        'api_type': 'google',
    }
]

llm_config = {
    'seed': 42,
    'config_list': config_list,
    'temperature': 0
}

# Initialize assistant agent
assistant = autogen.AssistantAgent(
    name='assistant',
    llm_config=llm_config
)

# Initialize user proxy agent
user_proxy = autogen.UserProxyAgent(
    name='user_proxy',
    human_input_mode='NEVER',
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get('content', '').rstrip().endswith('TERMINATE'),
    code_execution_config={
        'work_dir': 'web',
        'use_docker': False
    },
    llm_config=llm_config,
    system_message="""
    Reply TERMINATE if the task has been resolved at full satisfaction. 
    Otherwise, reply CONTINUE, or the reason why task is not solved yet.
    """
)

# First task: Write code to print numbers 1 to 100
user_proxy.initiate_chat(
    assistant,
    message="""
    Write a python code to output numbers 1 to 100, and then store the code in a file.
    """
)

# Second task: Modify the existing code to print 1 to 200
user_proxy.initiate_chat(
    assistant,
    message="""
    Change the code in the file you just created to instead output numbers 1 to 200.
    """
)
