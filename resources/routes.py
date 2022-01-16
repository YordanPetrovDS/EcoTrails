from resources.admin import (
    CreateAdmin,
    CreateModerator,
    DeleteUserEcotrailPost,
    DemoteModerator,
)
from resources.auth import LoginUser, RegisterUser
from resources.ecotrail import (
    ApproveEcotrail,
    CreateEcotrailList,
    DeletePlannedEcotrail,
    DeleteVisitedEcotrail,
    EcotrailDetail,
    EcotrailListVisitors,
    GetPlannedEcotrail,
    GetVisitedEcotrail,
    PlannedEcotrail,
    RejectEcotrail,
    VisitedEcotrail,
)

routes = (
    (EcotrailListVisitors, "/ecotrails"),
    (RegisterUser, "/register"),
    (LoginUser, "/login"),
    (CreateEcotrailList, "/profile/ecotrails"),
    (EcotrailDetail, "/profile/ecotrails/<int:id_>"),
    (ApproveEcotrail, "/moderators/ecotrails/<int:id_>/approve"),
    (RejectEcotrail, "/moderators/ecotrails/<int:id_>/reject"),
    (CreateAdmin, "/admins/users/<int:id_>/create-admin"),
    (CreateModerator, "/admins/users/<int:id_>/create-moderator"),
    (DemoteModerator, "/admins/moderators/<int:id_>"),
    (DeleteUserEcotrailPost, "/admins/ecotrails/<int:id_>"),
    (VisitedEcotrail, "/ecotrails/<int:id_>/visited"),
    (PlannedEcotrail, "/ecotrails/<int:id_>/planned"),
    (GetVisitedEcotrail, "/profile/ecotrails/visited"),
    (GetPlannedEcotrail, "/profile/ecotrails/planned"),
    (DeleteVisitedEcotrail, "/profile/ecotrails/visited/<int:id_>"),
    (DeletePlannedEcotrail, "/profile/ecotrails/planned/<int:id_>"),
)
