import dash
import flask


server = flask.Flask(__name__)
app = dash.Dash(__name__,
                assets_external_path='https://miro.medium.com/max/1200/0*jICjTiwfGMojvl_l.jpg',
                server=server,
                meta_tags=[
    # A description of the app, used by e.g.
    # search engines when displaying search results.
    {
        'name': 'H1B Analytics',
        'content': 'Analysis of public H1B salary data by city, company and job titles'
    },
    {
        'property': 'og:image',
        'content': 'https://miro.medium.com/max/1200/0*jICjTiwfGMojvl_l.jpg'
    },
    {
        'property': 'og:title',
        'content': 'image'
    },
    {
        'property': 'og:description',
        'content': 'description'
    },
    {
        'property': 'og:url',
        'content': 'https://analytics-h1b.herokuapp.com/'
    }
])
app.config.suppress_callback_exceptions = True
app.scripts.config.serve_locally = False
app.title = 'H1B Analytics'