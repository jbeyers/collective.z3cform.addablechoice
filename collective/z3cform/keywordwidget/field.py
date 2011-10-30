import zope.component
import zope.schema
import zope.interface
import z3c.form.converter

import interfaces

class Keywords(zope.schema.List):
    """A field representing a set."""
    zope.interface.implements(interfaces.IKeywordCollection)
    unique = True
    value_type = zope.schema.TextLine()


class KeywordsDataConverter(z3c.form.converter.BaseDataConverter):
    """A special converter between collections and sequence widgets."""

    zope.component.adapts(interfaces.IKeywordCollection, interfaces.IKeywordWidget)

    def toWidgetValue(self, value):
        collectionType = self.field._type
        if isinstance(collectionType, tuple):
            collectionType = collectionType[-1]

        if value:
            return collectionType(value)
        else:
            return collectionType()

    def toFieldValue(self, value):
        """See interfaces.IDataConverter
        """
        widget = self.widget
        if widget.terms is None:
            widget.updateTerms()
        collectionType = self.field._type
        if isinstance(collectionType, tuple):
            collectionType = collectionType[-1]

        return collectionType(value)


