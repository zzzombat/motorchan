from webassets import Environment, Bundle
from tornado.options import options

motorchan_env = Environment(options.static_root, options.static_url)
motorchan_env.debug = options.debug

js = Bundle(
    'js/app.coffee',
    'js/routes.coffee',
    'js/controllers/board_list.coffee',
    'js/controllers/board.coffee',
    'js/services/board.coffee',
    'js/services/thread.coffee',
    filters='coffeescript, jsmin',
    output='compiled/main.js'
)

motorchan_env.register('js', js)
