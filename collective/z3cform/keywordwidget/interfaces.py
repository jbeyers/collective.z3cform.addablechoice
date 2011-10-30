import zope.schema
import z3c.form.interfaces

class IKeywordWidget(z3c.form.interfaces.ISequenceWidget): 
    """A keyword widget.
    """

class IKeywordCollection(zope.schema.interfaces.ICollection):
    """ Marker interfaces for keyword collections
    """
