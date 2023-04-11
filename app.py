from flask import Flask, render_template, redirect, url_for,request
import folium
import pandas as pd
import geopandas as gpd

from tweet_data import TweetData

class ClientApp(Flask):
  url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
  tweet_data = TweetData()
  geo_data = pd.read_csv('/home/oaster/dissertation-client/data/location_data.csv', index_col=None, header=0)
  country_geo = f'{url}/world-countries.json'
  country_df = gpd.read_file(country_geo, driver='GeoJSON')
  geo_df = country_df.merge(geo_data, on="name")
  been_queried = False

  def regenerateGeoData(self):
    self.been_queried = True
    self.geo_df = self.country_df.merge(self.geo_data, on="name")

  def resetGeoData(self):
    self.geo_data = pd.read_csv('/home/oaster/dissertation-client/data/location_data.csv', index_col=None, header=0)
    self.country_geo = f'{self.url}/world-countries.json'
    self.geo_df = self.country_df.merge(self.geo_data, on="name")
    self.been_queried = False


  def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
    super(ClientApp, self).run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)

app = ClientApp(__name__)

@app.route("/", methods=['GET','POST'])
def index():
  if request.method == 'POST':
    topics = request.form.get('topics')
    app.tweet_data.getPlaceDataForTopics(topics)
    app.geo_data = pd.read_csv('/home/oaster/dissertation-client/data/query_location_data.csv', index_col=None, header=0)
    app.regenerateGeoData()
    return redirect(url_for('topic_view',topics = topics))
  else:
    if app.been_queried:
      app.resetGeoData()
    f = folium.Figure(width=1000, height=500)
    m = folium.Map(location= [45, 38],
            tiles='openstreetmap',
            zoom_start=3,
            min_zoom = 3,
            max_bounds = True,
            zoom_control=False
    ).add_to(f)

    folium.Choropleth(
      geo_data=app.country_geo,
      name="tweets",
      data=app.geo_data,
      columns=["name", "number"],
      key_on="feature.properties.name",
      fill_color="BuPu",
      fill_opacity=0.75,
      line_opacity=0.75,
      legend_name="Number of Tweets",
      bins=8,
      reset=True
    ).add_to(m)

    style_function = lambda x: {'fillColor': '#ffffff',
                            'color':'#000000',
                            'fillOpacity': 0.1,
                            'weight': 0.1}
    highlight_function = lambda x: {'fillColor': '#0000cc',
                                    'color':'#000000',
                                    'fillOpacity': 0.50,
                                    'weight': 0.1}
    NIL = folium.features.GeoJson(
      data=app.geo_df,
      style_function=style_function,
      control=False,
      highlight_function=highlight_function,
      tooltip=folium.features.GeoJsonTooltip(
            fields=['name','number'],
            aliases=['Country','Tweets'],
            style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
      ),
      zoom_on_click=True
    )
    m.add_child(NIL)
    m.keep_in_front(NIL)

    date_labels = app.tweet_data.getDateLabels()
    date_values = app.tweet_data.getDateValues()

    topic_lables = app.tweet_data.getTopicLabels()
    topic_values = app.tweet_data.getTopicValues()

    polarity_values = app.tweet_data.getPolarityValues()

    subjectivity_values = app.tweet_data.getSubjectivityValues()

    # set the iframe width and height
    m.get_root().width = "100%"
    m.get_root().height = "720px"

    return render_template("dashboard.html", map=f.get_root()._repr_html_(), date_labels=date_labels, date_values=date_values, topic_lables=topic_lables, topic_values=topic_values,
                            polarity_values=polarity_values, subjectivity_values=subjectivity_values)

@app.route("/<topics>")
def topic_view(topics):
  f_topic = folium.Figure(width=1000, height=500)
  m_topic = folium.Map(location= [45, 38],
          tiles='openstreetmap',
          zoom_start=3,
          min_zoom = 3,
          max_bounds = True,
          zoom_control=False
  ).add_to(f_topic)

  folium.Choropleth(
    geo_data=app.country_geo,
    name="tweets",
    data=app.geo_data,
    columns=["name", "number"],
    key_on="feature.properties.name",
    fill_color="BuPu",
    fill_opacity=0.75,
    line_opacity=0.75,
    legend_name="Number of Tweets",
    bins=8,
    reset=True
  ).add_to(m_topic)

  style_function = lambda x: {'fillColor': '#ffffff',
                          'color':'#000000',
                          'fillOpacity': 0.1,
                          'weight': 0.1}
  highlight_function = lambda x: {'fillColor': '#0000cc',
                                  'color':'#000000',
                                  'fillOpacity': 0.50,
                                  'weight': 0.1}
  NIL_topic = folium.features.GeoJson(
    data=app.geo_df,
    style_function=style_function,
    control=False,
    highlight_function=highlight_function,
    tooltip=folium.features.GeoJsonTooltip(
          fields=['name','number'],
          aliases=['Country','Tweets'],
          style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
    ),
    zoom_on_click=True
  )
  m_topic.add_child(NIL_topic)
  m_topic.keep_in_front(NIL_topic)

  date_labels = app.tweet_data.getDateLabels()
  date_values = app.tweet_data.getDateValues()

  topic_date_values = app.tweet_data.getDateTopicData()

  polarity_values = app.tweet_data.getPolarityValues()

  subjectivity_values = app.tweet_data.getSubjectivityValues()

  # set the iframe width and height
  m_topic.get_root().width = "100%"
  m_topic.get_root().height = "720px"
  map_topic = f_topic.get_root()._repr_html_()

  return render_template("topic.html", map=map_topic, date_labels=date_labels, date_values=date_values, topic_date_values=topic_date_values,
                            polarity_values=polarity_values, subjectivity_values=subjectivity_values, topics=topics)

if __name__ == '__main__':
        app.run(host='0.0.0.0')