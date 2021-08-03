layers = {
	'water': {
		'waterdeel': {
			'var': 'class'
			'allow_not': []
		},
	},
	'verhard': {
		'wegdeel': {
			'var': 'plus-fysiekVoorkomenWegdeel',
			'allow': ['asfalt','cementbeton','betonstraatstenen','gebakken klinkers','tegels','sierbestrating','beton element',]
		},
		'onbegroeidterreindeel': {
			'var': 'plus-fysiekVoorkomen',
			'allow': ['asfalt','cementbeton','kunststof','betonstraatstenen','gebakken klinkers','tegels','sierbestrating','beton element',]
		},
		'ondersteunendwegdeel': {
			'var': 'plus-fysiekVoorkomenOndersteunendWegdeel',
			'allow': ['asfalt','cementbeton','betonstraatstenen','gebakken klinkers','tegels','sierbestrating','beton element',]
		}
	},
	'onverhard': {
		'wegdeel': {
			'var': 'plus-fysiekVoorkomenWegdeel',
			'allow_not': ['asfalt','cementbeton','betonstraatstenen','gebakken klinkers','tegels','sierbestrating','beton element',]
		},
		'onbegroeidterreindeel': {
			'var': 'plus-fysiekVoorkomen',
			'allow_not': ['asfalt','cementbeton','kunststof','betonstraatstenen','gebakken klinkers','tegels','sierbestrating','beton element',]
		},
		'ondersteunendwegdeel': {
			'var': 'plus-fysiekVoorkomenOndersteunendWegdeel',
			'allow_not': ['asfalt','cementbeton','betonstraatstenen','gebakken klinkers','tegels','sierbestrating','beton element',]
		},
		'begroeidterreindeel': {
			'var': 'plus-fysiekVoorkomen',
			'allow_not': []
		}
	}
}



