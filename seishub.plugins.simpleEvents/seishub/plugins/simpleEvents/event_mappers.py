#!/usr/bin/env python
# -*- coding: utf-8 -*-
from seishub.core.core import Component, implements
from seishub.core.db.util import formatResults
from seishub.core.packages.interfaces import IMapper

import datetime
from sqlalchemy import Table, sql


class EventListMapper(Component):
    """
    Generates a list of available seismic events.
    """
    implements(IMapper)

    package_id = "simpleEvents"
    version = "0.0.0."
    mapping_url = "/simpleEvents/events/getList"

    def process_GET(self, request):
        """
        Function that will be called upon receiving a GET request for the
        aforementioned URL.
        """
        # Directly access the database via an SQLView which is automatically
        # created for every resource type and filled with all indexed values.
        tab = Table("/simpleEvents/event", request.env.db.metadata,
                    autoload=True)

        # Build up the query.
        query = sql.select([tab])

        # Potentially filter the results with a given minimum date.
        try:
            min_date = datetime.datetime(
                *map(int, request.args0.get("min_date").split("-")))
            query = query.where(tab.c["time"] >= min_date)
        except:
            pass

        # Execute the query.
        result = request.env.db.query(query)

        # Use a convenience function provided by SeisHub to get a nicely
        # formatted output.
        result = formatResults(request, result)
        result = result.replace("<html>", "<html><head>"
            "<link href='//netdna.bootstrapcdn.com/twitter-bootstrap/2.2.1/"
            "css/bootstrap.no-responsive.no-icons.min.css' rel='stylesheet'>"
            "</head>")
        result = result.replace("<body", "<body style='padding: 20px'")
        result = result.replace("<table",
            "<table class='table table-hover'")
        return result
