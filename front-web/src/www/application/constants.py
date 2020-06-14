BOARD_STATUS = [
    {'id': 'open',             'label': 'Open'},
    {'id': 'in_progress',      'label': 'In progress'},
    {'id': 'completed',        'label': 'Completed'},
    {'id': 'closed',           'label': 'Closed'},
]

BOARD_GOAL_STATUS = [
    {'id': 'active',           'label': 'Active'},
    {'id': 'success',          'label': 'Success'},
    {'id': 'failed',           'label': 'Failed'},
    {'id': 'rejected',         'label': 'Rejected'},
]

OBJECTIVE_RESULTS = [
    {'id': 'pending',           'label': 'Pending'},
    {'id': 'pass',          'label': 'Pass'},
    {'id': 'failed',           'label': 'Failed'},
]

REQUEST_PRIORITY = [
    {'id': 0,                  'label': 'Low'},
    {'id': 10,                 'label': 'Normal'},
    {'id': 20,                 'label': 'High'},
    {'id': 30,                 'label': 'Ultra High'},
]


REQUEST_STATUS = [
    {'id': 'pending',          'label': 'Pending'},
    {'id': 'planned',          'label': 'Planned'},
    {'id': 'processing',       'label': 'Processing'},
    {'id': 'completed',        'label': 'Completed'},
    {'id': 'rejected',         'label': 'Rejected'},
]

SCORING_SCHEMA = [
    [
        {'L': 'H', 'B': '+', 'R': '+', 'S': 'A'},
        {'L': 'H', 'B': '+', 'R': '.', 'S': '+'},
        {'L': 'H', 'B': '+', 'R': '-', 'S': '+'},
        {'L': 'H', 'B': '.', 'R': '+', 'S': '+'},
        {'L': 'H', 'B': '.', 'R': '.', 'S': '.'},
        {'L': 'H', 'B': '.', 'R': '-', 'S': '.'},
        {'L': 'H', 'B': '-', 'R': '+', 'S': '+'},
        {'L': 'H', 'B': '-', 'R': '.', 'S': '.'},
        {'L': 'H', 'B': '-', 'R': '-', 'S': '-'},
    ],
    [
        {'L': 'M', 'B': '+', 'R': '+', 'S': '+'},
        {'L': 'M', 'B': '+', 'R': '.', 'S': '+'},
        {'L': 'M', 'B': '+', 'R': '-', 'S': '.'},
        {'L': 'M', 'B': '.', 'R': '+', 'S': '+'},
        {'L': 'M', 'B': '.', 'R': '.', 'S': '.'},
        {'L': 'M', 'B': '.', 'R': '-', 'S': '.'},
        {'L': 'M', 'B': '-', 'R': '+', 'S': '.'},
        {'L': 'M', 'B': '-', 'R': '.', 'S': '-'},
        {'L': 'M', 'B': '-', 'R': '-', 'S': '-'},
    ],
    [
        {'L': 'L', 'B': '+', 'R': '+', 'S': '+'},
        {'L': 'L', 'B': '+', 'R': '.', 'S': '.'},
        {'L': 'L', 'B': '+', 'R': '-', 'S': '.'},
        {'L': 'L', 'B': '.', 'R': '+', 'S': '.'},
        {'L': 'L', 'B': '.', 'R': '.', 'S': '.'},
        {'L': 'L', 'B': '.', 'R': '-', 'S': '-'},
        {'L': 'L', 'B': '-', 'R': '+', 'S': '-'},
        {'L': 'L', 'B': '-', 'R': '.', 'S': '-'},
        {'L': 'L', 'B': '-', 'R': '-', 'S': 'F'},
    ],
]
