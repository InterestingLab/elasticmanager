
def select_indices( client, prefix, timestring, time_unit, older_than_days=None, newer_than_days=None ):
    """
    time_unit: One of hours, days, weeks, months, NO years!!!
    older_than_days, newer_than_days:
        Value of older_than_days or newer_than_days should be > 0
        If older_than_days and newer_than_days are both set, newer_than_days should be greater than older_than_days
        older_than_days = n will filters indices n days before today,
        newer_than_days = m will filters indices from m days before today to today
    """

    indices = curator.get_indices( client )

    filter_list = []

    index_regex = prefix + curator.get_date_regex( timestring )
    filter_list.append( curator.build_filter( kindOf='regex', value=index_regex  ) )

    if older_than_days:
        filter_list.append(
            curator.build_filter(
                kindOf='older_than', value=older_than_days, time_unit=time_unit,
                timestring=timestring
            )
        )

    if newer_than_days:
        filter_list.append(
            curator.build_filter(
                kindOf='newer_than', value=newer_than_days, time_unit=time_unit,
                timestring=timestring
            )
        )

    working_list = indices
    for _filter in filter_list:
        working_list = curator.apply_filter(working_list, **_filter)

    return working_list


def indices_in_days( days_in_advance, prefix, time_pattern, pattern_interval ):
    indices = []

    dt_fun = '_relativedelta_' + pattern_interval.lower()
    dt = globals()[ dt_fun ]()

    start = datetime.utcnow()
    end = start + relativedelta.relativedelta( days=days_in_advance + 1 )

    while start < end:
        index = prefix + start.strftime( time_pattern )
        indices.append( index )
        start += dt

    return indices


def _relativedelta_hours():
    return relativedelta.relativedelta( hours=1 )

def _relativedelta_days():
    return relativedelta.relativedelta( days=1 )

def _relativedelta_weeks():
    return relativedelta.relativedelta( weeks=1 )

def _relativedelta_months():
    return relativedelta.relativedelta( months=1 )

def _relativedelta_years():
    return relativedelta.relativedelta( years=1 )

