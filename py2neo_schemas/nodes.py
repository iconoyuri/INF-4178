from py2neo.ogm import Property,RelatedFrom,RelatedTo, GraphObject, Related, Property, Label


class User(GraphObject):
    __primarykey__ = "login"

    activated = Label()

    login = Property()
    password = Property()
    email = Property()

    profile = RelatedTo('Profile', 'HAS')
    statuses = RelatedTo('Status', 'POSTS')
    groups = RelatedTo('Group', 'BELONGS')
    created_groups = RelatedTo('Group', 'CREATE')
    relatives = Related('User', 'IN_CIRCLE')
    invited = RelatedTo('User', 'INVITES')
    did_invite = RelatedFrom('User', 'INVITES')   


class Group(GraphObject):
    __primarykey__ = "identifier"

    identifier = Property()
    name = Property()
    description = Property()

    members = RelatedFrom('User', 'BELONGS')
    creator = RelatedFrom('User', 'CREATE')
    
class Status(GraphObject):

    text_content = Property()
    media_content_path = Property()

    author = RelatedFrom('User', 'POSTS')
    viewers = RelatedFrom('User', 'LOOKS')

class Profile(GraphObject):

    user = RelatedFrom('User', 'HAS')

    content = RelatedTo('Profile_info', 'COMPOSES')

class Profile_info(GraphObject):

    key = Property()
    value = Property()

    profile = RelatedFrom('Profile', 'COMPOSES')