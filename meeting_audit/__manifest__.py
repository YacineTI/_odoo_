{
    'name':'meeting audit',
    'version':'12.0.0.1',
    'summary':'Meeting audit',
    'description':'Ce module permet d’ajouter une série de '
                  'rencontre à un contact type société afin de '
                  'mesurer l’efficacité des rencontres dans une '
                  'organisation. ',
    'category':'HR',
    'author':'Osis',
    'website':'osis.dz',
    'license':'AGPL-3',
    'depends':['survey', 'calendar', 'website'],
    'data':[
        'views/contact_event.xml',
        'views/calendar_survey.xml',
        'views/calendar_view.xml',
        'views/meet_portal_templates.xml',
        'views/assets.xml'
    ],
    'demo':[],
    'installable':True,
    'auto_install':False,
    #'post_init_hook':'post_init_hook',
    'external_dependencies':{
        'python':[],
    },
}
