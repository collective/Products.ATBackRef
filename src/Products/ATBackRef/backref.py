from Products.Archetypes import config
from Products.CMFCore.utils import getToolByName
from AccessControl import ClassSecurityInfo
from Products.Archetypes.Widget import TypesWidget
    
from Products.Archetypes.config import *
from Products.Archetypes.public import *
from Products.Archetypes.exceptions import ReferenceException
from Products.Archetypes.Field import Field,ObjectField
from Products.Archetypes.Widget import ReferenceWidget
from Products.Archetypes.ReferenceEngine import Reference
from Products.Archetypes.Registry import registerField
from Products.Archetypes import public
from Products import Archetypes

from archetypes.referencebrowserwidget.widget \
     import ReferenceBrowserWidget

class BackReferenceWidget(ReferenceWidget):
    _properties = ReferenceWidget._properties.copy()
    _properties.update({
        'macro' : "backreferencewidget",
        })

    security = ClassSecurityInfo()

class BackReferenceBrowserWidget(ReferenceBrowserWidget):
    _properties = ReferenceBrowserWidget._properties.copy()
    _properties.update({
        'macro' : "backreferencebrowserwidget",
        })

    security = ClassSecurityInfo()

class BackReferenceField(ReferenceField):
    """A field for creating references between objects.

    get() returns the list of objects referenced under the relationship
    set() converts a list of target UIDs into references under the
    relationship associated with this field.

    If no vocabulary is provided by you, one will be assembled based on
    allowed_types.
    """

    _properties = ReferenceField._properties.copy()
    _properties.update({
        'type' : 'backreference',
        'default' : None,
        'widget' : BackReferenceWidget,
        })

    security  = ClassSecurityInfo()

    security.declarePrivate('get')
    def get(self, instance, aslist=False, **kwargs):
        """get() returns the list of objects referenced under the relationship
        """
        res = instance.getBRefs(relationship=self.relationship)

        #singlevalued ref fields return only the object, not a list,
        #unless explicitely specified by the aslist option
        if not self.multiValued and not aslist:
            if res:
                assert len(res) == 1
                res =res[0]
            else:
                res = None
        return res

    security.declarePrivate('set')
    def set(self, instance, value, **kwargs):
        """Mutator.

        ``value`` is a list of UIDs or one UID string to which I will add a
        reference to. None and [] are equal.

        Keyword arguments may be passed directly to addReference(), thereby
        creating properties on the reference objects.
        """
        tool = getToolByName(instance, REFERENCE_CATALOG)
        targetUIDs = [ref.sourceUID for ref in
                      tool.getBackReferences(instance, self.relationship)]

        if not self.multiValued and value \
           and type(value) not in (type(()), type([])):
            value = (value,)

        if not value:
            value = ()

        # convertobjects to uids if necessary
        uids = []
        for v in value:
            if type(v) in (type(''), type(u'')):
                uids.append(v)
            else:
                uids.append(v.UID())

        add = [v for v in uids if v and v not in targetUIDs]
        sub = [t for t in targetUIDs if t not in uids]

        # tweak keyword arguments for addReference
        addRef_kw = kwargs.copy()
        addRef_kw.setdefault('referenceClass', self.referenceClass)
        if addRef_kw.has_key('schema'): 
            del addRef_kw['schema']

        for uid in add:
            __traceback_info__ = (instance, uid, value, targetUIDs)
            if uid:
                # throws IndexError if uid is invalid
                tool.addReference(tool.lookupObject(uid), instance.UID(), 
                                  self.relationship, **addRef_kw)

        for uid in sub:
            tool.deleteReference(tool.lookupObject(uid), instance.UID(), 
                                 self.relationship)

        if self.callStorageOnSet:
            #if this option is set the reference fields's values get written
            #to the storage even if the reference field never use the storage
            #e.g. if i want to store the reference UIDs into an SQL field
            ObjectField.set(self, instance, self.getRaw(instance), **kwargs)

    security.declarePrivate('getRaw')
    def getRaw(self, instance, aslist=False, **kwargs):
        """Return the list of UIDs referenced under this fields
        relationship
        """
        rc = getToolByName(instance, REFERENCE_CATALOG)
        brains = rc(targetUID=instance.UID(),
                    relationship=self.relationship)
        res = [b.sourceUID for b in brains]
        
        if not self.multiValued and not aslist:
            if res:
                return res[0]
            return None
        return res

    def getBackReferenceImpl(self, targetObject):
        """
        Get the references efficiently, sorting if possible.
        
        If we are not using orderablereferencefield we don't have the
        order attribute we swallow this error silently.
        """
        instance=targetObject
        refs = instance.getBackReferenceImpl(self.relationship)
        try:
            refs.sort(key=lambda ref: ref.order)
        except AttributeError:
            pass
        return refs


registerField(BackReferenceField,
              title='BackReference',
              description=('Used for storing backreferences to '
                           'other Archetypes Objects'))
