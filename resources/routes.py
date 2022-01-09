from resources.admin import CreateAdmin, CreateModerator,DeleteModerator
from resources.auth import LoginAdministrator, LoginModerator, LoginUser, RegisterUser
from resources.ecotrail import (
    ApproveEcotrail,
    CreateEcotrailList,
    EcotrailDetail,
    EcotrailListVisitors,
    RejectEcotrail,
)

routes = (
    (EcotrailListVisitors, "/ecotrails"),
    (RegisterUser, "/register"),
    (LoginUser, "/login"),
    (CreateEcotrailList, "/users/ecotrails"),
    (EcotrailDetail, "/users/ecotrails/<int:id_>"),
    (ApproveEcotrail, "/moderators/ecotrails/<int:id_>/approve"),
    (RejectEcotrail, "/moderators/ecotrails/<int:id_>/reject"),
    (CreateAdmin, "/admins/create-admin"),
    (CreateModerator, "/admins/create-moderator"),
    (LoginModerator, "/moderators/login"),
    (LoginAdministrator, "/admins/login"),
    (DeleteModerator, "/admins/moderators/<int:id_>"),
)
