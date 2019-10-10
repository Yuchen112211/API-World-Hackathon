def parse_activity(activities):
    return activities


def parse_meetup_events(events):
    rst = events
    for i in rst:
        i['resource'] = 'Meetup'
    return rst