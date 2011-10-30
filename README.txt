Introduction
============

This product adds a Keyword widget (similar to Archetypes.Widget:KeywordWidget)
for plone.z3cform.


How To Use (Doc Tests):
=======================
    
    >>> from z3c.form import testing
    >>> testing.setupFormDefaults()
    >>> import zope.interface
    >>> import zope.schema
    >>> from zope.schema.fieldproperty import FieldProperty

Use the Keywords field your field type:

    >>> from collective.z3cform.keywordwidget.field import Keywords
    >>> class IFoo(zope.interface.Interface):
    ... 
    ...     keywords = Keywords(title=u'Keywords')

    >>> class Foo(object):
    ...     zope.interface.implements(IFoo)
    ...     keywords = FieldProperty(IFoo['keywords'])
    ...     
    ...     def __init__(self, keywords):
    ...             self.keywords = keywords
    ...     
    ...     def __repr__(self):
    ...             return '<%s %r>' % (self.__class__.__name__, self.name)

We need to make sure that the keywords property is indexed in portal_catalog. 

First, we write the indexer. The indexer is a special adapter that adapts the type of an object 
and provides the value of the attribute to be indexed.

    >>> from plone.indexer.decorator import indexer
    >>> @indexer(IFoo)
    ... def keywords(obj):
    ...     return IFoo(obj).keywords

We need to register our indexer as a named adapter, where the name corresponds to
the index name. In ZCML, that may be::

    <adapter name="keywords" factory=".indexers.keywords" />

For testing purpoese, we will register it directly.

    >>> from zope.component import provideAdapter
    >>> provideAdapter(keywords, name='keywords')

Now we add a form in which the widget will be rendered:

Specify the KeywordWidget factory ('KeywordFieldWidget') as the field's widgetFactory.

    >>> from z3c.form.testing import TestRequest
    >>> from z3c.form import form, field
    >>> from collective.z3cform.keywordwidget.widget import KeywordFieldWidget

    >>> class FooAddForm(form.AddForm):
    ...     
    ...     fields = field.Fields(IFoo)
    ...     fields['keywords'].widgetFactory = KeywordFieldWidget 
    ...     
    ...     def create(self, data):
    ...             return Foo(**data)
    ...     
    ...     def add(self, object):
    ...             self.context[object.id] = object
    ...     
    ...     def nextURL(self):
    ...             return 'index.hml'


Create, update and render the form:

    >>> root = app
    >>> request = TestRequest()

    >>> addForm = FooAddForm(root, request)
    >>> addForm.update()

    >>> print addForm.render()



