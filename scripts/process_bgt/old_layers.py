layers = {
	'water': {
		'waterdeel': {
			'var': 'class',
			'allow_not': []
		},
	},
	'verhard': {
		'wegdeel': {
			'var': 'plus-fysiekVoorkomenWegdeel',
			'allow': ['asfalt','cementbeton','betonstraatstenen','gebakken klinkers','tegels','sierbestrating','beton element', 'waardeOnbekend']
		},
		'onbegroeidterreindeel': {
			'var': 'plus-fysiekVoorkomen',
			'allow': ['asfalt','cementbeton','kunststof','betonstraatstenen','gebakken klinkers','tegels','sierbestrating','beton element', 'waardeOnbekend']
		},
		'ondersteunendwegdeel': {
			'var': 'plus-fysiekVoorkomenOndersteunendWegdeel',
			'allow': ['asfalt','cementbeton','betonstraatstenen','gebakken klinkers','tegels','sierbestrating','beton element', 'waardeOnbekend']
		}
	},
	'onverhard': {
		'wegdeel': {
			'var': 'plus-fysiekVoorkomenWegdeel',
			'allow_not': ['asfalt','cementbeton','betonstraatstenen','gebakken klinkers','tegels','sierbestrating','beton element', 'waardeOnbekend']
		},
		'onbegroeidterreindeel': {
			'var': 'plus-fysiekVoorkomen',
			'allow_not': ['asfalt','cementbeton','kunststof','betonstraatstenen','gebakken klinkers','tegels','sierbestrating','beton element', 'waardeOnbekend']
		},
		'ondersteunendwegdeel': {
			'var': 'plus-fysiekVoorkomenOndersteunendWegdeel',
			'allow_not': ['asfalt','cementbeton','betonstraatstenen','gebakken klinkers','tegels','sierbestrating','beton element', 'waardeOnbekend']
		},
		'begroeidterreindeel': {
			'var': 'plus-fysiekVoorkomen',
			'allow_not': []
		}
	}
}
