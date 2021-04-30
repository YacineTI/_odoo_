{
    'name':'project phase',
    'version':'12.0.0.2',
    'summary':'Project extend',
    'description':'Project extend',
    'category':'Project',
    'author':'Osis',
    'website':'osis.dz',
    'license':'AGPL-3',
    'depends':['project'],
    'data':[
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
	'data/phase_data.xml',
        'views/project_type_views.xml',
        'views/project_phase_views.xml',
        'views/project_views.xml',
        'views/menu.xml'
    ],
    'demo':[],
    'installable':True,
    'auto_install':False,
    'external_dependencies':{
        'python':[],
    }
}
