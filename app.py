import dash
import flask


server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server, meta_tags=[
    # A description of the app, used by e.g.
    # search engines when displaying search results.
    {
        'name': 'H1B Analytics',
        'content': 'Analysis of public H1B salary data by city, company and job titles'
    },
    {
        'title': "H1B Analytics"
    },
    {
        'property': 'og:image',
        'content': 'https://dash.plot.ly/assets/images/logo.png'
    }])
app.config.suppress_callback_exceptions = True