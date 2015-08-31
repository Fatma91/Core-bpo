from openerp import models, fields, api, exceptions
from datetime import timedelta


class openacademy_courses(models.Model):
    _name = 'openacademy.courses'

    title = fields.Char(string="Course Title", required=True, defualt="Math")
    description = fields.Text(string="Course Description")
    responsible_id = fields.Many2one('res.users',
                                     ondelete='set null',string= "Responsible")
    session_ids = fields.One2many('openacademy.sessions',
                                  'course_id', string="Sessions")
    _sql_constraints = [('name_unique','UNIQUE(title)',
                         'The course title must be unique')]



class openacademy_sessions(models.Model):
    _name = 'openacademy.sessions'

    name= fields.Char(string="Session Name", required=True)
    start= fields.Date(string="Session Start Date",default=fields.Date.today)
    duration= fields.Float(string="The Duration of Session",
                           help=("Duration In Days"),digits=(2,5))
    active=fields.Boolean(string=" Session Case",default=True)
    seats= fields.Integer(string="No Of Seats")
    instructor_id = fields.Many2one('res.partner', string="Instructor",
                                    domain=['|', ('instructor', '=', True),
                                            ('category_id.name', 'ilike', "Teacher")])


    course_id = fields.Many2one('openacademy.courses',
                                ondelete='cascade',string="Course", required=True)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")
    taken_seats = fields.Float(string="Taken Seats", compute='_taken_seats')
    end= fields.Date(string="End Date",compute='_get_end_date',
                     inverse='_set_end_date',store=True,)
    hours = fields.Float(string="Duration In Hours",compute='_get_hours',
                         inverse='_set_hours')
    attendees_count = fields.Integer(string=" Attendees Count" ,
                                     compute='_get_attendees_count',store=True)
    color = fields.Integer()


    @api.one
    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        if not self.seats:
            self.taken_seats = 0.0
        else:
            self.taken_seats = 100.0 * len(self.attendee_ids) / self.seats

    @api.onchange('seats', 'attendee_ids')
    def _valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': "Incorrect 'seats' value",
                    'message': "The number of seats can not be negative",
                },
            }
        if self.seats < len(self.attendee_ids):
            return {
                'warning': {
                    'title': "Too many attendees",
                    'message': "Increase seats or decrease excess attendees",
                },
            }

    @api.one
    @api.constrains('instructor_id ', 'attendee_ids')
    def _check__that_instructor_not_attendees(self):
        if self.instructor_id and self.instructor_id in self.attendee_ids:
            raise exceptions.ValidationError("A instructor can't be an attendee")


    @api.one
    @api.depends('start', 'duration')
    def _get_end_date(self):
        if not (self.start and self.duration):
            self.end = self.start
            return
        start_date=fields.Datetime.from_string(self.start)
        duration = timedelta(days=self.duration, seconds=-1)
        self.end = start_date + duration

    @api.one
    def _set_end_date(self):
        if not (self.start and self.end):
            return

        start = fields.Datetime.from_string(self.start)
        end= fields.Datetime.from_string(self.end)
        self.duration = (end - start).days + 1

    @api.one
    @api.depends('duration')
    def _get_hours(self):
        self.hours = self.duration *24

    def _set_hours(self):
        self.duration = self.hours / 24

    @api.one
    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        self.attendees_count = len(self.attendee_ids)




