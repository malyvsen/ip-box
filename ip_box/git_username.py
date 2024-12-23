import git.config

git_username = git.config.GitConfigParser().get_value("user", "name")
