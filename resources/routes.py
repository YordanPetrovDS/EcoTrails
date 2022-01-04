from resources.admin import CreateAdmin, CreateModerator
from resources.auth import LoginAdministrator, LoginModerator, LoginUser, RegisterUser

routes = (
    (RegisterUser, "/register"),
    (LoginUser, "/login"),
    (CreateAdmin, "/admins/create-admin"),
    (CreateModerator, "/admins/create-moderator"),
    (LoginModerator, "/moderators/login"),
    (LoginAdministrator, "/admins/login"),
)
