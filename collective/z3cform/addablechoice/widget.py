import zope.component
import zope.interface
import zope.schema
import z3c.form
from z3c.form.i18n import MessageFactory as _
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
import interfaces

class AddableChoiceWidget(z3c.form.browser.text.TextWidget):
    """
    A textline widget with a dropdown choice of previous values. Suitable for
    up to, say, 40 options.
    """

    zope.interface.implementsOnly(interfaces.IAddableChoiceWidget)
    items = ()
    klass = u'addablechoice-widget'
    noValueToken = u''
    promptMessage = _('select a value ...')

    def getValueFromRequest(self, default=z3c.form.interfaces.NOVALUE):
        """Get the value from the request
        """
        val = self.request.get(self.name, u'')
        val = [v for v in val if v]
        if val:
            return val[-1]
        return u''

    def extract(self, default=z3c.form.interfaces.NOVALUE):
        """See z3c.form.interfaces.IWidget.
        """
        if (self.name not in self.request and
            self.name+'-added' not in self.request and
            self.name+'-empty-marker' in self.request):
            return default

        value = self.getValueFromRequest() or default
        return value

    def options(self):
        """
        A simplified version of the choicewidget terms. We are only concerned
        with single-line text values, so we do not need complicated
        vocabularies.
        """
        context = aq_inner(self.context)
        index = self.field.getName()
        catalog = getToolByName(context, 'portal_catalog')
        values = list(catalog.uniqueValuesFor(index))
        values = [v for v in values if v]

        added_value = self.getValueFromRequest()
        if added_value and added_value not in values:
            values.append(added_value)

        options = [{'value': self.noValueToken, 'display': self.promptMessage}]
        for v in values:
            options.append({'value': v,'display': v})
        print options
        return options

@zope.component.adapter(zope.schema.TextLine, z3c.form.interfaces.IFormLayer)
@zope.interface.implementer(z3c.form.interfaces.IFieldWidget)
def AddableChoiceFieldWidget(field, request):
    """ IFieldWidget factory for AddableChoiceWidget 
    """
    return z3c.form.widget.FieldWidget(field, AddableChoiceWidget(request))

