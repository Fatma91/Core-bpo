from openerp import models, fields,api


class openacademy_courses(models.Model):
    _name = 'openacademy.courses'

    title = fields.Char(string="Course Title", required=True, defualt="Math")
    description = fields.Text(string="Course Description")
    responsible_id = fields.Many2one('res.users',ondelete='set null',string= "Responsible")
    session_ids = fields.One2many('openacademy.sessions', 'course_id', string="Sessions")



class openacademy_sessions(models.Model):
    _name = 'openacademy.sessions'

    name= fields.Char(string="Session Name", required=True)
    start= fields.Date(string="Session Start Date")
    duration= fields.Float(string="The Duration of Session",
                           help=("Duration In Days"),digits=(2,5))
    seats= fields.Integer(string="No Of Seats")
    instructor_id = fields.Many2one('res.partner', string="Instructor",
                                    domain=['|', ('instructor', '=', True),('category_id.name', 'ilike', "Teacher")])


    course_id = fields.Many2one('openacademy.courses',
                                ondelete='cascade',string="Course", required=True)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")
    taken_seats = fields.Float(string="Taken Seats", compute='_taken_seats')

    @api.one
    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        if not self.seats:
            self.taken_seats = 0.0
        else:
            self.taken_seats = 100.0 * len(self.attendee_ids) / self.seats