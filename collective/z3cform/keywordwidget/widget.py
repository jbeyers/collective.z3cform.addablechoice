import zope.component
import zope.interface
import zope.schema
from zope.schema import vocabulary
import z3c.form
from z3c.form.i18n import MessageFactory as _
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
import interfaces

class KeywordWidget(z3c.form.browser.select.SelectWidget):

    zope.interface.implementsOnly(interfaces.IKeywordWidget)
    items = ()
    klass = u'keyword-widget'
    multiple = 'multiple'
    size = 14
    style = "width: 100%;"
    noValueToken = u''
    noValueMessage = _('no value')
    promptMessage = _('select a value ...')

    @property
    def formatted_value(self):
        if not self.value:
            return ''
        return '<br/>'.join(self.value)

    def getValuesFromRequest(self, default=z3c.form.interfaces.NOVALUE):
        """Get the values from the request and split the terms with newlines
        """
        new_val = []
        for v in self.request.get(self.name, []):
            l = [v.strip() for v in v.strip('\r').split('\r')]
            if '' in l:
                l.remove('')
            new_val += l
        return new_val

    def extract(self, default=z3c.form.interfaces.NOVALUE):
        """See z3c.form.interfaces.IWidget.
        """
        if (self.name not in self.request and
            self.name+'-empty-marker' in self.request):
            return default

        value = self.getValuesFromRequest() or default
        if value != default:
            for token in value:
                if token == self.noValueToken:
                    continue

                try:
                    self.terms.getTermByToken(token)
                except LookupError:
                    return default
        return value

    def updateTerms(self):
        if self.terms is None:
            self.terms = z3c.form.term.Terms()

        context = aq_inner(self.context)
        index = self.field.getName()
        catalog = getToolByName(context, 'portal_catalog')
        values = list(catalog.uniqueValuesFor(index))
        if None in values or '' in values:
            values = [v for v in values if v]

        added_values = self.getValuesFromRequest()
        for v in added_values:
            if v and v not in values:
                values.append(v)

        items = []
        for v in values:
            items.append(vocabulary.SimpleTerm(v, v, v))

        self.terms.terms = vocabulary.SimpleVocabulary(items)
        return self.terms


@zope.component.adapter(interfaces.IKeywordCollection, z3c.form.interfaces.IFormLayer)
@zope.interface.implementer(z3c.form.interfaces.IFieldWidget)
def KeywordFieldWidget(field, request):
    """ IFieldWidget factory for KeywordWidget 
    """
    return z3c.form.widget.FieldWidget(field, KeywordWidget(request))

