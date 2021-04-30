from odoo import api, SUPERUSER_ID

def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, dict())
    event_obj = env['calendar.event']
    events = event_obj.search([], order="id")
    for event in events:
        event.user2_id = event.user_id