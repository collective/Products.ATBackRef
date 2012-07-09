----------------------------------------------
Back Reference Field and Widget for Archetypes
----------------------------------------------

Usage
=====

Use it like a field is supposed to be used. Its almost similar to
`ReferenceField`, `ReferenceWidget`/ `ReferenceBrowserWidget`.

Archetypes `Referenceable API` offers already back-references, the field/widget
allows to visualize them like forward references. The relationship (name)
of the reference must be the same as on the forward reference field given.


Usage for ArchGenXML/ UML
=========================

- in your UML tool create a relation between 2 classes and make the 'to' end of i
  the assocation navigable (such a beast is provided in the sample dir).

- add the tagged value `backreferences_support` to your model and set it to 1.

- invoke ArchGenXML,

- restart your zope and try it out

BackReferenceField for Archetypes
=================================

This is the counterpart to the ReferenceField. When you have a relation
that is managed by a ReferenceField, you can define at
the reference's target object a BackReferenceField and a BackReferenceWidget,
that alows you to navigate back and also add references to the same relation
from the other side

Installation
============

Add ``Products.ATBackRef`` as egg to your instance-part and re-run buildout::

    [buildout]
    ...

    [instance]
    ...
    eggs =
        ...
        Products.ATBackRef

You have to install it via portal_setup because it includes skin elements (the
widget templates). If your product depends on ``Products.ATBackRef`` and you
want to install it as dependency automatically through Generic Setup, add
following lines into your Generic Setup ``metadata.xml`` file
(profiles/default/metadata.xml for default)::

    <?xml version="1.0"?>
    <metadata>
        <version>...</version>
        <dependencies>
            ...
            <dependency>profile-Products.ATBackRef:default</dependency>
        </dependencies>
    </metadata>


Comaptibility
=============

Works with Plone 3 - 4.1.x, works with Chameleon.

Licence
=======

copyright 2004-2009 BlueDynamics Alliance, Austria

GNU General Public License Version 2 or later

Author
======

Phil Auerperg <phil@bluedynamics.com>
http://bluedynamics.com

Contributors
============

- Kai Diefenbach - make it ready for Plone 3
- Jens Klein - remove old school Install, use GS profile instead, eggified.
- Daniel Widerin
- Peter Holzer
