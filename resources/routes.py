from resources.auth import LoginAdministrator, LoginModerator, LoginUser, RegisterUser

routes = (
    (RegisterUser, "/register"),
    (LoginUser, "/login"),
    (LoginModerator, "/moderators/login"),
    (LoginAdministrator, "/admins/login"),
)
