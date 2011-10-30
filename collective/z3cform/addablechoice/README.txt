Introduction
============

This product adds a Keyword widget (similar to Archetypes.Widget:KeywordWidget)
for plone.z3cform.


How To Use (Doc Tests):
=======================
    
    >>> from z3c.form import testing
    >>> testing.setupFormDefaults()

In your interface schema, use the Keywords field as your field type:

    >>> import zope.interface
    >>> import zope.schema
    >>> from zope.schema.fieldproperty import FieldProperty
    >>> from collective.z3cform.keywordwidget.field import Keywords
    >>> class IFoo(zope.interface.Interface):
    ... 
    ...     id = zope.schema.TextLine(
    ...                         title=u'ID',
    ...                         readonly=True,
    ...                         required=True
    ...                         )
    ... 
    ...     keywords = Keywords(title=u'Keywords')


Let's now create a class that implements our interface.

    >>> from AccessControl.Owned import Owned
    >>> class Foo(object, Owned):
    ...     zope.interface.implements(IFoo)
    ...     id = FieldProperty(IFoo['id'])
    ...     keywords = FieldProperty(IFoo['keywords'])
    ...     
    ...     def __init__(self, id, keywords):
    ...         self.id = id
    ...         self.keywords = keywords

For the keywordwidget to work, we need to make sure that the keywords 
property is indexed in portal_catalog. 

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
    ...         return Foo(**data)
    ...     
    ...     def add(self, object):
    ...         self.context[str(object.id)] = object
    ...
    ...     def nextURL(self):
    ...         return 'index.html'


Create an AddForm:

    >>> request = TestRequest()
    >>> addForm = FooAddForm(portal, request)
    >>> addForm.update()

Check for the keyword widget and render it:

    >>> addForm.widgets.keys()
    ['id', 'keywords']

    >>> addForm.widgets['keywords'].render()
    u'<div style="width: 45%; float: left">\n<span> Existing categories </span>\n<br />\n<select id="form-widgets-keywords"\n        name="form.widgets.keywords:list"\n        class="keyword-widget required keywords-field"\n        multiple="multiple" size="14" style="width: 100%;">\n\n</select>\n</div>\n\n<div style="width: 45%; float: right;">\n<span>New categories</span>\n<br />\n<textarea id="form-widgets-keywords"\n          name="form.widgets.keywords:list" cols="15"\n          rows="13" wrap="off">\n</textarea>\n</div>\n\n<input name="form.widgets.keywords-empty-marker"\n       type="hidden" value="1" />\n\n<div class="visualClear"><!-- --></div>\n'

Let's now submit the addform with data:

    >>> request = TestRequest(form={
    ...     'form.widgets.id': u'myobject',
    ...     'form.widgets.keywords': [u'chocolate', u'vanilla'], 
    ...     'form.buttons.add': u'Add'}
    ...     )

    >>> addForm = FooAddForm(portal, request)
    >>> addForm.update()

Check that the object has been created: 

    >>> portal['myobject'] 
    <Foo object at ...>

Check that the keywords attr has been set:

    >>> portal['myobject'].keywords
    [u'chocolate', u'vanilla']

Render the widget again and check that the keywords are present and selected:


    >>> addForm.widgets['keywords'].render()
     u'<div style="width: 45%; float: left">\n<span> Existing categories </span>\n<br />\n<select id="form-widgets-keywords"\n        name="form.widgets.keywords:list"\n        class="keyword-widget required keywords-field"\n        multiple="multiple" size="14" style="width: 100%;">\n\n    \n        <option id="form-widgets-keywords-0"\n                value="chocolate" selected="selected">chocolate</option>\n\n        \n    \n    \n        <option id="form-widgets-keywords-1" value="vanilla"\n                selected="selected">vanilla</option>\n\n        \n    \n</select>\n</div>\n\n<div style="width: 45%; float: right;">\n<span>New categories</span>\n<br />\n<textarea id="form-widgets-keywords"\n          name="form.widgets.keywords:list" cols="15"\n          rows="13" wrap="off">\n</textarea>\n</div>\n\n<input name="form.widgets.keywords-empty-marker"\n       type="hidden" value="1" />\n\n<div class="visualClear"><!-- --></div>\n'

    
