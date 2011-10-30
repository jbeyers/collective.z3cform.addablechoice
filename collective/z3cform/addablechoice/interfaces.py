import zope.schema
import z3c.form.interfaces

class IAddableChoiceWidget(z3c.form.interfaces.ITextWidget): 
    """A choice widget with extra textline for new choices.
    """
