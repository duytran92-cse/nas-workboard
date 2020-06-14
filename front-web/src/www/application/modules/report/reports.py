import sys
from fpdf import FPDF

class BoardReportBuilder(object):
    def __init__(self):
        self.GOAL_COLOR_CODES = {
            'active': {
                'text': (59,115,188),
                'fill': (235,242,249)
            },
            'success': {
                'text': (0,100,0),
                'fill': (152,251,152),
            },
            'failed': {
                'text': (255,0,0),
                'fill': (255,204,204),
            },
            'rejected': {
                'text': (0,0,0),
                'fill': (240, 240, 240),
            }
        }
        self.STORY_COLOR_CODES = {
            'default': {
                'text': (0, 0, 0),
                'fill': (250, 250, 250),
            },
            'accepted': {
                'text': (0,100,0),
                'fill': (152,251,152),
            },
            'failed': {
                'text': (255,0,0),
                'fill': (255,204,204),
            },
            'icebox': {
                'text': (0,0,0),
                'fill': (240, 240, 240),
            }
        }

    def generate_report(self, data, filename):
        pdf = FPDF()
        pdf.set_auto_page_break(False)
        self.build_summary_page(pdf, data)
        self.build_goal_page(pdf, data)
        self.build_story_page(pdf, data)
        pdf.output(filename, 'F')
    def build_summary_page(self, pdf, data):
        pdf.add_page()
        pdf.set_font('Arial', '', 16)
        pdf.text(5, 15, data['board']['name'])

        # Team
        Y = 25
        pdf.set_text_color(0, 0, 0)
        pdf.set_font('Arial', 'B', 10)
        pdf.text(5, Y, 'Team')
        pdf.set_xy(5, Y)

        Y += 2
        pdf.set_text_color(255, 255, 255)
        pdf.set_fill_color(0, 0, 0)
        pdf.set_font('Arial', '', 10)
        pdf.set_xy(5, Y)
        pdf.cell(59, 7, 'Member', 0, 0, 'L', True)
        pdf.set_xy(65, Y)
        pdf.cell(139, 7, 'Workload', 0, 0, 'L', True)

        pdf.set_text_color(59,115,188)
        pdf.set_fill_color(235,242,249)
        for member in data['board']['team']:
            Y += 8
            pdf.set_xy(5, Y)
            pdf.cell(59, 7, member['user'], 0, 0, 'L', True)
            pdf.set_xy(65, Y)
            pdf.cell(139, 7, '', 0, 0, 'L', True)


        # Statistics
        Y += 20
        pdf.set_text_color(0, 0, 0)
        pdf.set_font('Arial', 'B', 10)
        pdf.text(5, Y, 'Statistics')
        pdf.set_xy(5, Y)
        Y += 2
        pdf.set_text_color(255, 255, 255)
        pdf.set_fill_color(0, 0, 0)
        pdf.set_font('Arial', '', 10)
        pdf.set_xy(5, Y)
        pdf.cell(59, 7, 'Goal', 0, 0, 'L', True)
        pdf.set_xy(65, Y)
        pdf.cell(139, 7, 'Total', 0, 0, 'L', True)

        for k, v in data['board']['goal_stats'].iteritems():
            color_code = self.GOAL_COLOR_CODES[k]
            pdf.set_text_color(color_code['text'][0], color_code['text'][1], color_code['text'][2])
            pdf.set_fill_color(color_code['fill'][0], color_code['fill'][1], color_code['fill'][2])

            Y += 8
            pdf.set_xy(5, Y)
            pdf.cell(59, 7, k, 0, 0, 'L', True)
            pdf.set_xy(65, Y)
            pdf.cell(139, 7, str(v), 0, 0, 'L', True)

        Y += 10
        pdf.set_text_color(255, 255, 255)
        pdf.set_fill_color(0, 0, 0)
        pdf.set_font('Arial', '', 10)
        pdf.set_xy(5, Y)
        pdf.cell(59, 7, 'Story', 0, 0, 'L', True)
        pdf.set_xy(65, Y)
        pdf.cell(139, 7, 'Total', 0, 0, 'L', True)

        for k, v in data['board']['story_stats'].iteritems():
            color_code = self.STORY_COLOR_CODES[k]
            pdf.set_text_color(color_code['text'][0], color_code['text'][1], color_code['text'][2])
            pdf.set_fill_color(color_code['fill'][0], color_code['fill'][1], color_code['fill'][2])

            Y += 8
            pdf.set_xy(5, Y)
            pdf.cell(59, 7, k, 0, 0, 'L', True)
            pdf.set_xy(65, Y)
            pdf.cell(139, 7, str(v), 0, 0, 'L', True)

    def build_goal_page(self, pdf, data):
        pdf.add_page()
        pdf.set_text_color(0, 0, 0)
        pdf.set_font('Arial', '', 16)
        pdf.text(5, 15, 'Goals')

        Y = 20
        pdf.set_text_color(255, 255, 255)
        pdf.set_fill_color(0, 0, 0)
        pdf.set_font('Arial', '', 8)
        pdf.set_xy(5, Y)
        pdf.cell(150, 5, 'Goal', 0, 0, 'L', True)
        pdf.set_xy(155, Y)
        pdf.cell(40, 5, '', 0, 0, 'L', True)
        pdf.set_xy(185, Y)
        pdf.cell(20, 5, '', 0, 0, 'L', True)
        for goal in data['goals']:
            color_code = self.GOAL_COLOR_CODES[goal['status']]
            pdf.set_text_color(color_code['text'][0], color_code['text'][1], color_code['text'][2])
            pdf.set_fill_color(color_code['fill'][0], color_code['fill'][1], color_code['fill'][2])

            Y += 5
            pdf.set_xy(5, Y)
            pdf.cell(10, 5, str(goal['id']), 0, 0, 'L', True)
            pdf.set_xy(15, Y)
            pdf.cell(150, 5, goal['title'], 0, 0, 'L', True)
            pdf.set_xy(155, Y)
            pdf.cell(40, 5, goal['user'], 0, 0, 'L', True)
            pdf.set_xy(185, Y)
            pdf.cell(20, 5, goal['status'], 0, 0, 'L', True)

    def build_story_page(self, pdf, data):
        pdf.add_page()
        pdf.set_text_color(0, 0, 0)
        pdf.set_font('Arial', '', 16)
        pdf.text(5, 15, 'Stories')

        Y = 15
        for c in data['stories']:
            Y += 5
            if Y > 280:
                pdf.add_page()
                Y = 15

            pdf.set_text_color(255, 255, 255)
            pdf.set_fill_color(0, 0, 0)
            pdf.set_font('Arial', '', 8)
            pdf.set_xy(5, Y)
            pdf.cell(150, 5, c['category'], 0, 0, 'L', True)
            pdf.set_xy(155, Y)
            pdf.cell(40, 5, '', 0, 0, 'L', True)
            pdf.set_xy(185, Y)
            pdf.cell(20, 5, '', 0, 0, 'L', True)
            for story in c['stories']:
                color_code = self.STORY_COLOR_CODES[story['status']]
                pdf.set_text_color(color_code['text'][0], color_code['text'][1], color_code['text'][2])
                pdf.set_fill_color(color_code['fill'][0], color_code['fill'][1], color_code['fill'][2])

                Y += 5
                if Y > 280:
                    pdf.add_page()
                    Y = 15

                pdf.set_xy(5, Y)
                pdf.cell(10, 5, str(story['id']), 0, 0, 'L', True)
                pdf.set_xy(15, Y)
                pdf.cell(150, 5, story['title'].encode('utf-8'), 0, 0, 'L', True)
                pdf.set_xy(155, Y)
                pdf.cell(40, 5, story['user'], 0, 0, 'L', True)
                pdf.set_xy(185, Y)
                pdf.cell(20, 5, story['status'], 0, 0, 'L', True)


class MonthlyPerformanceReportBuilder(object):
    def __init__(self):
        self.WORKLOAD_COLOR_CODE = {
            'H': 'green',
            'M': 'gray',
            'L': 'red'
        }
        self.BEHAVIOR_COLOR_CODE = {
            '+': 'green',
            '.':  'gray',
            '-': 'red'
        }
        self.RESULT_COLOR_CODE = {
            '+': 'green',
            '.':  'gray',
            '-': 'red'
        }
        self.SCORE_COLOR_CODE = {
            '+': 'green',
            '.': 'gray',
            '-': 'red',
            'A': 'blue',
            'F': 'red'
        }
        self.GOAL_COLOR_CODES = {
            'active': {
                'text': (59,115,188),
                'fill': (235,242,249)
            },
            'success': {
                'text': (0,100,0),
                'fill': (152,251,152),
            },
            'failed': {
                'text': (255,0,0),
                'fill': (255,204,204),
            },
            'rejected': {
                'text': (0,0,0),
                'fill': (240, 240, 240),
            }
        }
        self.STORY_COLOR_CODES = {
            'default': {
                'text': (0, 0, 0),
                'fill': (250, 250, 250),
            },
            'accepted': {
                'text': (0,100,0),
                'fill': (152,251,152),
            },
            'failed': {
                'text': (255,0,0),
                'fill': (255,204,204),
            },
            'icebox': {
                'text': (0,0,0),
                'fill': (240, 240, 240),
            }
        }
        self.STORY_RATING_COLOR_CODE = {
            '+': 'green',
            '-': 'red',
            '.': 'black'
        }

    def set_color_code(self, pdf, colorcode):
        if colorcode == 'black':
            pdf.set_text_color(0, 0, 0)
        if colorcode == 'gray':
            pdf.set_text_color(204, 204, 204)
        if colorcode == 'green':
            pdf.set_text_color(0, 100, 0)
        if colorcode == 'red':
            pdf.set_text_color(255, 0, 0)
        if colorcode == 'blue':
            pdf.set_text_color(0, 0, 240)

    def generate_report(self, data, filename):
        pdf = FPDF()
        pdf.set_auto_page_break(False)
        self.build_summary_page(pdf, data)
        for member in data['performances']:
            self.build_member_result_page(pdf, member)
        self.build_instruction_page(pdf, data)
        pdf.output(filename, 'F')

    def build_member_result_page(self, pdf, member):
        pdf.add_page()
        pdf.set_font('Arial', '', 16)
        pdf.set_text_color(0, 0, 0)
        pdf.set_fill_color(255, 255, 255)
        pdf.text(5, 15, member['name'])

        # PERFORMANCE
        pdf.set_font('Arial', 'B', 9)
        pdf.set_xy(174, 9)
        pdf.set_fill_color(235,242,249)
        self.set_color_code(pdf, self.WORKLOAD_COLOR_CODE[member['performance']['L']])
        pdf.cell(7, 7, member['performance']['L'], 0, 0, 'C', True)

        pdf.set_xy(182, 9)
        pdf.set_text_color(200, 200, 200)
        pdf.set_fill_color(235,242,249)
        pdf.cell(7, 7, '?', 0, 0, 'C', True)

        pdf.set_xy(190, 9)
        pdf.set_text_color(200, 200, 200)
        pdf.set_fill_color(235,242,249)
        pdf.cell(7, 7, '?', 0, 0, 'C', True)

        pdf.set_xy(198, 9)
        pdf.set_fill_color(255,245,238)
        self.set_color_code(pdf, self.SCORE_COLOR_CODE[member['performance']['S']])
        pdf.cell(7, 7, member['performance']['S'], 0, 0, 'C', True)

        # Responsibilities
        y = 20
        pdf.set_xy(5, y)
        pdf.set_text_color(255, 255, 255)
        pdf.set_fill_color(0, 0, 0)
        pdf.set_font('Arial', '', 8)
        pdf.cell(200, 5, 'Work summary', 0, 0, 'L', True)
        i = 0
        for w in member['work_summaries']:
            y += 5
            i += 1
            pdf.set_text_color(0, 100, 0)
            pdf.set_fill_color(152,251,152)
            pdf.set_xy(5, y)
            pdf.cell(10, 5, str(i), 0, 0, 'L', True)
            pdf.set_xy(15, y)
            pdf.cell(190, 5, w.encode('utf-8'), 0, 0, 'L', True)

        # Goals
        y += 5
        pdf.set_xy(5, y)
        pdf.set_text_color(255, 255, 255)
        pdf.set_fill_color(0, 0, 0)
        pdf.set_font('Arial', '', 8)
        pdf.cell(120, 5, 'Goal', 0, 0, 'L', True)
        pdf.set_xy(125, y)
        pdf.cell(30, 5, '', 0, 0, 'L', True)
        pdf.set_xy(155, y)
        pdf.cell(50, 5, '', 0, 0, 'L', True)
        for goal in member['goals']:
            color_code = self.GOAL_COLOR_CODES[goal['result']]
            pdf.set_text_color(color_code['text'][0], color_code['text'][1], color_code['text'][2])
            pdf.set_fill_color(color_code['fill'][0], color_code['fill'][1], color_code['fill'][2])
            y += 5
            pdf.set_xy(5, y)
            pdf.cell(10, 5, str(goal['id']), 0, 0, 'L', True)
            pdf.set_xy(15, y)
            pdf.cell(110, 5, goal['goal'].encode('utf-8'), 0, 0, 'L', True)
            pdf.set_xy(125, y)
            pdf.cell(30, 5, goal['result'], 0, 0, 'L', True)
            pdf.set_xy(155, y)
            pdf.cell(50, 5, goal['board'], 0, 0, 'L', True)

        # Stories
        y += 5
        pdf.set_xy(5, y)
        pdf.set_text_color(255, 255, 255)
        pdf.set_fill_color(0, 0, 0)
        pdf.set_font('Arial', '', 8)
        pdf.cell(120, 5, 'Story', 0, 0, 'L', True)
        pdf.set_xy(125, y)
        pdf.cell(30, 5, '', 0, 0, 'L', True)
        pdf.set_xy(155, y)
        pdf.cell(50, 5, 'Rating', 0, 0, 'L', True)
        for story in member['stories']:
            pdf.set_font('Arial', '', 8)
            color_code = self.STORY_COLOR_CODES[story['result']]
            pdf.set_text_color(color_code['text'][0], color_code['text'][1], color_code['text'][2])
            pdf.set_fill_color(color_code['fill'][0], color_code['fill'][1], color_code['fill'][2])
            y += 5
            pdf.set_xy(5, y)
            pdf.cell(10, 5, str(story['id']), 0, 0, 'L', True)
            pdf.set_xy(15, y)
            pdf.cell(110, 5, story['story'].encode('utf-8'), 0, 0, 'L', True)
            pdf.set_xy(125, y)
            pdf.cell(30, 5, story['result'], 0, 0, 'L', True)
            pdf.set_xy(155, y)

            pdf.set_font('Arial', '', 8)
            self.set_color_code(pdf, self.STORY_RATING_COLOR_CODE[story['rating']])
            pdf.cell(50, 5, "%s %s" % (story['rating'] if story['rating'] != '.' else '', story['notes']), 0, 0, 'L', True)

    def build_summary_page(self, pdf, data):
        pdf.add_page()

        pdf.set_font('Arial', '', 16)
        pdf.text(5, 15, 'Monthly Performance Report')
        pdf.text(180, 15, '%s/%s' % (data['month'], data['year']))

        # PERFORMANCE REPORT
        pdf.set_font('Arial', 'B', 10)
        pdf.text(5, 25, 'Summary')
        pdf.set_xy(5, 30)

        pdf.set_text_color(255, 255, 255)
        pdf.set_fill_color(0, 0, 0)
        pdf.set_font('Arial', '', 10)
        pdf.cell(79, 7, 'Member', 0, 0, 'L', True)

        pdf.set_text_color(59,115,188)
        pdf.set_fill_color(235,242,249)
        pdf.set_xy(85, 30)
        pdf.cell(9, 7, 'L', 0, 0, 'C', True)
        pdf.set_xy(95, 30)
        pdf.cell(9, 7, 'B', 0, 0, 'C', True)
        pdf.set_xy(105, 30)
        pdf.cell(9, 7, 'R', 0, 0, 'C', True)

        pdf.set_text_color(0, 0, 0)
        pdf.set_fill_color(255,245,238)
        pdf.set_xy(115, 30)
        pdf.cell(9, 7, 'S', 0, 0, 'C', True)

        pdf.set_text_color(255,255,255)
        pdf.set_fill_color(0,0,0)
        pdf.set_xy(125, 30)
        pdf.cell(79, 7, 'Notes', 0, 0, 'L', True)

        y = 30
        for perf in data['performances']:
            y += 8
            pdf.set_font('Arial', '', 10)
            pdf.set_xy(5, y)
            pdf.set_text_color(0, 0, 0)
            pdf.set_fill_color(240, 240, 240)
            pdf.cell(79, 7, perf['name'], 0, 0, 'L', True)
            pdf.set_font('Arial', 'B', 10)

            pdf.set_font('Arial', 'B', 10)
            pdf.set_xy(85, y)
            self.set_color_code(pdf, self.WORKLOAD_COLOR_CODE[perf['performance']['L']])
            pdf.set_fill_color(235,242,249)
            pdf.cell(9, 7, perf['performance']['L'], 0, 0, 'C', True)

            pdf.set_xy(95, y)
            pdf.set_text_color(200, 200, 200)
            pdf.set_fill_color(235,242,249)
            pdf.cell(9, 7, '?', 0, 0, 'C', True)

            pdf.set_xy(105, y)
            pdf.set_text_color(200, 200, 200)
            pdf.set_fill_color(235,242,249)
            pdf.cell(9, 7, '?', 0, 0, 'C', True)

            pdf.set_xy(115, y)
            self.set_color_code(pdf, self.SCORE_COLOR_CODE[perf['performance']['S']])
            pdf.set_fill_color(255,245,238)
            pdf.cell(9, 7, perf['performance']['S'], 0, 0, 'C', True)

            pdf.set_font('Arial', '', 10)
            pdf.set_xy(125, y)
            pdf.set_text_color(0, 0, 0)
            pdf.set_fill_color(240,240,240)
            pdf.cell(79, 7, perf['performance']['notes'], 0, 0, 'L', True)

    def build_instruction_page(self, pdf, data):
        # Legend
        y = 20
        pdf.add_page()
        pdf.set_text_color(0, 0, 0)
        pdf.set_font('Arial', 'B', 10)
        pdf.text(5, y, 'Legend')

        y += 3
        pdf.set_xy(5, y)
        pdf.set_font('Arial', 'B', 10)
        pdf.set_text_color(59,115,188)
        pdf.set_fill_color(235,242,249)
        pdf.cell(9, 7, 'L', 0, 0, 'C', True)

        pdf.set_font('Arial', '', 10)
        pdf.set_xy(15, y)
        pdf.cell(189, 7, 'Your work load (or contribution), relatively based on your job position / salary', 0, 0, 'L', True)

        y += 8
        pdf.set_xy(15, y)
        pdf.cell(9, 7, 'H',  0, 0, 'C', True)
        pdf.set_xy(25, y)
        pdf.cell(179, 7, ' High workload / contribution', 0, 0, 'L', True)

        y += 8
        pdf.set_xy(15, y)
        pdf.cell(9, 7, 'M',  0, 0, 'C', True)
        pdf.set_xy(25, y)
        pdf.cell(179, 7, ' Medium workload / contribution', 0, 0, 'L', True)

        y += 8
        pdf.set_xy(15, y)
        pdf.set_font('Arial', '', 10)
        pdf.cell(9, 7, 'L',  0, 0, 'C', True)
        pdf.set_xy(25, y)
        pdf.cell(179, 7, ' Low workload / contribution', 0, 0, 'L', True)

        y += 8
        pdf.set_xy(5, y)
        pdf.set_font('Arial', 'B', 10)
        pdf.set_text_color(59,115,188)
        pdf.set_fill_color(235,242,249)
        pdf.cell(9, 7, 'B', 0, 0, 'C', True)

        pdf.set_font('Arial', '', 10)
        pdf.set_xy(15, y)
        pdf.cell(189, 7, 'Your behavior / work ethnic, relatively based on company core values, culture and work ethnic', 0, 0, 'L', True)

        y += 8
        pdf.set_xy(15, y)
        pdf.cell(9, 7, '+',  0, 0, 'C', True)
        pdf.set_xy(25, y)
        pdf.cell(179, 7, ' Positive behavior', 0, 0, 'L', True)

        y += 8
        pdf.set_xy(15, y)
        pdf.cell(9, 7, '.',  0, 0, 'C', True)
        pdf.set_xy(25, y)
        pdf.cell(179, 7, ' Neutral behavior', 0, 0, 'L', True)

        y += 8
        pdf.set_xy(15, y)
        pdf.set_font('Arial', '', 10)
        pdf.cell(9, 7, '-',  0, 0, 'C', True)
        pdf.set_xy(25, y)
        pdf.cell(179, 7, ' Negative behavior', 0, 0, 'L', True)

        y += 8
        pdf.set_xy(5, y)
        pdf.set_font('Arial', 'B', 10)
        pdf.set_text_color(59,115,188)
        pdf.set_fill_color(235,242,249)
        pdf.cell(9, 7, 'R', 0, 0, 'C', True)

        pdf.set_font('Arial', '', 10)
        pdf.set_xy(15, y)
        pdf.cell(189, 7, 'Your work result', 0, 0, 'L', True)

        y += 8
        pdf.set_xy(15, y)
        pdf.cell(9, 7, '+',  0, 0, 'C', True)
        pdf.set_xy(25, y)
        pdf.cell(179, 7, ' Good', 0, 0, 'L', True)

        y += 8
        pdf.set_xy(15, y)
        pdf.cell(9, 7, '.',  0, 0, 'C', True)
        pdf.set_xy(25, y)
        pdf.cell(179, 7, ' OK', 0, 0, 'L', True)

        y += 8
        pdf.set_xy(15, y)
        pdf.set_font('Arial', '', 10)
        pdf.cell(9, 7, '-',  0, 0, 'C', True)
        pdf.set_xy(25, y)
        pdf.cell(179, 7, ' Bad', 0, 0, 'L', True)


        # Scoring schema
        y = 130
        pdf.set_text_color(0, 0, 0)
        pdf.set_font('Arial', 'B', 10)
        pdf.text(5, y, 'Scoring schema')
        for sc in data['scoring_schema']:
            y += 6
            pdf.set_text_color(59,115,188)
            pdf.set_fill_color(235,242,249)
            for i in range(0, 9):
                pdf.set_xy(i*22 + 5, y)
                pdf.set_fill_color(235,242,249)
                self.set_color_code(pdf, self.WORKLOAD_COLOR_CODE[sc[i]['L']])
                pdf.cell(5, 5, sc[i]['L'], 0, 0, 'C', True)

                pdf.set_xy(i*22 + 10, y)
                pdf.set_fill_color(235,242,249)
                self.set_color_code(pdf, self.BEHAVIOR_COLOR_CODE[sc[i]['B']])
                pdf.cell(5, 5, sc[i]['B'], 0, 0, 'C', True)

                pdf.set_xy(i*22 + 15, y)
                pdf.set_fill_color(235,242,249)
                self.set_color_code(pdf, self.RESULT_COLOR_CODE[sc[i]['R']])
                pdf.cell(5, 5, sc[i]['R'], 0, 0, 'C', True)

                pdf.set_xy(i*22 + 20, y)
                pdf.set_fill_color(255,245,238)
                self.set_color_code(pdf, self.SCORE_COLOR_CODE[sc[i]['S']])
                pdf.cell(5, 5, sc[i]['S'], 0, 0, 'C', True)
