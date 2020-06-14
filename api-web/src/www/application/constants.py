BOARD_STATUS = (
    ('open',            'Open'),
    ('in_progress',     'In progress'),
    ('completed',       'Completed'),
    ('closed',          'Closed')
)

BOARD_STATUS_DATA = {
    'open': {
        'name': 'open',
        'bg_color': '#FFFFFF',
        'text_color': '#000000'
    },
    'in_progress': {
        'name': 'in progress',
        'bg_color': '#EBF2F9',
        'text_color': '#3B73BC'
    },
    'completed': {
        'name': 'completed',
        'bg_color': '#009900',
        'text_color': '#FFFFFF'
    },
    'closed': {
        'name': 'closed',
        'bg_color': '#999999',
        'text_color': '#FFFFFF'
    },
}

BOARD_ACTIVE_STATUS_LIST = ['open', 'in_progress', 'completed']

BOARD_GOAL_STATUS = (
    ('active',          'Active'),
    ('success',         'Success'),
    ('failed',          'Failed'),
    ('rejected',        'Rejected'),
)

BOARD_STORY_RATING = {
    1: {'id': 'rating-up', 'label': 'Thumb up'},
    2: {'id': 'rating-down', 'label': 'Thumb down'},
    3: {'id': 'rating-none', 'label': 'Thumb none'},
}
BOARD_GOAL_STATUS_DATA = {
    'active': {
        'name':         'Active',
        'bg_color':     '#EBF2F9',
        'text_color':   '#3B73BC',
    },
    'success': {
        'name':         'Success',
        'bg_color':     '#009900',
        'text_color':   '#FFFFFF',
    },
    'failed': {
        'name':         'Failed',
        'bg_color':     '#cc0000',
        'text_color':   '#FFFFFF',
    },
    'rejected': {
        'name':         'Rejected',
        'bg_color':     '#999999',
        'text_color':   '#FFFFFF',
    },
}

OBJECTIVE_RESULTS = (
    ('pending',         'Pending'),
    ('pass',            'Pass'),
    ('failed',          'Failed'),
)

OBJECTIVE_RESULTS_DATA = {
    'pending': {
        'name':         'Pending',
        'bg_color':     '#EBF2F9',
        'text_color':   '#3B73BC',
    },
    'pass': {
        'name':         'Pass',
        'bg_color':     '#009900',
        'text_color':   '#FFFFFF',
    },
    'failed': {
        'name':         'Failed',
        'bg_color':     '#cc0000',
        'text_color':   '#FFFFFF',
    },
}

REQUEST_PRIORITY = (
    (0,        'Low'),
    (10,       'Normal'),
    (20,       'High'),
    (30,       'Ultra High')
)

REQUEST_STATUS = (
    ('pending',       'Pending'),
    ('planned',       'Planned'),
    ('processing',    'Processing'),
    ('completed',     'Completed'),
    ('rejected',      'Rejected'),
)

REQUEST_STATUS_DATA = {
    'pending': {
        'name':         'Pending',
        'bg_color':     '#EBF2F9',
        'text_color':   '#3B73BC',
    },
    'planned': {
        'name':         'Planned',
        'bg_color':     '#EBF2F9',
        'text_color':   '#FF0000',
    },
    'processing': {
        'name':         'Processing',
        'bg_color':     '#fff5ee',
        'text_color':   '#b8860b',
    },
    'completed': {
        'name':         'Completed',
        'bg_color':     '#009900',
        'text_color':   '#FFFFFF',
    },
    'rejected': {
        'name':         'Rejected',
        'bg_color':     '#cc0000',
        'text_color':   '#FFFFFF',
    },
}


SCORING_SCHEMA = [
    {'L': 'H', 'B': '+', 'R': '+', 'S': 'A'},
    {'L': 'H', 'B': '+', 'R': '.', 'S': '+'},
    {'L': 'H', 'B': '+', 'R': '-', 'S': '+'},
    {'L': 'H', 'B': '.', 'R': '+', 'S': '+'},
    {'L': 'H', 'B': '.', 'R': '.', 'S': '.'},
    {'L': 'H', 'B': '.', 'R': '-', 'S': '.'},
    {'L': 'H', 'B': '-', 'R': '+', 'S': '+'},
    {'L': 'H', 'B': '-', 'R': '.', 'S': '.'},
    {'L': 'H', 'B': '-', 'R': '-', 'S': '-'},
    {'L': 'M', 'B': '+', 'R': '+', 'S': '+'},
    {'L': 'M', 'B': '+', 'R': '.', 'S': '+'},
    {'L': 'M', 'B': '+', 'R': '-', 'S': '.'},
    {'L': 'M', 'B': '.', 'R': '+', 'S': '+'},
    {'L': 'M', 'B': '.', 'R': '.', 'S': '.'},
    {'L': 'M', 'B': '.', 'R': '-', 'S': '.'},
    {'L': 'M', 'B': '-', 'R': '+', 'S': '.'},
    {'L': 'M', 'B': '-', 'R': '.', 'S': '-'},
    {'L': 'M', 'B': '-', 'R': '-', 'S': '-'},
    {'L': 'L', 'B': '+', 'R': '+', 'S': '+'},
    {'L': 'L', 'B': '+', 'R': '.', 'S': '.'},
    {'L': 'L', 'B': '+', 'R': '-', 'S': '.'},
    {'L': 'L', 'B': '.', 'R': '+', 'S': '.'},
    {'L': 'L', 'B': '.', 'R': '.', 'S': '.'},
    {'L': 'L', 'B': '.', 'R': '-', 'S': '-'},
    {'L': 'L', 'B': '-', 'R': '+', 'S': '-'},
    {'L': 'L', 'B': '-', 'R': '.', 'S': '-'},
    {'L': 'L', 'B': '-', 'R': '-', 'S': 'F'},
]

STORY_STATUS = {
    'Backlog':{
        'name': 'backlog',
        'bg_color': '#FFFFFF',
        'text_color': '#black',
    },

    'Pending':{
        'name': 'pending',
        'bg_color': '#ebf2f9',
        'text_color': '3b73bc', 
    },

    'In progress': {
        'name': 'in progress',
        'bg_color': '#fff5ee',
        'text_color': '#b8860b',
    },

    'Acceptance':{
        'name': 'acceptance',
        'bg_color': '#d8bfd8',
        'text_color': '#8b008b',
    },
    
    'Accepted':{
        'name': 'accepted',
        'bg_color': '#98fb98',
        'text_color': '#006400',
    },
    
    'Testing':{
        'name': 'testing',
        'bg_color': '#fff5ee',
        'text_color': '#cc2900',
    },
    
    'Failed':{
        'name': 'failed',
        'bg_color': '#ffcccc',
        'text_color': '#ff0000',
    },
    
    'Icebox':{
        'name': 'icebox',
        'bg_color': '#CCCCCC',
        'text_color': '#ffffff',
    },
}