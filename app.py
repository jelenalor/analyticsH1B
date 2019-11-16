import dash
import flask


server = flask.Flask(__name__)
app = dash.Dash(__name__,
                server=server,
                meta_tags=[
    # A description of the app, used by e.g.
    # search engines when displaying search results.
    {
        'name': 'H1B Analytics',
        'content': 'Analysis of public H1B salary data by city, company and job titles'
    },
    {
        'data-rh': 'true',
        'property': 'og:image',
        'content': 'https://user-images.githubusercontent.com/31029142/68996492-da481700-0868-11ea-8a16-9871d16d2b7b.PNG'
    },
    {
        'data-rh': 'true',
        'property': 'og:title',
        'content': 'H1B Analytics'
    },
    {
        'data-rh': 'true',
        'property': 'og:description',
        'content': 'Interactive Dashboard presenting the analysis of public H1B salary data by city, company and job titles...'
    },
    {
        'data-rh': 'true',
        'property': 'og:url',
        'content': 'https://analytics-h1b.herokuapp.com/'
    }
])
app.config.suppress_callback_exceptions = True
app.title = 'H1B Analytics'