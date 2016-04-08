import vincent
import pandas as pd
import json
import bokeh
#vincent.core.initialize_notebook()

df = pd.DataFrame({'states':[u'Massachusetts',u'Vermont',u'Iowa'],'numbers':[2,5,16]})



states_topo = 'us_states.topo.json'

f = open(states_topo, 'r')
j = json.load(f)
f.close()

geoms = j['objects']['us_states.geo']['geometries']
state_names = [x['properties']['NAME'] for x in geoms]

test_df = pd.DataFrame({'states':state_names, 'numbers':range(len(state_names))})




geo_data = [{'name': 'states', 'url': states_topo, 'feature': 'us_states.geo'}]

vis = vincent.Map(data=test_df, columns=['states','numbers'], geo_data=geo_data,
                  projection='albersUsa', map_key={'states': 'NAME'}
                  #,scale=1000
                  ,data_key='states', data_bind='numbers'
                  )

vis.to_json('vis.json', html_out=True, html_path='vis.html', )
#vincent.core.initialize_notebook()
#vis.to_json('vis.json')
#vis.display()
