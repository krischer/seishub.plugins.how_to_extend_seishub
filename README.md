# Template for new SeisHub Plug-ins

This repository contains a very simple but working SeisHub plug-in intended as a
template for new SeisHub plug-ins. It is also a means of documenting how to
extend SeisHub with your own functionality.

## Tutorial for a new SeisHub Plug-in

This short tutorial will walk you through the steps of creating a simple
SeisHub plug-in. In the course of the tutorial we will develop a simple plug-in
to store seismic events.

### Prerequisites

Developing a plug-in for SeisHub is not particularly difficult but some skill
are required before you can start.

* SeisHub is written in [Python](http://www.python.org/) (Version 2.6 and 2.7
  should work) so at least a limited knowledge of Python is required. But don't
  fret as Python is very simple to learn. There are a number of free and good
  resource available online, e.g. [Learn Python The Hard Way](http://learnpythonthehardway.org/book/),
  [Dive Into Python](http://www.diveintopython.net/),
  [The official Python tutorial](http://docs.python.org/2/tutorial/index.html), ...
* SeisHub stores all data as [XML](http://en.wikipedia.org/wiki/Xml) files.
  Some familiarity with it and the related technologies
  [XSD](http://en.wikipedia.org/wiki/Xsd) and
  [XSLT](http://en.wikipedia.org/wiki/Xslt) is also advisable.
* Depending on how sophisticated your plug-in will be, some insights into
  [relational databases](http://en.wikipedia.org/wiki/Relational\_database)
  might prove useful.

### Things to Know About SeisHub


[SeisHub](http://github.com/barsch/seishub.core) is a XML database meaning
that it, as a fundamental unit, stores XML documents. For you this means that
your data has to be available in XML. This is feasible in most cases. Later on
we will also learn how to deal with binary data, e.g.  images, large binary
time series in a custom format, ...

#### Terminology

 * **Package:** A component to structure stored files into categories. A
     SeisHub plug-in can define one or more packages. Every package can store
     resources of one or more different resource types.
 * **Document:** An actual XML document.
 * **Resource:** A logical XML document with an associated resource type. One
     resource can have multiple revisions, each a seperate document.
 * **Resource Type:** Every resource needs to have a type, called a resource
     type.
 * **Mapper:** A mapper (in a SeisHub plug-in) is a Python function that is
     called everytime a specified URL is requested. Enables completely
     customized SeisHub behaviour.

### Designing the Plug-in

Let's assume you have a large collection of seismic events and want to store
them in SeisHub. First we need to define the structure of the XML files that we
want to store. In this case we only want to store the most basic information
about an event. ( *Please note that this only serves to demonstrate SeisHub. If
you really want to store event data you are better off using the standardized
[QuakeML](https://quake.ethz.ch/quakeml/Documents) format.* ) Our simple XML
format looks akin to the following:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<seismic_event>
    <latitude>12.123</latitude>
    <longitude>52.234</longitude>
    <depth_in_km>22.23</depth_in_km>
    <time>2012-10-26T09:33:11.123Z</time>
    <magnitude>2.1</magnitude>
</seismic_event>
```

At the end of this tutorial, you will be able to store events in the predefined
format, validate them and reject files that deviate from the format.
Furthermore you will be able to transform the data on the fly to different
formats and query the data with a web based interface.


### Let's get started

The first step is to clone this repository. This is already a fully functional
plug-in but it does not really do much.

```bash
$ git clone https://github.com/krischer/seishub.plugins.template_tutorial
```

### The Plug-in Structure

The current directory structure along with some additional information is shown
in the next block. The basic structure must not be changed. This is due to the
way Python modules work. The `__init__.py` files are also necessary so don't
delete them.

```
seishub.plugins.template_tutorial     <- Rename this folder to "seishub.plugins.simpleEvents"
├── README.md
├── seishub
│   ├── __init__.py
│   └── plugins
│       ├── __init__.py
│       └── template_tutorial         <- Rename this folder to "simpleEvents"
│           ├── __init__.py
│           ├── LICENSE.txt           <- Make sure the license suits your purpose.
│           └── package.py            <- Currently the only file of the actual plugin.
└── setup.py                          <- Installation script
```

Right now the plug-in is called `seishub.plugins.template_tutorial` which is of
course not a very good name. Let's start by renaming the folder to
`seishub.plugins.simpleEvents`. Also rename the
`seishub/plugins/template_tutorial` folder to `seishub/plugins/simpleEvents`.


### Changes to the installation script

Python modules are installed with the help of the `setup.py` file. The
`setup.py` file in this module is commented and should be self-explanatory.
Change things as you see fit. The only necessary change is to swap all
occurrences of `seishub.plugins.template_tutorial` with
`seishub.plugins.simpleEvents`.


### Add resources

The actual resources of the plug-in are defined in
`seishub/plugins/simpleEvents/package.py`. Two classes are already defined in
the file:

* `TemplateComponent`
* `SomeTemplateResourceType`

both inheriting from `seishub.core.core.Component`. Both also implement an
interface. Interfaces in SeisHub are
[Zope interfaces](http://wiki.zope.org/Interfaces/FrontPage). If you implement
an interface you give a promise that the class has certain attributes and
methods defined in the interface specification. The interface are defined in
`seishub.core.packages.interface`.

#### Defining a new package

A package in SeisHub is the root element of a plug-in (actually several packages
can be defined in one plug-in). You can think of it as a folder or category for
the functionality of the plug-in. Lets us first change the `TemplateComponent`
class. It inherits from `Component` as all plugin components have to.
Furthermore it implements the `IPackage` interface and thus it needs to have
two attributes:

* **package_id:**
    Defines the package ID of this package. Single string representing a unique
    package ID.
* **version:** Sets the version of this package. Version may be any string.


We want to have a package dealing with a simple event specification so change
the `TemplateComponent` class to

```python
class SimpleEventsComponent(Component):
    """
    Package dealing with a simple event format.
    """
    implement(IPackage)
    package_id = "simpleEvents"
    version = "0.0.0"
```

This has the consequence that all resources of this package will be available
under *SEISHUB_URL/xml/simpleEvents/RESOURCE_TYPE*.

#### Defining a new resource.

A package can have an unlimited number of different resource types. We will now
define a new resource type `event` that is designed to store event in the
custom XML format we previously defined.

Resources implement the `IResourceType` interface and thus have the
**package_id** and **version** attributes as defined above plus one additional
attribute:

* **resourcetype_id:** Defines the resource type ID of this package. Single
  string representing a unique resource type ID.

In our example we want to have a event resource so go ahead and change the
**SomeTemplateResourceType** class so it looks akin to the following:

```python
class EventResource(Component):
    """
    Simple event resource type.
    """
    implements(IResourceType)
    package_id = "simpleEvents"
    version = "0.0.0."
    resourcetype_id = "event"
```

Now all events will be available under
*SEISHUB_URL/xml/simpleEvents/event/EVENT_NAME*. Now we can already upload
some events.


### Testing the Plug-in

#### Installation

First of all [SeisHub](https://github.com/barsch/seishub.core) needs to be
installed. If you do not have it installed, follow the instructions on the
site; SQLite is suitable as a database backend for now.

Assuming you modified the `setup.py` as described above, you can install the
plug-in with either

```bash
$ python setup.py develop
```

or (in the same directory as the `setup.py` file)

```bash
$ pip install -v -e .
```

depending on your preference. Make sure to install it as `develop` or `-e`
which will only place a link to the plug-in in the `site-packages` directory so
you can still edit the code and see changes reflected immediately.


#### Setup new SeisHub instance

Now create a new SeisHub instance somewhere with

```bash
$ seishub-admin initenv PATH/TO/INSTANCE
```

`PATH/TO/INSTANCE` must not exist. You can now start the SeisHub server with

```bash
$ PATH/TO/INSTANCE/bin/debug.sh
```

Assuming you did not change any of the default settings you should be able to
navigate to `http://localhost:8080/manage` in your web browser. The default
login is `admin:admin`. This opens the admin panel of the SeisHub instance.

By default the plug-in will not be activated. So click on "Plug-ins" on the left
hand side. If the `simpleEvents` plug-in does not show up, something went
wrong. Check the mark next to `seishub.plugins.simpleEvents.package` and press
`Save`. The plug-in should now be fully operational. While at it you might also
want to enable the `seishub.core.packages.admin.web.components` and
`seishub.core.packages.admin.web.catalog` components.


#### Uploading some files

Create a test file, e.g. by copying the xml from above and upload it via `POST`
to `http://localhost:8080/xml/simpleEvents/event/RESOURCE_NAME.xml`. Depending
on the configuration username and password might also be necessary.
`RESOURCE_NAME.xml` is optional but it is a good idea to pass one, otherwise a
random one will be assigned to the resource.

The task can be achieved with the help of the curl command but numerous other
methods also exist.

```bash
$ curl -v --data-binary @test.xml -u admin:admin -X POST http://localhost:8080/xml/simpleEvents/event/test.xml
```

The file can be downloaded via HTTP `GET`, e.g.

```bash
$ curl -u admin:admin -X GET http://localhost:8080/xml/simpleEvents/event/test.xml | cat
```


### Making it useful

So far it is nothing else but a glorified XML file storage that will make sure
that every uploaded file is a valid XML file. That's about it. Let's add some
more functionality to it.


#### Validating uploaded files

You might have noticed that you can upload any file, as long as it is a valid
XML file. Usually you have a pretty good idea about what you want to store and
thus you want to restrict uploads to, in some sense, valid files.

This is done via XSD schemas. Creating these is fairly complex but only has to
be done once and a number of
[graphical editors](http://en.wikipedia.org/wiki/XML_Schema_Editor) are
available to help with it.

The XSD schema we are going to use for our example restrict latitude,
longitude, depth and magnitude to sensible values and makes sure that given
time is valid as well. This is a very simple schema and they can get
arbitrarily complex and thus are a very powerful tool.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<schema xmlns="http://www.w3.org/2001/XMLSchema">
    <element name="seismic_event">
        <complexType>
            <sequence>
                <element name="latitude" maxOccurs="1" minOccurs="1">
                    <simpleType>
                        <restriction base="float">
                            <maxInclusive value="90.0"></maxInclusive>
                            <minInclusive value="-90.0"></minInclusive>
                        </restriction>
                    </simpleType>
                </element>
                <element name="longitude" maxOccurs="1" minOccurs="1">
                    <simpleType>
                        <restriction base="float">
                            <minInclusive value="-180.0"></minInclusive>
                            <maxInclusive value="180.0"></maxInclusive>
                        </restriction>
                    </simpleType>
                </element>
                <element name="depth_in_km" maxOccurs="1" minOccurs="1">
                    <simpleType>
                        <restriction base="float">
                            <minInclusive value="-10.0"></minInclusive>
                            <maxInclusive value="2000.0"></maxInclusive>
                        </restriction>
                    </simpleType>
                </element>
                <element name="time" type="dateTime" maxOccurs="1"
                    minOccurs="1">
                </element>
                <element name="magnitude" maxOccurs="1" minOccurs="1">
                    <simpleType>
                        <restriction base="float">
                            <minInclusive value="-10.0"></minInclusive>
                            <maxInclusive value="11.0"></maxInclusive>
                        </restriction>
                    </simpleType>
                </element>
            </sequence>
        </complexType>
    </element>
</schema>
```


Create a file called `simple_events.xsd`, paste the schema definition and place
it in a `xsd` subfolder in the directory where the `package.py` resides. To
validate all uploaded files with a schema, a scheme needs to be registered for
the given resource type. This is done with the `registerSchema()` function. Add
it to the `EventResource` class definition:

```python
class EventResource(Component):
    """
    Simple event resource type.
    """
    implements(IResourceType)
    package_id = "simpleEvents"
    version = "0.0.0."
    resourcetype_id = "event"
    # Use the get_path() helper function to avoid any path issues.
    registerSchema(get_path("xsd", "simple_events.xsd"), "XMLSchema")
```

Restarting the SeisHub server and attempting to upload an incorrect file will
result in a failure and a (hopefully) meaningful error message, e.g.

```
Resource-validation against schema 'simpleEvents_event_simple_events.xsd' failed.
(Could not validate document.
    (Element 'latitude': [facet 'maxInclusive'] The value '112.123' is greater
     than the maximum value allowed ('90.0')., line 2)
)
```

Now we have ensured that only files that satisfy our requirements will end up
in the database.


#### Transforming the output

SeisHub internally stores all documents as XML documents which oftentimes might
not be very practical for the user. To deal with this SeisHub can transform the
output with XSLT stylesheets.

We are going to implement a style sheet that converts an event to the kml
format so it can be viewed with Google Maps.

In technical terms we want to convert

```xml
<?xml version="1.0" encoding="UTF-8"?>
<seismic_event>
    <latitude>12.123</latitude>
    <longitude>52.234</longitude>
    <depth_in_km>22.23</depth_in_km>
    <time>2012-10-26T09:33:11.123Z</time>
    <magnitude>2.1</magnitude>
</seismic_event>
```

to

```xml
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
  <Placemark>
    <name>Event</name>
    <description>Magnitude: 2.1, Time: 2012-10-26T09:33:11.123Z</description>
    <Point>
      <coordinates>12.123,52.234</coordinates>
    </Point>
  </Placemark>
</Document>
</kml>
```

Creating XSLT stylesheets is again fairly involved. A good editor, with a 30
day free trial period and academic licences available, is
[oXygen](http://www.oxygenxml.com/).

Copy the following stylesheet to a file called `simple_events.xsl` in a newly
created `xslt` subdirectory in the plug-in source code directory.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:output method="xml" indent="yes" encoding="UTF-8"/>
    <xsl:template match="/seismic_event">
        <kml xmlns="http://www.opengis.net/kml/2.2">
            <Document>
                <Placemark>
                    <name>Event</name>
                    <description>Magnitude: <xsl:value-of select="magnitude" />, Time: <xsl:value-of select="time" /></description>
                    <Point>
                        <coordinates><xsl:value-of select="latitude" />, <xsl:value-of select="longitude" /></coordinates>
                    </Point>
                </Placemark>
            </Document>
        </kml>
    </xsl:template>
</xsl:stylesheet>
```

Registering the stylesheet happens with the `registerStylesheet()` function.
Add it to the `EventResource` class definition so it looks like this:

```python
class EventResource(Component):
    """
    Simple event resource type.
    """
    implements(IResourceType)
    package_id = "simpleEvents"
    version = "0.0.0."
    resourcetype_id = "event"
    # Use the get_path() helper function to avoid any path issues.
    registerSchema(get_path("xsd", "simple_events.xsd"), "XMLSchema")
    registerStylesheet(get_path("xslt", "simple_events.xsl"), "kml")
```

After restarting the SeisHub server, any previously uploaded resource will be
converted to kml on-the-fly, if `?format=kml` is appended to the URL. This file
can be openend with Google Earth.

```bash
$ curl -u admin:admin -X GET "http://localhost:8080/xml/simpleEvents/event/test.xml?format=kml" -o test.kml
$ googleearth `realpath test.kml`
```

XSLT's are particularly well suited to convert XML documents to human-readable
X(HTML) webpages. In the context of SeisHub they are often used to present
data in a tabular form, on a map or, if used as a RESTful webservice to convert
a document to JSON.


#### Indexing documents

One of SeisHub's strong points is the ability to build a relational database
from certain key values in your XML documents. This results in SeisHub being
able to store and quickly search large amounts of data. Only indexed values are
searchable in a performant way (otherwise a full text search of every XML
document has to be performed). Therefore you need to specify which values you
want to be able to search after for every resource type. No need to worry if
you change your mind at some point as you can always reindex your documents
which is a reasonable quick procedure.

So in our example lets assume we want to be able to search for events depending
on latitude, longitude and the time. We therefore need to register three
indices for the Event resource type. This is done with the `registerIndex()`
function. It takes three arguments: name of the index (name of the row in the
database), an xpath to the value in the XML document, and the type of the
index. Be careful to choose the correct type, otherwise it will be inefficient
or will potentially not work all. Available types are "text", "numeric",
"float", "datetime", "boolean", "date", "integer", and "timestamp".

An [XPath](http://en.wikipedia.org/wiki/Xpath) is, in its simplest form, like a
filepath for an XML document and quite intuitive to use.

The indices also have to be registered in the class definition, so our
`EventResource` is now:

```python
class EventResource(Component):
    """
    Simple event resource type.
    """
    implements(IResourceType)
    package_id = "simpleEvents"
    version = "0.0.0."
    resourcetype_id = "event"
    # Use the get_path() helper function to avoid any path issues.
    registerSchema(get_path("xsd", "simple_events.xsd"), "XMLSchema")
    registerStylesheet(get_path("xslt", "simple_events.xsl"), "kml")
    # Register three indices.
    registerIndex("latitude", "/seismic_event/latitude", "float")
    registerIndex("longitude", "/seismic_event/longitude", "float")
    registerIndex("time", "/seismic_event/time", "datetime")
```

The indexing will happen upon resource uploading. If you previously uploaded
some data, you will need to reindex the database. This can be done in the admin
webinterface under Components/Indexes.

The database can now be queried over the defined indices.


#### Custom Mappers

One of SeisHub big strength's is the ability to defined custom so-called
mappers for the webservices. A mapper is a user-defined Python function that is
evoked upon visiting a certain URL. Therefore a mapper can do anything that a
user desires. Examples would be to run localization algorithms, query
datacenters for similar events or maybe plot some beachballs.

In our example, let's go for a very obvious use case of mappers. The previously
created indices are fine if you want to query the database directly. Due to
security reasons, the database cannot be queried directly via the webinterface.
So let's create a mapper to have be able to search for events in the SeisHub
database. For the sake of simplicity it is only possible to restrict the
minimum time of the returned events during the search.

A mapper basically needs two things to work. First it requires the URL for
which it will be invoked. Furthermore it requires one function per HTTP method
you want to support (possible are GET, POST, PUT, and DELETE). If one or more
functions are missing, the mapper will simply not exists for the missing HTTP
methods. Only GET must be supported.

Mappers implement *IMapper* and therefore has three attributes. **package_id**
and **version** are defined as seen before. One additional attribute is
required:

 * **mapping_url:** Defines the absolute URL of this mapping.  Single string
 representing a unique mapping URL.

For import and initialization reasons, the mappers have to be defined in a
different file than the previous classes. So create a file `event_mappers.py`
in the same directory and paste the following code into it. It is heavily
commented and should be fairly self-explanatory.

```python
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
        return result
```

The `__init__.py` also needs to be updated to import the new file. So open it
and change it to

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from package import *
from event_mappers import *
```

After restarting the SeisHub server you have to activate the event mappers in
the webinterface at General/Plug-ins. Now you can get a list of all events with

```
http://localhost:8080/simpleEvents/events/getList
```

You can also abitrarily restrict the minimum date with

```
http://localhost:8080/simpleEvents/events/getList&min_date=2012-01-01
```

which will only return events that have occured after the specified date. The
`formatResults()` function is a convenience method provided by SeisHub which
results in two additional formats being available. Use

```
http://localhost:8080/simpleEvents/events/getList?format=json
```

or

```
http://localhost:8080/simpleEvents/events/getList?format=xhtml
```

to have a look.

The nice thing about it is that you can do whatever you want in there and
return whatever you want. You don't like the barebones look of the `xhtml`
format? Just hack in a stylesheet by replacing the last two lines with

```python
result = formatResults(request, result)
result = result.replace("<html>", "<html><head>"
    "<link href='//netdna.bootstrapcdn.com/twitter-bootstrap/2.2.1/"
    "css/bootstrap.no-responsive.no-icons.min.css' rel='stylesheet'>"
    "</head>")
result = result.replace("<body", "<body style='padding: 20px'")
result = result.replace("<table",
    "<table class='table table-hover'")
return result
```

and you've got a nicely formatted HTML table (for a real case you might code
want to code something more solid but it serves to illustrate a point).

#### Where are we at?

This concludes the first basic tutorial of how to write a simple SeisHub
plug-in. So with just a few lines of code you can store your XML data in the
database, make sure only valid data is stored, transform it on the fly to
other formats and have a web based interface for querying your data in a
meaningful way. This should provide you with a head start to develop your
own SeisHub plug-in tailored to your particular problem.
