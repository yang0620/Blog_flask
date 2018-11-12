from . import users

@users.route('/users')
def users_views():
  return "这是users中的访问路径"