from openerp import models, fields


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
    instructor_id = fields.Many2one('res.partner', string="Instructor")
    course_id = fields.Many2one('openacademy.courses',
                                ondelete='cascade',string="Course", required=True)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")

