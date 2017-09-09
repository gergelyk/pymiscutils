Tree of Attributes
==================

Attempts to structurize attributes of given object.

tree
----

**tree** `(obj, split_attr=split_attr_default)`

Create a structure of Branch objects that is described by names of the attributes of `obj`. For instance:
        
>>> class C: pass
>>> c = C()
>>> setattr(c, 'foo.x', 123)
>>> setattr(c, 'foo.y', 234)
>>> setattr(c, 'bar.x', 345)
>>> setattr(c, 'bar.y', 456)
>>> t = tree(c)
>>> t.foo.x
123
>>> t.foo.y
234
>>> t.bar.x
345
>>> t.bar.y
456
     
`split_attr` is a function that takes attribute name as parameter and splits it into list of components that build path to the attribute. By default `split_attr_default` function is in use. For example:
        
>>> split_attr_default('foo.x')
['foo', 'x']
        
List of components can include also integers. Later they turn into indices. For example:
        
>>> split_attr_default('foo.x0.val')
['foo', 'x', 0, 'val']

>>> class C: pass
>>> c = C()
>>> setattr(c, 'foo.x0', 123)
>>> setattr(c, 'foo.x1', 234)
>>> setattr(c, 'foo.x02', 345)
>>> t = tree(c)
>>> t.x[0]
123
>>> t.x[1]
234
>>> t.x[2]
345
    
Names and indices can be mixed.


Branch
------

**Branch** `(self, root)`
Branch that is a component of the tree. See tree() function. Note that Branch implements idea of Extended Attributes. This means that attributes can be accessed in three ways:
            
>>> obj.foo
>>> obj['foo']
>>> getattr(obj, 'foo')

>>> obj.foo = 123
>>> obj['foo'] = 123
>>> setattr(obj, 'foo', 123)

Attribute names can be not only textual, but also numerical (indices) or of any other type.


