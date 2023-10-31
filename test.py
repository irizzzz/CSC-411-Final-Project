import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly

def heatmap_list(data, path):
    heatmap_data = {
        'continents':[],
        'rows':[[],[],[],[],[],[]]
    }
    
    heatmap_data['continents'] = path
    
    for na, asi, eu, af, sa, oc in zip(data[path[0]], data[path[1]], data[path[2]], data[path[3]], data[path[4]], data[path[5]]):
        heatmap_data['rows'][0].append(na)
        heatmap_data['rows'][1].append(asi)
        heatmap_data['rows'][2].append(eu)
        heatmap_data['rows'][3].append(af)
        heatmap_data['rows'][4].append(sa)
        heatmap_data['rows'][5].append(oc)
        
    return heatmap_data
    
def get_social(data,path):
    social_data = {
    'gstory':[],
    'nstory':[],
    'xg' : [],
    'yg' : [],
    'xn' : [],
    'yn' : [],
    }
    
    for start, end, story, value, place in zip(data[path[0]], data[path[1]], data[path[2]], data[path[3]], data[path[4]]):
        if(place == "North America"):
            social_data['nstory'].append(story)
            social_data['nstory'].append(story)
            social_data['nstory'].append(None)
            social_data['xn'].append(start)
            social_data['xn'].append(end)
            social_data['xn'].append(None)
            social_data['yn'].append(value)
            social_data['yn'].append(value)
            social_data['yn'].append(None)
        elif(place == "Global"):
            social_data['gstory'].append(story)
            social_data['gstory'].append(story)
            social_data['gstory'].append(None)
            social_data['xg'].append(start)
            social_data['xg'].append(end)
            social_data['xg'].append(None)
            social_data['yg'].append(value)
            social_data['yg'].append(value)
            social_data['yg'].append(None)
    return social_data
    
    
    


config = dict({'scrollZoom': True})
fig = make_subplots(rows = 2, cols = 1, shared_xaxes=True, row_heights = [0.9, 0.3], vertical_spacing=0.12, specs=[[{"type": "xy", "secondary_y": True}], [{"type": "heatmap", "secondary_y": False}]], subplot_titles=("","Natural Disaster Activity Per Continent"))

df = pd.read_csv('active.csv')
cc = pd.read_csv('monthlyavg.csv')
se = pd.read_csv('socialevents.csv')
social = get_social(se, ['sdate', 'edate', 'story', 'ccb', 'place'])


htmap = pd.read_csv('activityheatmap.csv')
ht = heatmap_list(htmap, ['North America', 'Asia', 'Europe', 'Africa', 'South America', 'Oceania'])


fig.add_trace(go.Scatter(x = cc['Date'], y = cc['Broadcasts'], name='Average # of Climate Change Mentions on TV', fill='tozeroy', line_color='grey', hovertemplate = '%{x}' + '<br>Avg Mentions: %{y}'), secondary_y = True)
fig.update_yaxes(automargin='left+top+right')

fig.add_trace(go.Scatter(
    x=df['dates'], y=df['GlobalClimate'],
    hoverinfo='x+y',
    mode='lines',
    line=dict(width=0.5), fill='tozeroy', line_color='goldenrod', name='Global Natural Disasters', hovertemplate = '%{x}' + '<br># of Disasters: %{y}'), secondary_y = False)

fig.add_trace(go.Scatter(
     x=df['dates'], y=df['NAClimate'],
    hoverinfo='x+y',
    mode='lines',
    line=dict(), fill='tozeroy', name='North American Natural Disasters', hovertemplate = '%{x}' + '<br># of Disasters: %{y}' + '<br>Avg CC Mentions During: %{y}'), secondary_y = False)

fig.add_trace(go.Scatter(
    x=social['xg'],
    y=social['yg'],
    name = 'Global Social Events',
    connectgaps=False, line=dict(color='red', width=4), hovertemplate = '%{text}' + '<br>Date: %{x}' + '<br>Avg CC Mentions During: %{y}', text = social['gstory']), secondary_y = True, row=1, col=1)

fig.add_trace(go.Scatter(
    x=social['xn'],
    y=social['yn'],
    name = 'North American Social Events', # Style name/legend entry with html tags
    connectgaps=False, line=dict(color='blue', width=4), hovertemplate = '%{text}' + '<br>Date: %{x}' + '<br>Avg CC Mentions During: %{y}', text = social['nstory']), secondary_y = True, row=1, col=1)

fig.add_trace(go.Heatmap(z=ht['rows'], x=htmap['dates'], y=ht['continents'], colorscale='Viridis', colorbar=dict(x=0.95, y=.12,len=.26, title = 'Natural Disasters'), hovertemplate = 'Continent: %{y}' + '<br>Date: %{x}' + '<br>Active Disasters: %{z}<extra></extra> '), row=2, col=1)


start_date = "2009-07-01"
end_date = "2020-01-01"

     
             

fig.update_xaxes(type="date", range=[start_date, end_date])
fig.update_yaxes(range=[0,130], secondary_y=True, row=1, col=1)
fig.update_yaxes(range=[0,130], secondary_y=False, row=1, col=1)

fig.update_xaxes(title_text="Time")

fig.update_yaxes(title_text="Natural Disasters Occurring", secondary_y=False, row=1, col=1)
fig.update_yaxes(title_text="Average Number of Climate Change Mentions on TV", secondary_y=True, row=1,col=1)


fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="right",
            active=0,
            x=0.65,
            y=0.3,
            buttons=list([
                dict(label="Reset",
                     method="relayout",
                     args=[{"xaxis.range": [start_date, end_date]}, {"yaxis.range":[0, 130]}]),
                dict(label="2009",
                     method="relayout",
                     args=[{"xaxis.range": ["2009-07-01", "2010-01-01"]}, {"yaxis.range":[0, 130, 1, 1]}]),
                dict(label="2010",
                     method="relayout",
                     args=[{"xaxis.range": ["2010-01-01", "2011-01-01"]}, {"yaxis.range":[0, 65, 1, 1]}]),
                dict(label="2011",
                     method="relayout",
                     args=[{"xaxis.range": ["2011-01-01", "2012-01-01"]}]),
                dict(label="2012",
                     method="relayout",
                     args=[{"xaxis.range": ["2012-01-01", "2013-01-01"]}]),
                dict(label="2013",
                     method="relayout",
                     args=[{"xaxis.range": ["2013-01-01", "2014-01-01"]}]),
                dict(label="2014",
                     method="relayout",
                     args=[{"xaxis.range": ["2014-01-01", "2015-01-01"]}]),
                dict(label="2015",
                     method="relayout",
                     args=[{"xaxis.range": ["2015-01-01", "2016-01-01"]}]),
                dict(label="2016",
                     method="relayout",
                     args=[{"xaxis.range": ["2016-01-01", "2017-01-01"]}]),
                dict(label="2017",
                     method="relayout",
                     args=[{"xaxis.range": ["2017-01-01", "2018-01-01"]}]),
                dict(label="2018",
                     method="relayout",
                     args=[{"xaxis.range": ["2018-01-01", "2019-01-01"]}]),
                dict(label="2019",
                     method="relayout",
                     args=[{"xaxis.range": ["2019-01-01", "2020-01-01"]}])
            ]),
        )
    ])

fig.update_layout(
    modebar_add=[
        "v1hovermode",
        "toggleSpikeLines"
    ]
)

fig.update_layout(legend_title_text='<b>Legend<b>')

fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.01,
    xanchor="right",
    x=0.94, bgcolor="white",
        bordercolor="Black",
        borderwidth=1))

fig.update_layout(title_text="Climate Change Reporting And How Different Types of World Events Affect it", title_pad_b = 0.5, title_pad_t = 0.5)
fig.update_xaxes(nticks=12)

fig.show(config=config)
#fig.write_html("app.html")
